import json

import boto3
from botocore.exceptions import ClientError
from config.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_PORT, MINIO_HOST
from urllib.parse import quote
import asyncio

bucket_name = "images"
endpoint_url = f"http://{MINIO_HOST}:{MINIO_PORT}"
print(f"[MINIO] host: {MINIO_HOST}, port: {MINIO_PORT}")
s3_client = boto3.client(
    "s3",
    endpoint_url=endpoint_url,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1"
)


async def ensure_bucket_exists():
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            try:
                s3_client.create_bucket(Bucket=bucket_name)

                public_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": ["s3:GetObject"],
                            "Resource": f"arn:aws:s3:::{bucket_name}/*"
                        }
                    ]
                }

                s3_client.put_bucket_policy(
                    Bucket=bucket_name,
                    Policy=json.dumps(public_policy)
                )
                print(f"[MINIO] Public policy set for bucket: {bucket_name}")
            except ClientError as e:
                raise Exception(f"Failed to create or configure bucket: {e}")
        else:
            raise Exception(f"Failed to check bucket: {e}")


async def upload_to_s3(image_id: str, content: bytes, content_type: str):
    await ensure_bucket_exists()
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
