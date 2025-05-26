import asyncio
from io import BytesIO

import boto3
import os
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

    async def upload_from_memory(self, buffer: BytesIO, folder: str, filename: str) -> str:
        s3_key = f"{folder}/{filename}"
        await asyncio.to_thread(
            self.s3.upload_fileobj,
            buffer,
            self.bucket_name,
            s3_key
        )
        return f"{os.getenv('S3_PUBLIC_URL')}/{self.bucket_name}/{s3_key}"

    # async def upload_filtered(self, image_id: str, file_path: str) -> str:
    #     try:
    #         start = time.perf_counter()
    #         s3_key = f"filtered/{image_id}_{uuid.uuid4().hex}.jpg"
    #         logging.info(f"[s3] uploading file: {file_path} as {s3_key}")
    #
    #         with open(file_path, 'rb') as f:
    #             file_bytes = f.read()
    #
    #         # put_object вместо upload_fileobj — быстрее
    #         await asyncio.to_thread(
    #             self.s3.put_object,
    #             Bucket=self.bucket_name,
    #             Key=s3_key,
    #             Body=file_bytes,
    #             ContentType="image/jpeg"
    #         )
    #
    #         public_url = f"{os.getenv('S3_PUBLIC_URL')}/{self.bucket_name}/{s3_key}"
    #         logging.info(f"[s3] uploaded to: {public_url}")
    #         duration = time.perf_counter() - start
    #         logging.info(f"[timing] [s3] uploaded to in {duration:.2f} seconds")
    #         return public_url
    #     except BotoCoreError as e:
    #         raise RuntimeError(f"Failed to upload to S3: {e}")
