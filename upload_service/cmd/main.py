import asyncio
import logging
from internal.repository.s3_repo import ensure_bucket_exists
from internal.broker.rabbitclient.workers import wrap_consumer, consume_images_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

CONSUMER_COUNT = 10

async def serve():
    await ensure_bucket_exists()
    await asyncio.gather(
        *[
            wrap_consumer(consume_images_data, f"consume_images_data_{i}")
            for i in range(CONSUMER_COUNT)
        ]
    )

if __name__ == "__main__":
    asyncio.run(serve())