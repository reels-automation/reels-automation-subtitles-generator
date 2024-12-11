from abc import ABC

class ISubtitleSaverStrategy(ABC):
    """Interface for the different audio saving strategies
    """
    def __init__(self, temp_folder: str):
        """_summary_

        Args:
            temp_folder (str): path to the temp folder to store files
        """
        self.temp_folder = temp_folder
    
    def get_file(self, file_name:str) -> str:
        """Gets the file to convert the subtitles

        Args:
            file_name (str): filename to get from the minio bucket

        Returns:
            local_path (str): the path where the file was downloaded temporarily
        """
        pass

    def save_subtitle(self, file_to_save_name:str):
        """Saves an audio
        """
