import os
import speech_recognition as sr

recognizer = sr.Recognizer()

def recognize_file():
    input_file = "./files/audio_output.wav"
    output_file = "./files/transcription.txt"

    if os.path.exists(input_file):
        with sr.AudioFile(input_file) as source:
            audio_data = recognizer.record(source)

        result = recognizer.recognize_google(audio_data, language="pt-BR")
        print("Transcription:", result)

        with open(output_file, 'w') as f:
            f = result