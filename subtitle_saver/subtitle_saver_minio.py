import os
from minio import Minio
from minio.error import S3Error

from subtitle_saver.i_subtitle_saver_strategy import ISubtitleSaverStrategy

class SubtitleSaverMinio(ISubtitleSaverStrategy):

    def __init__(self, temp_folder:str, bucket_name:str):
        self.minio_client = Minio(
        "172.19.0.2:9000",
        access_key="AKIAIOSFODNN7EXAMPLE",
        secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        secure=False
        )
        self.bucket_name = bucket_name
        self.temp_folder = temp_folder
    
    
    def save_subtitle(self, file_to_save_name: str):
        current_path = os.path.join(self.temp_folder, file_to_save_name)
        self.minio_client.fput_object(
            self.bucket_name,
            file_to_save_name,
            current_path,
        )
        os.remove(current_path)


