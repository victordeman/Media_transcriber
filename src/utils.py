import logging
import os

def setup_logging(log_file="logs/transcription.log"):
    """Set up logging with file and console handlers, avoiding duplicates."""
    logger = logging.getLogger()
    if logger.handlers:
        return  # Handlers already configured
    
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
