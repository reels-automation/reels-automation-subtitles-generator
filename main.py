from subtitle_saver.subtitle_saver_minio import SubtitleSaverMinio
from subtitles_generator.vosk_subtitle_generator import VoskSubtitleGenerator

def main():
    temp_folder = "temp_json"
    bucket_name = "subtitles-json"
    model_path = "/home/porky/Downloads/vosk-model-es-0.42"

    subtitle_saver = SubtitleSaverMinio(temp_folder,bucket_name)
    subtitle_generator = VoskSubtitleGenerator(model_path)

    subtitle_generator.create_subtitles("test.mp3", subtitle_saver)

    # subtitle_saver.save_subtitle("caca.json")

if __name__ == "__main__":
    main()
