import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    redis_url: str = os.getenv("REDIS_URL")
    s3_bucket: str = os.getenv("S3_BUCKET")
    s3_region: str = os.getenv("S3_REGION")
    grpc_port: int = int(os.getenv("GRPC_PORT"))


config = Config()
