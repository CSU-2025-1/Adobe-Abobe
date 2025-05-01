import asyncio
from grpc.aio import server as grpc_aio_server
from api.filter import filter_pb2_grpc
from internal.delivery.grpc.filter_handler import FilterServiceServicer
from config.config import config


async def serve() -> None:
    server = grpc_aio_server()
    filter_pb2_grpc.add_FilterServiceServicer_to_server(FilterServiceServicer(), server)
    listen_addr = f"[::]:{config.grpc_port}"
    server.add_insecure_port(listen_addr)
    print(f"[filter_service][grpc] server running on {listen_addr}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
