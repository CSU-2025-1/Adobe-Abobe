import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER')
    RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')


cfg = Config()
