from minio import Minio
from minio.error import S3Error
from config.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

bucket_name = "images"

def upload_to_s3(image_id: str, content: bytes, content_type: str):
    from io import BytesIO
    client.put_object(
        bucket_name,
        image_id,
        data=BytesIO(content),
        length=len(content),
        content_type=content_type
    )
    return f"http://localhost:9000/{bucket_name}/{image_id}"

