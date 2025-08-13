import os
import logging
import whisper
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import yaml
from datetime import datetime
from langdetect import detect
from src.utils import setup_logging

def load_config(config_path="config/config.yaml"):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def extract_audio_from_video(video_path, temp_audio_path):
    """Extract audio from a video file and save as WAV."""
    setup_logging()
    logger = logging.getLogger(__name__)
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(temp_audio_path)
        video.close()
        logger.info(f"Extracted audio from {video_path} to {temp_audio_path}")
        return temp_audio_path
    except Exception as e:
        logger.error(f"Error extracting audio from {video_path}: {e}")
        return None

def transcribe_audio(audio_path, language="en", model_name="base"):
    """Transcribe an audio file using Whisper and return the text."""
    setup_logging()
    logger = logging.getLogger(__name__)
    try:
        model = whisper.load_model(model_name)
        result = model.transcribe(audio_path, language=language)
        transcription = result["text"].strip()
        logger.info(f"Transcription for {audio_path}: {transcription}")
        return transcription if transcription else None
    except Exception as e:
        logger.error(f"Error transcribing {audio_path}: {e}")
        return None

def save_raw_transcription(filename, text):
    """Save transcription to a text file and return the path."""
    raw_path = f"data/raw/{filename}.txt"
    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return raw_path

def process_file(file_path, config):
    """Process an audio or video file and return transcription and raw file path."""
    language = config['transcription']['language']
    temp_audio_dir = config['transcription']['temp_audio_dir']
    audio_formats = config['transcription']['audio_formats']
    video_formats = config['transcription']['video_formats']
    base_filename = os.path.splitext(os.path.basename(file_path))[0]

    os.makedirs(temp_audio_dir, exist_ok=True)

    if file_path.endswith(tuple(audio_formats)):
        transcription = transcribe_audio(file_path, language)
        if transcription:
            raw_path = save_raw_transcription(base_filename, transcription)
            detected_lang = detect(transcription) if transcription else "unknown"
            return transcription, detected_lang, raw_path
        return None, None, None

    elif file_path.endswith(tuple(video_formats)):
        temp_audio_path = os.path.join(temp_audio_dir, f"{base_filename}_temp.wav")
        audio_path = extract_audio_from_video(file_path, temp_audio_path)
        if audio_path:
            transcription = transcribe_audio(audio_path, language)
            os.remove(temp_audio_path)
            if transcription:
                raw_path = save_raw_transcription(base_filename, transcription)
                detected_lang = detect(transcription) if transcription else "unknown"
                return transcription, detected_lang, raw_path
        return None, None, None

    return None, None, None
