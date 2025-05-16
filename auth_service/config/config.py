import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    jwt_secret: str = str(os.getenv("JWT_SECRET"))
    db_name: str = str(os.getenv("DB_NAME"))
    db_user: str = str(os.getenv("DB_USER"))
    db_password: str = str(os.getenv("DB_PASSWORD"))
    db_host: str = str(os.getenv("DB_HOST"))
    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: str = os.getenv("REDIS_PORT")
    grpc_port: int = int(os.getenv("GRPC_PORT"))
    rabbit_user: str = os.getenv("RABBITMQ_USER")
    rabbit_pass: str = os.getenv("RABBITMQ_PASS")
    rabbit_host: str = os.getenv("RABBITMQ_HOST")
    rabbit_port: str = os.getenv("RABBITMQ_PORT")


config = Config()