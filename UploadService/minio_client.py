import os
from minio import Minio
from dotenv import load_dotenv

load_dotenv()

client = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=os.getenv("MINIO_SECURE", "false").lower() == "true"
)

bucket_name = os.getenv("MINIO_BUCKET_NAME")

found = client.bucket_exists(bucket_name)
if not found:
    client.make_bucket(bucket_name)