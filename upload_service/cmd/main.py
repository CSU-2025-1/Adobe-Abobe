import asyncio
import grpc
from api import upload_pb2_grpc
from internal.delivery.grpc.handler import UploadService

async def serve():
    server = grpc.aio.server()
    upload_pb2_grpc.add_UploadServiceServicer_to_server(UploadService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("started on port 50051")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
