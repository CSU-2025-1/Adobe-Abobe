import asyncio
import logging
import concurrent.futures

from internal.broker.rabbitclient.workers import wrap_consumer, consume_filters, consume_filtered
import utils.filters
from internal.repository.redis_repo import RedisRepo
from internal.repository.s3_repo import S3Repo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

s3_repo = S3Repo()
redis_repo = RedisRepo()


async def serve() -> None:
    await s3_repo.init_client()
    try:
        await asyncio.gather(
            *(wrap_consumer(consume_filters, f"consume_filters_{i}") for i in range(10)),
            *(wrap_consumer(consume_filtered, f"consume_result_{i}") for i in range(10))
        )
    finally:
        await s3_repo.close_client()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=64)
    loop.set_default_executor(executor)
    loop.run_until_complete(serve())
