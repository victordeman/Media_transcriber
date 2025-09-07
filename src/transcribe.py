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
        if language == "auto":
            # Perform initial transcription to detect language
            result = model.transcribe(audio_path, language=None)
            detected_lang = result.get("language", "unknown")
            if detected_lang == "unknown":
                logger.warning(f"Language detection failed for {audio_path}, defaulting to English")
                detected_lang = "en"
        else:
            detected_lang = language
            result = model.transcribe(audio_path, language=language)
        transcription = result["text"].strip()
        logger.info(f"Transcription for {audio_path}: {transcription} (Language: {detected_lang})")
        return transcription, detected_lang if transcription else (None, "unknown")
    except Exception as e:
        logger.error(f"Error transcribing {audio_path}: {e}")
        return None, "unknown"

def save_raw_transcription(filename, text):
    """Save transcription to a text file and return the path."""
    raw_path = f"data/raw/{filename}.txt"
    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return raw_path

def process_file(file_path, config, language="en", file_format=None):
    """Process an audio or video file and return transcription, detected language, and raw file path."""
    setup_logging()
    logger = logging.getLogger(__name__)
    audio_formats = config['transcription']['audio_formats']
    video_formats = config['transcription']['video_formats']
    temp_audio_dir = config['transcription']['temp_audio_dir']
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    
    os.makedirs(temp_audio_dir, exist_ok=True)

    # Determine file format
    if file_format is None or file_format == "auto":
        file_ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        if file_ext in audio_formats:
            file_format = "audio"
        elif file_ext in video_formats:
            file_format = "video"
        else:
            logger.error(f"Unsupported file extension: {file_ext}")
            return None, "unknown", None
    else:
        file_format = file_format.lower()

    # Validate file format
    if file_format == "audio" and os.path.splitext(file_path)[1].lstrip('.') not in audio_formats:
        logger.error(f"File {file_path} is not a supported audio format: {audio_formats}")
        return None, "unknown", None
    elif file_format == "video" and os.path.splitext(file_path)[1].lstrip('.') not in video_formats:
        logger.error(f"File {file_path} is not a supported video format: {video_formats}")
        return None, "unknown", None

    # Process based on file format
    if file_format == "audio":
        transcription, detected_lang = transcribe_audio(file_path, language)
        if transcription:
            raw_path = save_raw_transcription(base_filename, transcription)
            return transcription, detected_lang, raw_path
        return None, "unknown", None
    elif file_format == "video":
        temp_audio_path = os.path.join(temp_audio_dir, f"{base_filename}_temp.wav")
        audio_path = extract_audio_from_video(file_path, temp_audio_path)
        if audio_path:
            transcription, detected_lang = transcribe_audio(audio_path, language)
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            if transcription:
                raw_path = save_raw_transcription(base_filename, transcription)
                return transcription, detected_lang, raw_path
        return None, "unknown", None

    return None, "unknown", None
