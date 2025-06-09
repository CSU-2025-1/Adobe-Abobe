import asyncio
import logging
import time

import aio_pika
import json

from internal.core.usecase.apply_filter_usecase import apply_filter_usecase
from internal.core.usecase.get_filtered_usecase import get_filtered_usecase
from internal.repository.redis_repo import RedisRepo
from internal.repository.s3_repo import S3Repo
from internal.repository.s3_repo import s3_repo
from internal.repository.redis_repo import redis_repo
from internal.broker.rabbitclient.client import get_channel

FILTER_REQUEST_QUEUE = "filter"
FILTER_RESULT_REQUEST_QUEUE = "filtered"


async def wrap_consumer(consumer_fn, name: str):
    while True:
        try:
            channel = await get_channel()
            await consumer_fn(channel)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.exception(f"[{name}] error in consumer, restart 5 sec: {e}")
            await asyncio.sleep(5)


async def consume_filters(channel: aio_pika.channel):
    await channel.set_qos(prefetch_count=30)
    queue = await channel.declare_queue(FILTER_REQUEST_QUEUE, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process(ignore_processed=True):
                data = json.loads(message.body.decode())
                user_id = data['user_id']
                image_url = data["image_url"]
                filters = data["filters"]

                try:
                    start = time.perf_counter()

                    task_id = data.get("task_id")
                    await apply_filter_usecase(
                        user_id=user_id,
                        image_url=image_url,
                        filters=filters,
                        task_id=task_id,
                        s3_repo=s3_repo,
                        redis_repo=redis_repo
                    )
                    logging.info(f"[timing] Filter applied in {time.perf_counter() - start} seconds")

                except Exception as e:
                    logging.warning(f"[filter_worker] Failed to process filter: {e}")


async def consume_filtered(channel: aio_pika.channel):
    queue = await channel.declare_queue(FILTER_RESULT_REQUEST_QUEUE, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process(ignore_processed=True):
                data = json.loads(message.body.decode())
                task_id = data["task_id"]

                result = await get_filtered_usecase(task_id, redis_repo)

                if message.reply_to and message.correlation_id:
                    await channel.default_exchange.publish(
                        aio_pika.Message(
                            body=json.dumps(result).encode(),
                            correlation_id=message.correlation_id
                        ),
                        routing_key=message.reply_to
                    )