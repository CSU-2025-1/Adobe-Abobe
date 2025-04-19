import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    redis_url: str = os.getenv("REDIS_URL")
    grpc_port: int = int(os.getenv("GRPC_PORT"))


config = Config()