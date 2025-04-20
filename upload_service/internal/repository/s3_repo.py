import boto3
from botocore.exceptions import ClientError
from config.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
from urllib.parse import quote
import asyncio

bucket_name = "images"

# Создаем клиента для MinIO
s3_client = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_ENDPOINT}",
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1"
)

async def upload_to_s3(image_id: str, content: bytes, content_type: str):
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(
            None,
            lambda: s3_client.put_object(
                Bucket=bucket_name,
                Key=image_id,
                Body=content,
                ContentType=content_type
            )
        )
    except ClientError as e:
        raise Exception(f"Failed to upload: {e}")

    return f"http://localhost:9000/{bucket_name}/{quote(image_id)}"
