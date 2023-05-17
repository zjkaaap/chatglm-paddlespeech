import os
import io
import pyaudio
import wave
import requests
from paddlespeech.server.bin.paddlespeech_client import ASROnlineClientExecutor, TTSOnlineClientExecutor
import tempfile
import subprocess

CHUNK = 1024

def record_audio(filename, record_seconds=5):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("开始录制...")

    frames = []

    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录制完成，正在保存...")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

def recognize_audio_using_paddlespeech(filename):
    asrclient_executor = ASROnlineClientExecutor()
    res = asrclient_executor(
        input=filename,
        server_ip="127.0.0.1",
        port=8090,
        sample_rate=16000,
        audio_format="wav")
    return res

def send_text_to_api(text):
    api_url = "http://127.0.0.1:8000"
    payload = {
        "prompt": text,
        "history": [],
        "max_length": None,
        "top_p": None,
        "temperature": None
    }
    response = requests.post(api_url, json=payload)
    return response.json()["response"]


def text_to_speech(input_text, output_filename=None):
    print("input_text:", input_text)

    if output_filename is None:
        output_filename = "output.wav"

    cmd = [
        "paddlespeech_client", "tts_online",
        "--server_ip", "127.0.0.1",
        "--port", "8092",
        "--protocol", "http",
        "--input", input_text,
        "--output", output_filename
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("PaddleSpeech TTS Client 运行失败。错误信息：", e)
        return None

    with open(output_filename, "rb") as f:
        audio_data = f.read()

    return audio_data


def play_audio(audio_data):
    with tempfile.NamedTemporaryFile(delete=True) as temp_wav_file:
        temp_wav_file.write(audio_data)
        temp_wav_file.flush()

        wf = wave.open(temp_wav_file.name, 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
        p.terminate()


filename = "output.wav"


record_audio(filename)


result = recognize_audio_using_paddlespeech(filename)


print("识别结果：", result)


response = send_text_to_api(result)


print("API回复：", response)

if response:
    audio_data = text_to_speech(response)
    if audio_data is not None:
        play_audio(audio_data)
    else:
        print("无法播放音频，因为没有音频数据。")
else:
    print("无法获取API回复，因为API返回了一个无效的响应。")



# 删除录音文件
os.remove(filename)


