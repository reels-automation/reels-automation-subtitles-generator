from abc import ABC
from subtitle_saver.i_subtitle_saver_strategy import ISubtitleSaverStrategy

class ISubtitleGenerator(ABC):
    """Interface for the different subtitle creation strategies
    """

    def create_subtitles(self, file_path:str, audio_saving_strategy: ISubtitleSaverStrategy):
        """Creates the subtitles of a given audio
        """
        pass

    def change_model(self, language:str):
        """Changes the model based on a provided language

        Args:
            language (str): the model language
        """
        
    
