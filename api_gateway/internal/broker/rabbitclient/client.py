import aio_pika

from config.config import cfg

RABBIT_URL = f"amqp://{cfg.RABBITMQ_USER}:{cfg.RABBITMQ_PASS}@{cfg.RABBITMQ_HOST}:{cfg.RABBITMQ_PORT}/"
_connection = None
_channel = None


async def get_connection():
    global _connection
    if _connection is None or _connection.is_closed:
        _connection = await aio_pika.connect_robust(RABBIT_URL, heartbeat=30)
    return _connection


async def get_channel():
    global _channel
    if _channel is None or _channel.is_closed:
        conn = await get_connection()
        _channel = await conn.channel()
        await _channel.set_qos(prefetch_count=10)
    return _channel
