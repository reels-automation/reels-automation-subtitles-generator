import os
from minio import Minio
from minio.error import S3Error

from subtitle_saver.i_subtitle_saver_strategy import ISubtitleSaverStrategy
from dotenv import load_dotenv
from setttings import MINIO_URL

class SubtitleSaverMinio(ISubtitleSaverStrategy):

    def __init__(self, temp_folder:str, audio_bucket_name:str, subtitles_bucket_name:str ):
        load_dotenv()
        self.minio_client = Minio(
        MINIO_URL,
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
        )
        self.temp_folder = temp_folder
        self.bucket_name = audio_bucket_name
        self.subtitles_bucket_name = subtitles_bucket_name
    
    def get_file(self, file_name:str) -> str:
        local_path = os.path.join(self.temp_folder, file_name) #Temp path to save the file
     #   print("Filename: ", file_name)

        try:
            self.minio_client.fget_object(
                bucket_name="audios-tts",
                object_name=file_name,
                file_path=local_path
            )
            return local_path
        except S3Error as err:
            print(f"Error ocurred:{err}")

    def save_subtitle(self, local_path: str) -> str:

       # local_path = self.get_file(file_to_save_name)        
        file_to_save_name = os.path.basename(local_path)
        self.minio_client.fput_object(
            self.subtitles_bucket_name,
            file_to_save_name,
            local_path,
        )
        os.remove(local_path)
        print("File saved succesfulyy")
        return file_to_save_name


