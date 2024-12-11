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

    def save_subtitle(self, file_to_save_name:str):
        """Saves an audio
        """
