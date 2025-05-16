import asyncio
import logging
import aio_pika
import json

from internal.broker.rabbitclient.client import get_channel
from internal.core.usecase.auth_core import AuthCore

from internal.broker.rabbitclient.producers import send_authorization_response, send_validation_response

AUTH_REQUEST_QUEUE = "auth_request"
AUTHORIZATION_QUEUE = "authorization"


async def wrap_consumer(consumer_fn, name):
    while True:
        try:
            channel = await get_channel()
            await consumer_fn(channel)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.exception(f"[{name}] error in consumer, restart 5 sec: {e}")
            await asyncio.sleep(5)


# Проверить актуальность токена
async def check_authorization(channel: aio_pika.channel):
    queue = await channel.declare_queue(AUTHORIZATION_QUEUE, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process(ignore_processed=True):
                data = json.loads(message.body.decode())
                token = data["token"]
                valid, user_id = AuthCore.validate_token(token) # Методы, которые проверяют токен. В метод ниже вставить valid и user_id
                await send_validation_response(valid, user_id)


# Отправить токены после авторизации
async def give_token(channel: aio_pika.channel):
    queue = await channel.declare_queue(AUTH_REQUEST_QUEUE, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process(ignore_processed=True):
                data = json.loads(message.body.decode())
                login = data["login"]
                password = data["password"]
                try:
                    access, refresh = AuthCore.login(login, password)
                    await send_authorization_response(access, refresh)
                except Exception as e:
                    logging.warning(f"Login failed for {login}: {e}")
                    # можно сделать отправку ошибки через Rabbit, если нужно
                # Здесь написать методы для получения токенов и засунуть их в метод ниже
                await send_authorization_response()
