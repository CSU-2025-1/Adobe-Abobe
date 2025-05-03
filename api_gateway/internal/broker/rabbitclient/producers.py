import json
import logging
import aio_pika

from lib.rabbitclient.client import get_channel
from lib.rabbitclient.workers import get_token, validate_token, get_uploaded_image_id
from internal.core.entity.auth import AuthRequest
from internal.core.entity.upload import UploadRequest
from tenacity import retry, stop_after_attempt, wait_fixed

AUTH_REQUEST_QUEUE = "auth_request"
AUTHORIZATION_QUEUE = "authorization"
UPLOAD_IMAGE_REQUEST_QUEUE = "upload_image"


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
async def publish(routing_key: str, payload: dict):
    channel = await get_channel()
    message = json.dumps(payload).encode()
    await channel.default_exchange.publish(
        aio_pika.Message(body=message),
        routing_key=routing_key
    )


async def send_authorization_message(auth_request: AuthRequest):
    payload = {
        "login": auth_request.login,
        "password": auth_request.password,
    }

    try:
        await publish(AUTHORIZATION_QUEUE, payload)
    except Exception as e:
        logging.warning(f"[send_authorization_message] RabbitMQ failed: {e}")

    channel = await get_channel()
    resp = await get_token(channel)

    return resp


async def send_auth_message(token: str):
    payload = {
        "token": token,
    }

    try:
        await publish(AUTH_REQUEST_QUEUE, payload)
    except Exception as e:
        logging.warning(f"[send_auth_message] RabbitMQ failed: {e}")

    channel = await get_channel()
    resp = await validate_token(channel)

    return resp


async def send_image_message(upload_request: UploadRequest):
    payload = {
        "file_data": upload_request.file_data,
        "file_name": upload_request.file_name,
        "content_type": upload_request.content_type,
        "user_id": upload_request.user_id,
    }

    try:
        await publish(UPLOAD_IMAGE_REQUEST_QUEUE, payload)
    except Exception as e:
        logging.warning(f"[send_image_message] RabbitMQ failed: {e}")

    channel = await get_channel()
    resp = await get_uploaded_image_id(channel)

    return resp
