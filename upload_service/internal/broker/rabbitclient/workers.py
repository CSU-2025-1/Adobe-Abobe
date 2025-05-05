import asyncio
import logging
import aio_pika
import json

from lib.rabbitclient.client import get_channel
from internal.broker.rabbitclient.producers import send_image_id_message
from upload_service.internal.core.entity.image import Image
from upload_service.internal.core.usecase.upload import handle_upload

UPLOAD_IMAGE_REQUEST_QUEUE = "upload_image"

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


async def consume_images_data(channel: aio_pika.channel):
    queue = await channel.declare_queue(UPLOAD_IMAGE_REQUEST_QUEUE, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process(ignore_processed=True):
                try:
                    data = json.loads(message.body.decode())
                    file_data = data["file_data"]
                    file_name = data["file_name"]
                    content_type = data["content_type"]
                    user_id = data["user_id"]

                    image = Image(
                        filename=file_name,
                        content=file_data,
                        content_type=content_type,
                        user_id=user_id
                    )

                    image_id = await handle_upload(image)

                    await send_image_id_message(image_id=image_id, status="success")

                except Exception as e:
                    await send_image_id_message(image_id=None, status=f"error: {str(e)}")
