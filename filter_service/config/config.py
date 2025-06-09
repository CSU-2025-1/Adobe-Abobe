import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    redis_url: str = os.getenv("REDIS_URL")

    s3_bucket: str = os.getenv("S3_BUCKET")
    s3_region: str = os.getenv("S3_REGION")
    s3_endpoint_url: str = os.getenv("S3_ENDPOINT_URL")
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_public_url: str = os.getenv("S3_PUBLIC_URL")

    rabbitmq_host: str = os.getenv("RABBITMQ_HOST")
    rabbitmq_user: str = os.getenv("RABBITMQ_USER")
    rabbitmq_pass: str = os.getenv("RABBITMQ_PASS")
    rabbitmq_port: str = os.getenv("RABBITMQ_PORT")



config = Config()
