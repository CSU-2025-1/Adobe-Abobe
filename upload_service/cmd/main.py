import asyncio
import grpc
from api import upload_pb2_grpc
from internal.delivery.grpc.handler import UploadService
from internal.broker.rabbitclient.workers import wrap_consumer
from internal.broker.rabbitclient.workers import consume_images_data


async def serve():
    # server = grpc.aio.server()
    # upload_pb2_grpc.add_UploadServiceServicer_to_server(UploadService(), server)
    # server.add_insecure_port('[::]:50051')
    # await server.start()
    # print("started on port 50051")
    # await server.wait_for_termination()

    await asyncio.gather(
        wrap_consumer(consume_images_data, "consume_images_data"),
    )

if __name__ == "__main__":
    asyncio.run(serve())
