import aio_pika
from config.config import config

RABBIT_URL = f"amqp://{config.RABBITMQ_USER}:{config.RABBITMQ_PASS}@{config.RABBITMQ_HOST}:{config.RABBITMQ_PORT}/"
_connection = None


async def get_connection():
    global _connection
    if _connection is None or _connection.is_closed:
        _connection = await aio_pika.connect_robust(RABBIT_URL, heartbeat=30)
    return _connection


async def get_channel():
    connection = await get_connection()
    return await connection.channel()
