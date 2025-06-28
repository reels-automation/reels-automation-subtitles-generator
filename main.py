import os
import setttings
from quixstreams import Application
from subtitle_saver.subtitle_saver_minio import SubtitleSaverMinio
from subtitles_generator.vosk_subtitle_generator import VoskSubtitleGenerator
from quix_utils.consumer import create_consumer
from dotenv import load_dotenv
from setttings import KAFKA_BROKER, ADMIN_API
from utils import download_and_extract_voice_models

def main():
    download_and_extract_voice_models(f"{ADMIN_API}/get-files/vosk-models")        
    app_consumer = Application(
        broker_address =KAFKA_BROKER,
        loglevel="DEBUG",
        consumer_group = "audio_subtitles_reader",
        auto_offset_reset = "latest"
    )
    
    topic_to_subscribe = "audio_subtitles"
    audio_temp_folder = "temp_audios"

    audio_bucket_name = "audios-tts"
    subtitles_bucket_name = "subtitles-json"

    default_model_path = setttings.VOSK_MODEL_ES_PATH
    subtitle_saver = SubtitleSaverMinio(audio_temp_folder,audio_bucket_name,subtitles_bucket_name)
    subtitle_generator = VoskSubtitleGenerator(default_model_path)

    create_consumer(app_consumer,topic_to_subscribe, subtitle_saver, subtitle_generator)

if __name__ == "__main__":
    main()
