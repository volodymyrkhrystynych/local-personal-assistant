# Local Personal Assistant

This project aims to build a fully local personal assistant. The first step is
setting up **speech‑to‑text** so voice commands can be transcribed without an
internet connection.

## STT Server

`server.py` provides a minimal FastAPI service that exposes a `/transcribe`
endpoint. It loads OpenAI's Whisper model and returns the transcription of an
uploaded audio file. The server attempts to load the largest model that fits on
your GPU and will default to GPU inference whenever available.

### Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python server.py
   ```
3. Send an audio file using `curl` or any HTTP client:
   ```bash
   curl -F "audio=@sample.wav" http://localhost:8000/transcribe
   ```

The server will respond with a JSON payload containing the transcribed text.

This serves as the foundation for the rest of the assistant and can later be
extended with text‑to‑speech, a local chatbot and additional functionality.
