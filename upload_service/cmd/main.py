import grpc
from concurrent import futures
from api import upload_pb2_grpc
from internal.delivery.grpc.handler import UploadService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    upload_pb2_grpc.add_UploadServiceServicer_to_server(UploadService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC UploadService started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
