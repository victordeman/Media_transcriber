# Media Transcriber

A Python-based transcription project for audio (WAV, MP3) and video (MP4, AVI, MOV) files, with support for English language using OpenAI Whisper. Includes an ETL pipeline and a Streamlit interface for file uploads and transcription.

**Repository**: [https://github.com/victordeman/Media_transcriber](https://github.com/victordeman/Media_transcriber)

## Features
- Upload audio/video files via a Streamlit web interface.
- Transcribe files to text using OpenAI Whisper.
- Support for English language transcription.
- ETL pipeline to clean and format transcribed text into CSV.
- Download raw transcriptions and CSV outputs.

## Setup
1. Run `setup_project.sh` to create the project structure and files.
2. Install FFmpeg and add it to your system PATH.
3. Create a virtual environment: `python3 -m venv .venv`
4. Activate the virtual environment: `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run the Streamlit app: `streamlit run src/app.py`
7. Open the provided URL (e.g., http://localhost:8501) in a browser.
8. Upload audio/video files and view/download transcriptions.

## Requirements
- Python 3.8+
- FFmpeg (for audio/video processing)

## License
MIT
