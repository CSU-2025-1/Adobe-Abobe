import asyncio
import logging

from internal.broker.rabbitclient.workers import wrap_consumer, consume_filters

logging.basicConfig(
    level=logging.INFO,  # или INFO
    format="%(asctime)s [%(levelname)s] %(message)s",
)


async def serve() -> None:
    # server = grpc_aio_server()
    # filter_pb2_grpc.add_FilterServiceServicer_to_server(FilterServiceServicer(), server)
    # listen_addr = f"[::]:{config.grpc_port}"
    # server.add_insecure_port(listen_addr)
    # print(f"[filter_service][grpc] server running on {listen_addr}")
    # await server.start()
    # await server.wait_for_termination()

    await asyncio.gather(
        wrap_consumer(consume_filters, "consume_filters"),
    )


if __name__ == "__main__":
    asyncio.run(serve())
