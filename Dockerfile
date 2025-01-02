FROM python:3.9-slim

# Install FFmpeg and dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copies the whole app 
COPY . . 

#copies the vosk model
COPY vosk-model-small-es-0.42 vosk-model-small-cn-0.22

CMD ["python", "main.py"]