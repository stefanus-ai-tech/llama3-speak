# Voice Assistant Project Tutorial

This tutorial will guide you through the steps to set up and run a voice assistant project using Python. The project includes recording audio, transcribing speech to text using Whisper, generating responses with Llama 3 via Ollama server, and converting text to speech using Coqui TTS.

## Prerequisites

- Python 3.10 or higher
- `pip` (Python package installer)
- `ffmpeg` (for `pydub`)

## Project Setup

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/voice-assistant-project.git
cd voice-assistant-project
```

### 2. Create a Virtual Environment

Create and activate a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install all the required Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Install ffmpeg

Ensure `ffmpeg` is installed on your system, as it is required by `pydub`:

```bash
sudo apt-get install ffmpeg  # For Debian-based systems
# On macOS
brew install ffmpeg
# On Windows, download from https://ffmpeg.org/download.html and add to PATH
```

### 5. Running the Project

You can now run the main script to start the voice assistant:

```bash
python3 main.py
```

## Project Structure

- `main.py`: The main script that handles recording, transcribing, generating responses, and text-to-speech conversion.
- `requirements.txt`: A file listing all the Python dependencies.

## Detailed Steps in `main.py`

1. **Recording Audio**:
    - The script waits for you to press Enter to start recording and again to stop.
    - The recorded audio is saved to `input.wav`.

2. **Transcribing Speech to Text**:
    - The `whisper` model transcribes the audio file, restricted to English.

3. **Generating Responses**:
    - The transcribed text is sent to the Llama 3 model via Ollama server to generate a response.

4. **Text to Speech**:
    - The response text is converted to speech using Coqui TTS and played back.


## Contributing

Feel free to submit issues and pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

