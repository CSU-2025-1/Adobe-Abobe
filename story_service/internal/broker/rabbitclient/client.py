import aio_pika
from config.config import RABBITMQ_URL

async def setup_rabbit_channel():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    return channel
