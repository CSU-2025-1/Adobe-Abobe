import json
import logging
import aio_pika

from internal.broker.rabbitclient.client import get_channel

AUTH_RESPONSE_QUEUE = "auth_response"
VALIDATION_TOKEN_QUEUE = "token"


async def publish(routing_key: str, payload: dict):
    channel = await get_channel()
    message = json.dumps(payload).encode()
    await channel.default_exchange.publish(
        aio_pika.Message(body=message),
        routing_key=routing_key
    )


# Отправка токенов в сообщении
async def send_authorization_response(access_token: str, refresh_token: str):
    payload = {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    try:
        await publish(AUTH_RESPONSE_QUEUE, payload)
    except Exception as e:
        logging.warning(f"[send_authorization_response] RabbitMQ failed: {e}")


# Проверка актуальности токена
async def send_validation_response(valid: bool, user_id: int):
    payload = {
        "valid": valid,
        "user_id": user_id
    }

    try:
        await publish(VALIDATION_TOKEN_QUEUE, payload)
    except Exception as e:
        logging.warning(f"[send_validation_response] RabbitMQ failed: {e}")
