import asyncio
from internal.broker.rabbitclient.workers import consume_filter_history
from internal.broker.rabbitclient.client import setup_rabbit_channel

async def serve():
    channel = await setup_rabbit_channel()
    await consume_filter_history(channel)

if __name__ == "__main__":
    asyncio.run(serve())
