import asyncio
import json
import logging
import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from config.config import cfg

RABBIT_URL = f"amqp://{cfg.RABBITMQ_USER}:{cfg.RABBITMQ_PASS}@{cfg.RABBITMQ_HOST}:{cfg.RABBITMQ_PORT}/"
_connection = None
# _connection: aio_pika.RobustConnection | None = None
# _channel: aio_pika.Channel | None = None
# _callback_queue: aio_pika.Queue | None = None
# _pending_futures: dict[str, asyncio.Future] = {}


async def get_connection():
    global _connection
    if _connection is None or _connection.is_closed:
        _connection = await aio_pika.connect_robust(RABBIT_URL, heartbeat=30)
    return _connection


async def get_channel():

    connection = await get_connection()
    return await connection.channel()
    # global _channel
    # if _channel is None or _channel.is_closed:
    #     conn = await get_connection()
    #     _channel = await conn.channel()
    #     await _channel.set_qos(prefetch_count=10)
    # return _channel


# async def setup_callback_queue():
#     global _callback_queue
#
#     if _callback_queue:
#         return
#
#     channel = await get_channel()
#     _callback_queue = await channel.declare_queue(exclusive=True, auto_delete=True)
#
#     async def on_response(msg: AbstractIncomingMessage):
#         correlation_id = msg.correlation_id
#         future = _pending_futures.pop(correlation_id, None)
#
#         if future:
#             try:
#                 decoded = json.loads(msg.body.decode())
#                 future.set_result(decoded)
#                 logging.debug(f"response for {correlation_id}")
#             except Exception as e:
#                 future.set_exception(e)
#
#         await msg.ack()
#
#     await _callback_queue.consume(on_response, no_ack=False)
#     logging.info(f"Callback queue initialized: {_callback_queue.name}")
