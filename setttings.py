import os 
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT")

if ENVIRONMENT == "DEVELOPMENT":
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
    MINIO_URL = os.getenv("MINIO_URL")
else:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER_DOCKER")
    MINIO_URL = os.getenv("MINIO_URL_DOCKER")

