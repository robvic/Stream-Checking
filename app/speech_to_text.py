import os
import glob
import time
import re
import speech_recognition as sr

AUDIO_PATH = "./files/audios"
STT_PATH = "./files/raw_transcriptions/"

recognizer = sr.Recognizer()

def get_timestamp(input_file):
    timestamp = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', input_file).group(1)
    return timestamp

def recognize_file(input_file):
    timestamp = get_timestamp(input_file)
    output_file = os.path.join(STT_PATH, f"transcription_{timestamp}.txt" )

    if os.path.exists(input_file):
        with sr.AudioFile(input_file) as source:
            audio_data = recognizer.record(source)

        result = recognizer.recognize_google(audio_data, language="pt-BR")
        print("Transcription:", result)

        with open(output_file, 'w') as f:
            f.write(result)
    return output_file

def execution_loop():
    while True:
        recognize_file()
        time.sleep(30)

if __name__ == "__main__":
    files = glob.glob(os.path.join(AUDIO_PATH, '*.wav'))
    for file in files:
        print(file.replace('\\', '/'))
        recognize_file(file.replace('\\', '/'))