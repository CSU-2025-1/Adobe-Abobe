import asyncio
import base64
import logging
import aio_pika
import json

from internal.broker.rabbitclient.client import get_channel
from internal.broker.rabbitclient.producers import send_image_id_message
from internal.core.entity.image import Image
from internal.core.usecase.upload import handle_upload

UPLOAD_IMAGE_REQUEST_QUEUE = "upload"


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
            async with message.process():
                try:
                    data = json.loads(message.body.decode())
                    file_data = base64.b64decode(data["file_data"])

                    file_name = data["file_name"]
                    content_type = data["content_type"]
                    user_id = data["user_id"]

                    logging.info(f"[upload] {file_name}")

                    image = Image(
                        image_id="",
                        filename=file_name,
                        content=file_data,
                        content_type=content_type,
                        user_id=user_id
                    )

                    image_id, image_url = await handle_upload(image)

                    response_payload = {
                        "image_id": image_id,
                        "status": "success",
                        "image_url": image_url,
                    }
                    await channel.default_exchange.publish(
                        aio_pika.Message(
                            body=json.dumps(response_payload).encode(),
                            correlation_id=message.correlation_id
                        ),
                        routing_key=message.reply_to
                    )

                except Exception as e:
                    logging.warning(f"[upload_worker] Failed to process upload: {e}")
