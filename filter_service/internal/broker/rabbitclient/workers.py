import asyncio
import logging
import aio_pika
import json

from internal.broker.rabbitclient.producers import send_filtered_image_message

FILTER_REQUEST_QUEUE = "filter"


async def consume_filters(channel: aio_pika.channel):
    while True:
        try:
            queue = await channel.declare_queue(FILTER_REQUEST_QUEUE, durable=True)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process(ignore_processed=True):
                        data = json.loads(message.body.decode())
                        image_id = data["image_id"]
                        filters = data["filters"]
                        # Методы, которые делают фильтры
                        await send_filtered_image_message()  # Сюда ответ вставить
        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.exception(f"[consume_filters] error in consumer, restart 5 sec: {e}")
            await asyncio.sleep(5)
