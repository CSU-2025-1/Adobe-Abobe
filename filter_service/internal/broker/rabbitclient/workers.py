import asyncio
import logging
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
            queue = await channel.declare_queue(FILTER_REQUEST_QUEUE, durable=True)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process(ignore_processed=True):
                        data = json.loads(message.body.decode())
                        logging.debug("📩 Received raw message:", data)
                        logging.info("📩 Received raw message:", data)
                        print("📩 Received raw message:", data)
                        image_id = data["image_id"]
                        filter_obj = data["filter"]

                        redis_repo = RedisRepo()
                        s3_repo = S3Repo()

                        try:
                            filtered_url = await apply_filter_usecase(
                                image_id=image_id,
                                filter=filter_obj,
                                redis_repo=redis_repo,
                                s3_repo=s3_repo
                            )

                            await send_filtered_image_message(filtered_url)

                        except Exception as e:
                            logging.warning(f"[filter_worker] Failed to process filter: {e}")

        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.exception(f"[consume_filters] error in consumer, restart 5 sec: {e}")
            await asyncio.sleep(5)
