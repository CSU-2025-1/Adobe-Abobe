import asyncio
import logging
import aio_pika
import json

import asyncpg
import psycopg2

from config.config import config
from internal.broker.rabbitclient.client import get_channel
# from internal.core.usecase.auth_core import AuthCore
from internal.broker.rabbitclient.producers import send_authorization_response, send_validation_response
from internal.core.usecase.refresh import refresh_tokens
from internal.core.usecase.register import register_user
from internal.core.usecase.login import login_user
from internal.core.usecase.validate import validate_token
# from internal.repository.postgres_repo import PostgresRepo
# from internal.repository.redis_repo import RedisRepo

VALIDATION_QUEUE = "validation"
AUTHORIZATION_QUEUE = "authorization"
REFRESH_QUEUE = "refresh"

# dbname = config.db_name
# user = config.db_user
# password = config.db_password
# host = config.db_host
# # подключение к бд
# conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
# pg_repo = PostgresRepo(conn)
# pg_repo.init_schema()
# redis_repo = RedisRepo()


# auth_core = AuthCore(pg_repo, redis_repo)


async def wrap_consumer(pg_repo,consumer_fn, name):
    while True:
        try:
            channel = await get_channel()
            await consumer_fn(pg_repo, channel)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.exception(f"[{name}] error in consumer, restart 5 sec: {e}")
            await asyncio.sleep(5)


# Проверить актуальность токена
async def check_authorization(pg_repo, channel: aio_pika.channel):
    queue = await channel.declare_queue(VALIDATION_QUEUE, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process(ignore_processed=True):
                data = json.loads(message.body.decode())
                token = data["token"]
                valid, user_id = validate_token(token)
                try:
                    await channel.default_exchange.publish(
                        aio_pika.Message(
                            body=json.dumps({
                                "valid": valid,
                                "user_id": user_id
                            }).encode(),
                            correlation_id=message.correlation_id
                        ),
                        routing_key=message.reply_to
                    )
                except Exception as e:
                    logging.warning(f"Login failed: {e}")


# Отправить токены после авторизации
async def consume_authorization(pg_repo, channel):
    queue = await channel.declare_queue(AUTHORIZATION_QUEUE, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process(ignore_processed=True):
                data = json.loads(message.body.decode())
                command = data["command"]
                login = data["login"]
                password = data["password"]
                response = {}
                try:
                    if command == "login":
                        tokens = await login_user(pg_repo, login, password)
                    else:
                        tokens = await register_user(pg_repo, login, password)
                    access_token, refresh_token = tokens
                    response = {
                        "status": "success",
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    }
                except Exception as e:
                    logging.warning(f"Login failed for {login}: {e}")
                    response = {
                        "status": "error",
                        "detail": str(e)
                    }

                try:
                    if not message.reply_to:
                        logging.warning("[auth] Missing reply_to — cannot respond to RPC")
                        return
                    await channel.default_exchange.publish(
                        aio_pika.Message(
                            body=json.dumps(response).encode(),
                            correlation_id=message.correlation_id
                        ),
                        routing_key=message.reply_to
                    )
                except Exception as e:
                    logging.warning(f"Login failed for {login}: {e}")


async def consume_token_refresh(channel):
    queue = await channel.declare_queue(REFRESH_QUEUE, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process(ignore_processed=True):
                data = json.loads(message.body.decode())
                token = data["refresh_token"]
                try:
                    access_token, refresh_token = refresh_tokens(token)
                    await channel.default_exchange.publish(
                        aio_pika.Message(
                            body=json.dumps({
                                "access_token": access_token,
                                "refresh_token": refresh_token
                            }).encode(),
                            correlation_id=message.correlation_id
                        ),
                        routing_key=message.reply_to
                    )
                except Exception as e:
                    logging.warning(f"Refresh failed: {e}")
