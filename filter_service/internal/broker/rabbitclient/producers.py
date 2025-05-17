import json
import logging
import aio_pika

from internal.broker.rabbitclient.client import get_channel
from tenacity import retry, stop_after_attempt, wait_fixed

FILTERED_IMAGE_QUEUE = "filtered_image"


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
async def publish(routing_key: str, payload: dict):
    try:
        channel = await get_channel()
        message = json.dumps(payload).encode()
        logging.debug(f"Publishing to queue '{routing_key}':", payload)
        logging.info(f"Publishing to queue '{routing_key}':", payload)
        print(f"Publishing to queue '{routing_key}':", payload)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message),
            routing_key=routing_key
        )
    except Exception as e:
        print(f"Exception in publish(): {e}")
        raise


async def send_filtered_image_message(filtered_url: str):
    payload = {
        "filtered_url": filtered_url,
    }

    try:
        await publish(FILTERED_IMAGE_QUEUE, payload)
        logging.debug(f"✅ Filtered URL sent to filtered_image: {filtered_url}")
        logging.info(f"✅ Filtered URL sent to filtered_image: {filtered_url}")
        print(f"✅ Filtered URL sent to filtered_image: {filtered_url}")
    except Exception as e:
        logging.warning(f"[send_filters_message] RabbitMQ failed: {e}")
