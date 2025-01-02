from quixstreams import Application

from subtitle_saver.subtitle_saver_minio import SubtitleSaverMinio
from subtitles_generator.vosk_subtitle_generator import VoskSubtitleGenerator
from quix_utils.consumer import create_consumer

def main():

    app_consumer = Application(
        broker_address ="localhost:9092",
        loglevel="DEBUG",
        consumer_group = "audio_subtitles_reader",
        auto_offset_reset = "latest"
    )
    
    topic_to_subscribe = "audio_subtitles"
    bucket_name = "subtitles-json"
    audio_temp_folder = "temp_audios"

    audio_bucket_name = "audios-tts"
    subtitles_bucket_name = "subtitles-json"

    model_path = "/home/porky/Downloads/vosk-model-small-es-0.42"

    subtitle_saver = SubtitleSaverMinio(audio_temp_folder,audio_bucket_name,subtitles_bucket_name)
    subtitle_generator = VoskSubtitleGenerator(model_path)

    create_consumer(app_consumer,topic_to_subscribe, subtitle_saver, subtitle_generator)

if __name__ == "__main__":
    main()
