from api import upload_pb2, upload_pb2_grpc
from internal.core.entity.image import Image
from internal.core.usecase.upload import handle_upload

class UploadService(upload_pb2_grpc.UploadServiceServicer):
    def UploadImage(self, request, context):
        image = Image(
            filename=request.filename,
            content_type=request.content_type,
            content=request.content,
            user_id=request.user_id,
            image_id=""
        )
        image_id = handle_upload(image)
        return upload_pb2.ImageUploadResponse(image_id=image_id, status="uploaded")
