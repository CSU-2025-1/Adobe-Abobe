import asyncio
import logging

from internal.broker.rabbitclient.workers import wrap_consumer
from internal.broker.rabbitclient.workers import consume_images_data

logging.basicConfig(
    level=logging.INFO,  # или INFO
    format="%(asctime)s [%(levelname)s] %(message)s",
)

async def serve():


    await asyncio.gather(
        wrap_consumer(consume_images_data, "consume_images_data"),
    )

if __name__ == "__main__":
    asyncio.run(serve())
