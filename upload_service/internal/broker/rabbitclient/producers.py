import json
import logging
import aio_pika

from internal.broker.rabbitclient.client import get_channel
from tenacity import retry, stop_after_attempt, wait_fixed

IMAGE_ID_QUEUE = "image_id"


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
async def publish(routing_key: str, payload: dict):
    channel = await get_channel()
    message = json.dumps(payload).encode()
    await channel.default_exchange.publish(
        aio_pika.Message(body=message),
        routing_key=routing_key
    )


async def send_image_id_message(image_id: str, status: str):
    payload = {
        "image_id": image_id,
        "status": status,
    }

    try:
        await publish(IMAGE_ID_QUEUE, payload)
    except Exception as e:
        logging.warning(f"[send_authorization_message] RabbitMQ failed: {e}")
