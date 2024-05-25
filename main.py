import sounddevice as sd
import numpy as np
import wave
import whisper
import requests
from TTS.api import TTS
from pydub import AudioSegment
import simpleaudio as sa
import os
import threading

# Function to record audio
def record_audio(sample_rate=16000):
    print("Press Enter to start recording...")
    input()
    print("Recording... Press Enter to stop.")
    recording = []
    rec_event = threading.Event()

    def callback(indata, frames, time, status):
        if status:
            print(status)
        recording.append(indata.copy())

    stream = sd.InputStream(callback=callback, channels=1, samplerate=sample_rate, dtype=np.int16)
    with stream:
        input()  # Wait for Enter to stop recording
        rec_event.set()

    print("Recording finished.")
    return np.concatenate(recording, axis=0)

# Function to save audio to a file
def save_audio(filename, data, sample_rate):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes for int16
        wf.setframerate(sample_rate)
        wf.writeframes(data.tobytes())

# Function to transcribe speech to text using Whisper
def transcribe_speech(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, language="en")  # Set language to English
    return result["text"]

# Function to convert text to speech using Coqui TTS
def text_to_speech(text):
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
    tts.tts_to_file(text=text, file_path="response.wav")

    # Play the WAV file
    wave_obj = sa.WaveObject.from_wave_file("response.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

    # Remove the temporary file after playing it
    os.remove("response.wav")

# Function to converse with Llama 3 via Ollama server
def converse_with_llama3(text, history):
    url = "http://localhost:11434/api/generate"
    prompt = history + "\n" + text
    data = {"model": "llama3", "prompt": prompt, "stream": False}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data.get("response", "")
        except requests.exceptions.JSONDecodeError:
            return response.text.strip()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ""

def main():
    conversation_history = ""
    while True:
        # Record audio
        audio_data = record_audio()
        save_audio("input.wav", audio_data, 16000)
        
        # Transcribe speech to text
        user_input = transcribe_speech("input.wav")
        print(f"User: {user_input}")
        
        if user_input.lower() == "exit":
            print("Exiting conversation.")
            break
        
        conversation_history += f" {user_input}\n"
        
        # Get response from Llama 3
        llama_response = converse_with_llama3(user_input, conversation_history)
        print(f"->> {llama_response}")
        
        conversation_history += f"->> {llama_response}\n"
        
        # Convert response to speech
        text_to_speech(llama_response)

if __name__ == "__main__":
    main()
