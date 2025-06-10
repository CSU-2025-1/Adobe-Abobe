import asyncio
import base64
import json
import logging
import uuid
import aio_pika

from internal.broker.rabbitclient.client import get_channel
from internal.core.entity.auth.auth_dto import AuthRequest
from internal.core.entity.upload.upload_dto import UploadRequest
from internal.core.entity.filter.filter_dto import FilterRequest
from internal.core.entity.story.story_dto import StoryRequest

VALIDATION_QUEUE = "validation"
AUTHORIZATION_QUEUE = "authorization"
UPLOAD_IMAGE_QUEUE = "upload"
FILTER_QUEUE = "filter"
STORY_QUEUE = "filter_story"
RESULT_QUEUE = "filtered"
REFRESH_QUEUE = "refresh"


async def publish_rpc(routing_key: str, payload: dict, timeout: float = 5.0):
    channel = await get_channel()
    callback_queue = await channel.declare_queue(exclusive=True, auto_delete=True, durable=False)
    correlation_id = str(uuid.uuid4())
    future = asyncio.get_event_loop().create_future()

    async def on_response(message: aio_pika.IncomingMessage):
        try:
            if message.correlation_id == correlation_id:
                decoded = json.loads(message.body.decode())
                future.set_result(decoded)
            await message.ack()
        except Exception as e:
            logging.error(f"Failed to process/ack message: {e}")
            await message.nack(requeue=False)

    consumer_tag = await callback_queue.consume(on_response)

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(payload).encode(),
            reply_to=callback_queue.name,
            correlation_id=correlation_id,
        ),
        routing_key=routing_key
    )

    try:
        result = await asyncio.wait_for(future, timeout=timeout)
        await callback_queue.cancel(consumer_tag)
        await callback_queue.delete()
        return result
    except asyncio.TimeoutError:
        await callback_queue.cancel(consumer_tag)
        await callback_queue.delete()
        raise Exception("RPC timeout")


async def send_authorization_message(auth_request: AuthRequest, command: str):
    payload = {
        "login": auth_request.login,
        "password": auth_request.password,
        "command": command
    }
    return await publish_rpc(AUTHORIZATION_QUEUE, payload)


async def send_validate_message(token: str):
    payload = {"token": token}

    try:
        return await publish_rpc(VALIDATION_QUEUE, payload)
    except Exception as e:
        logging.warning(f"[send_auth_message] RabbitMQ failed: {e}")


async def send_refresh_token(token: str, command: str):
    payload = {"token": token, "command": command}

    try:
        return await publish_rpc(REFRESH_QUEUE, payload)
    except Exception as e:
        logging.warning(f"[send_refresh_token] RabbitMQ failed: {e}")


async def send_upload_message(upload_request: UploadRequest):
    payload = {
        "file_data": base64.b64encode(upload_request.content).decode(),
        "file_name": upload_request.filename,
        "content_type": upload_request.content_type,
        "user_id": upload_request.user_id,
    }
    return await publish_rpc(UPLOAD_IMAGE_QUEUE, payload)


async def send_story_message(story_request: StoryRequest):
    payload = {
        "user_id": story_request.user_id,
        "timestamp": story_request.timestamp
    }
    return await publish_rpc(STORY_QUEUE, payload)


async def send_filters_message(filter_request: FilterRequest):
    payload = {
        "user_id": filter_request.user_id,
        "image_url": filter_request.image_url,
        "filters": [f.dict() for f in filter_request.filters]
    }

    try:
        result = await publish_rpc(FILTER_QUEUE, payload)
        return result
    except Exception as e:
        logging.error(f"[send_filters_message] RabbitMQ failed: {e}")
        return None


async def send_filter_task_message(filter_request: FilterRequest, task_id: str):
    channel = await get_channel()
    payload = {
        "user_id": filter_request.user_id,
        "image_url": filter_request.image_url,
        "filters": [f.dict() for f in filter_request.filters],
        "task_id": task_id
    }

    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(payload).encode()),
        routing_key=FILTER_QUEUE
    )


async def send_get_filtered_message(operation_id: str):
    payload = {"task_id": operation_id}
    return await publish_rpc(RESULT_QUEUE, payload)
