import os 
import json
import subprocess
import setttings
from vosk import Model, KaldiRecognizer, SetLogLevel
from subtitles_generator.i_subtitle_generator import ISubtitleGenerator
from subtitle_saver.i_subtitle_saver_strategy import ISubtitleSaverStrategy


class VoskSubtitleGenerator(ISubtitleGenerator):

    def __init__(self,model_path:str, sample_rate:int = 16000):
        self.model = Model(model_path)
        self.sample_rate = sample_rate
        self.temp_json_folder = "temp_subtitles"
        SetLogLevel(0)

    def change_model(self, language:str):

        if language == "es":
            model = setttings.VOSK_MODEL_ES_PATH
        elif language == "en":
            model = setttings.VOSK_MODEL_EN_PATH
        else:
            model = setttings.VOSK_MODEL_ES_PATH #  Default value 
            print("wrong language. changing to spanish!")

        self.model = Model(model)

    def create_subtitles(self, file_path:str, audio_saving_strategy: ISubtitleSaverStrategy):
        
        rec = KaldiRecognizer(self.model, self.sample_rate)
        rec.SetWords(True)

        # Get the base name (without extension) for output JSON
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        temp_output_folder = self.temp_json_folder
        output_json = os.path.join(temp_output_folder, f"{base_name}.json")

        # List to accumulate word timestamps
        all_word_timestamps = []

        # Use ffmpeg to process the audio
        with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i", file_path, "-ar", str(self.sample_rate), "-ac", "1", "-f", "s16le", "-"], stdout=subprocess.PIPE) as process:
            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    partial_result = rec.Result()
                    partial_data = json.loads(partial_result)
                    if "result" in partial_data:
                        for word_info in partial_data["result"]:
                            all_word_timestamps.append({
                                "word": word_info["word"],
                                "start": word_info["start"],
                                "end": word_info["end"]
                            })
                else:
                    rec.PartialResult()

            # Process the final result
            final_result = json.loads(rec.FinalResult())
            if "result" in final_result:
                for word_info in final_result["result"]:
                    all_word_timestamps.append({
                        "word": word_info["word"],
                        "start": word_info["start"],
                        "end": word_info["end"]
                    })
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(all_word_timestamps, f, ensure_ascii=False, indent=4)

        os.remove(file_path)
     #  print(f"Transcription saved to: {output_json}")
        json_file = f"{base_name}.json"
      # print(json_file)
        audio_saving_strategy.save_subtitle(output_json)
        return json_file


        