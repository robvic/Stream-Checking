# Orchestrate steps
import time

import audio_recorder as ac
import speech_to_text as stt
import spellcheck as sc
import semantic_correction as sem
import term_finder as tf

CHUNK_DURATION = 30
TERM = ""

#ac.record_audio(CHUNK_DURATION, 4)
time.sleep(5)
stt.recognize_file()
time.sleep(5)
sc.correct_text_file("./files/transcription.txt", "./files/transcription_spellchecked.txt")
time.sleep(5)
text = sem.read_file()
msg = sem.send_message(text)
time.sleep(5)
sem.write_file(msg)
time.sleep(5)
tf.indexation()
time.sleep(5)
tf.find_terms(TERM)