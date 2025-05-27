import aiobotocore.session
from config.config import config
import os
from io import BytesIO


class S3Repo:
    def __init__(self, bucket_name: str = config.s3_bucket):
        self.bucket_name = bucket_name
        self.session = aiobotocore.session.get_session()
        self.s3_client = None

    async def init_client(self):
        if not self.s3_client:
            self.s3_client = await self.session.create_client(
                's3',
                region_name=config.s3_region,
                endpoint_url=os.getenv("S3_ENDPOINT_URL"),
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            ).__aenter__()

    async def close_client(self):
        if self.s3_client:
            await self.s3_client.__aexit__(None, None, None)

    async def upload_from_memory(self, buffer: BytesIO, folder: str, filename: str) -> str:
        await self.init_client()

        s3_key = f"{folder}/{filename}"
        buffer.seek(0)
        body = buffer.read()

        await self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=body,
            ContentType="image/jpeg"
        )

        return f"{os.getenv('S3_PUBLIC_URL')}/{self.bucket_name}/{s3_key}"


s3_repo = S3Repo()
