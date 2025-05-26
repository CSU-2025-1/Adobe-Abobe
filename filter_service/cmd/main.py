import asyncio
import logging

from internal.broker.rabbitclient.workers import wrap_consumer, consume_filters
import utils.filters

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)


async def serve() -> None:
    await asyncio.gather(
        wrap_consumer(consume_filters, "consume_filters"),
    )


if __name__ == "__main__":
    asyncio.run(serve())
