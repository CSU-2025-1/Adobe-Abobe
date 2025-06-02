import aio_pika
from config.config import config

RABBIT_URL = f"amqp://{config.rabbit_user}:{config.rabbit_pass}@{config.rabbit_host}:{config.rabbit_port}/"
_connection = None


async def get_connection():
    global _connection
    if _connection is None or _connection.is_closed:
        _connection = await aio_pika.connect_robust(RABBIT_URL, heartbeat=30)
    return _connection


async def get_channel():
    connection = await get_connection()
    return await connection.channel()
