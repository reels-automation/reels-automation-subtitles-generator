import os
import subprocess
import sys
import json
from vosk import Model, KaldiRecognizer, SetLogLevel

SAMPLE_RATE = 16000

SetLogLevel(0)

# Path to the Vosk model

model_path = "C:/Users/diego/Desktop/vosk-model-es-0.42/vosk-model-es-0.42"
model = Model(model_path)

def transcribe_audio(file_path, output_folder):
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(True)

    # Get the base name (without extension) for output JSON
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_json = os.path.join(output_folder, f"{base_name}.json")

    # List to accumulate word timestamps
    all_word_timestamps = []

    # Use ffmpeg to process the audio
    with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i", file_path, "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "s16le", "-"], stdout=subprocess.PIPE) as process:
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

    # Save the transcript as a JSON file
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_word_timestamps, f, ensure_ascii=False, indent=4)

    print(f"Transcription saved to: {output_json}")

# Main script to loop through a folder
def process_audios_to_transcript_folder(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all files in the input folder
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        
        # Process only files with audio extensions
        if os.path.isfile(file_path) and file_name.lower().endswith(('.mp3', '.wav', '.flac', '.ogg')):
            print(f"Processing: {file_name}")
            transcribe_audio(file_path, output_folder)
