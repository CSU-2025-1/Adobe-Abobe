import aio_pika
from config.config import RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_HOST, RABBITMQ_PORT

RABBIT_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
_connection = None


async def get_connection():
    global _connection
    if _connection is None or _connection.is_closed:
        _connection = await aio_pika.connect_robust(RABBIT_URL, heartbeat=30)
    return _connection


async def get_channel():
    connection = await get_connection()
    return await connection.channel()
