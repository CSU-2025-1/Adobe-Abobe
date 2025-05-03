import asyncio
import logging
import aio_pika
import json

from lib.rabbitclient.client import get_channel
from internal.broker.rabbitclient.producers import send_image_id_message

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


# Получение данных для загрузки изображения
async def consume_images_data(channel: aio_pika.channel):
    queue = await channel.declare_queue(UPLOAD_IMAGE_REQUEST_QUEUE, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process(ignore_processed=True):
                data = json.loads(message.body.decode())
                file_data = data["file_data"]
                file_name = data["file_name"]
                content_type = data["content_type"]
                user_id = data["user_id"]
                # Методы, которые проверяют токен. В метод ниже вставить image_id и status
                await send_image_id_message()
