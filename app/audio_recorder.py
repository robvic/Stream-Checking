import os
from datetime import datetime as dt
import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 30
AUDIO_PATH = "./files/audios/"

def find_loopback_device():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if "Virtual Audio Cable" in dev_info.get('name'):
            p.terminate()
            print(f'Found input index {i}.')
            return i
    p.terminate()
    return None

def record_audio(duration, 
                 index, 
                 format=FORMAT, 
                 channels=CHANNELS, 
                 rate=RATE, 
                 chunk=CHUNK ):
    p = pyaudio.PyAudio()
    timestamp = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(AUDIO_PATH, f"audio_output_{timestamp}.wav") 
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk,
                    input_device_index=index)

    print("Recording...")

    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    return output_file

def loop_execution(device_index):
    while True:
        record_audio(RECORD_SECONDS, device_index)

if __name__ == "__main__":
    #device_index = find_loopback_device()
    #file = record_audio(RECORD_SECONDS, device_index)
    loop_execution(4)