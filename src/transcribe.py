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
