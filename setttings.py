import os 
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT")

MODELS_PATH = 'voice_models'
VOSK_MODEL_ES_PATH = os.path.join(MODELS_PATH, "vosk-model-es-0.42") 
VOSK_MODEL_EN_PATH = os.path.join(MODELS_PATH,"vosk-model-en-us-0.22")

ADMIN_API = os.getenv("ADMIN_API")

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
MINIO_URL = os.getenv("MINIO_URL")
