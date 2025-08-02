# Media Transcriber

## Purpose
The `setup_project.sh` script creates the directory structure and necessary files for the Media Transcriber project, a Python-based application for transcribing audio and video files using OpenAI Whisper with a Streamlit interface. It does not handle installations or Sig actions.

## Model Description
The Media Transcriber project uses **OpenAI Whisper**, an automatic speech recognition (ASR) model, for transcribing audio and video files. Whisper is a transformer-based model trained on a large dataset of audio and text pairs, capable of transcribing English-language audio (WAV, MP3) and video (MP4, AVI, MOV) files with high accuracy. The script configures the project to use the `base` Whisper model by default, as specified in `src/transcribe.py`, balancing performance and resource efficiency.

## Requirements File
The script generates a `requirements.txt` file in `Media_transcriber/` with the following Python dependencies required for the project:

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
