FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copies the whole app 
COPY . . 

#copies the vosk model
COPY vosk-model-small-es-0.42 /app/vosk-model-small-cn-0.22

CMD ["python", "main.py"]