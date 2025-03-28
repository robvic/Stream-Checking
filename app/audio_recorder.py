import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 30

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
    OUTPUT_FILENAME = f"./files/audio_output.wav"
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

    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    device_index = find_loopback_device()
    record_audio(RECORD_SECONDS, device_index)