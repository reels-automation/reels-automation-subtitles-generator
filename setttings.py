import os 
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT")

VOSK_MODEL_ES_PATH = "vosk-model-es-0.42"
VOSK_MODEL_EN_PATH = "vosk-model-en-us-0.22"

if ENVIRONMENT == "DEVELOPMENT":
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
    MINIO_URL = os.getenv("MINIO_URL")
else:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER_DOCKER")
    MINIO_URL = os.getenv("MINIO_URL_DOCKER")

