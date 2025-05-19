import asyncio
import logging
import aio_pika
import json

from internal.broker.rabbitclient.client import get_channel

AUTH_RESPONSE_QUEUE = "auth_response"
TOKEN_QUEUE = "token"
IMAGE_ID_QUEUE = "image_id"
FILTERED_IMAGE_QUEUE = "filtered_image"


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


async def wait_for_response(channel: aio_pika.channel, queue_name: str):
    queue = await channel.declare_queue(queue_name, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process(ignore_processed=True):
                data = json.loads(message.body.decode())
                return data


async def validate_token(channel: aio_pika.channel):
    response = await wait_for_response(channel, AUTH_RESPONSE_QUEUE)
    return response


async def get_token(channel: aio_pika.channel):
    response = await wait_for_response(channel, TOKEN_QUEUE)
    return response


async def get_uploaded_image_id(channel: aio_pika.channel):
    response = await wait_for_response(channel, IMAGE_ID_QUEUE)
    return {
        "image_id": response.get("image_id"),
        "status": response.get("status"),
        "image_url": response.get("image_url")
    }


async def get_filtered_image(channel: aio_pika.channel):
    response = await wait_for_response(channel, FILTERED_IMAGE_QUEUE)
    return response
