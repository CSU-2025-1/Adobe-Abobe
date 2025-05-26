import asyncio
import logging
import time

import aio_pika
import json

from internal.core.usecase.apply_filter_usecase import apply_filter_usecase
from internal.repository.redis_repo import RedisRepo
from internal.repository.s3_repo import S3Repo
from internal.broker.rabbitclient.producers import send_filtered_image_message
from internal.broker.rabbitclient.client import get_channel

FILTER_REQUEST_QUEUE = "filter"


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
    while True:
        try:
            await channel.set_qos(prefetch_count=10)
            queue = await channel.declare_queue(FILTER_REQUEST_QUEUE, durable=True)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process(ignore_processed=True):
                        data = json.loads(message.body.decode())
                        user_id = data['user_id']
                        image_url = data["image_url"]
                        filters = data["filters"]
                        s3_repo = S3Repo()

                        try:
                            start = time.perf_counter()
                            filtered_url, timestamp = await apply_filter_usecase(
                                user_id=user_id,
                                image_url=image_url,
                                filters=filters,
                                s3_repo=s3_repo
                            )
                            duration = time.perf_counter() - start
                            logging.info(f"[timing] Filter applied in {duration:.2f} seconds")

                            logging.info(f"➡ reply_to: {message.reply_to}")
                            await channel.default_exchange.publish(
                                aio_pika.Message(
                                    body=json.dumps({
                                        "filtered_url": filtered_url,
                                        "timestamp": timestamp,
                                        "filters": filters
                                    }).encode(),
                                    correlation_id=message.correlation_id
                                ),
                                routing_key=message.reply_to
                            )

                        except Exception as e:
                            logging.warning(f"[filter_worker] Failed to process filter: {e}")

        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.exception(f"[consume_filters] error in consumer, restart 5 sec: {e}")
            await asyncio.sleep(5)
