import boto3
from botocore.exceptions import BotoCoreError
import os
import uuid
from config.config import config


class S3Repo:
    def __init__(self, bucket_name: str = config.s3_bucket):
        self.s3 = boto3.client(
            "s3",
            region_name=config.s3_region,
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self.bucket_name = bucket_name

    async def upload_filtered(self, image_id: str, file_path: str) -> str:
        try:
            s3_key = f"filtered/{image_id}_{uuid.uuid4().hex}.jpg"

            self.s3.upload_file(file_path, self.bucket_name, s3_key)

            public_url = f"{os.getenv('S3_PUBLIC_URL')}/{self.bucket_name}/{s3_key}"
            return public_url
        except BotoCoreError as e:
            raise RuntimeError(f"Failed to upload to S3: {e}")

