import json
import logging
import aio_pika

from internal.broker.rabbitclient.client import get_channel
from internal.broker.rabbitclient.workers import get_token, validate_token, get_uploaded_image_id, get_filtered_image
from internal.core.entity.auth.auth_dto import AuthRequest
from internal.core.entity.upload.upload_dto import UploadRequest
from tenacity import retry, stop_after_attempt, wait_fixed
from internal.core.entity.filter.filter_dto import FilterRequest


AUTH_REQUEST_QUEUE = "auth_request"
AUTHORIZATION_QUEUE = "authorization"
UPLOAD_IMAGE_REQUEST_QUEUE = "upload_image"
FILTER_REQUEST_QUEUE = "filter"


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
        "file_data": upload_request.content,
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


async def send_filters_message(filter_request: FilterRequest):
    payload = {
        "image_id": filter_request.image_id,
        "filter": {
            "type": filter_request.filter.type,
            "value": filter_request.filter.value
        }
    }

    try:
        await publish(FILTER_REQUEST_QUEUE, payload)
    except Exception as e:
        logging.warning(f"[send_filters_message] RabbitMQ failed: {e}")

    channel = await get_channel()
    resp = await get_filtered_image(channel)

    return resp
