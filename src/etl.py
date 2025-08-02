import os
import pandas as pd
import yaml
from datetime import datetime
import logging
from src.utils import setup_logging

def load_config(config_path="config/config.yaml"):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def extract():
    setup_logging()
    logger = logging.getLogger(__name__)
    config = load_config()
    raw_dir = config['etl']['raw_dir']
    data = []
    
    for filename in os.listdir(raw_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(raw_dir, filename), 'r', encoding='utf-8') as f:
                text = f.read().strip()
                data.append({
                    'filename': filename.replace('.txt', ''),
                    'transcription': text,
                    'language': 'de-DE',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
    
    logger.info(f"Extracted {len(data)} transcriptions")
    return data

def transform(data):
    setup_logging()
    logger = logging.getLogger(__name__)
    df = pd.DataFrame(data)
    
    df['transcription'] = df['transcription'].str.strip().str.lower()
    df = df.dropna(subset=['transcription'])
    
    logger.info(f"Transformed {len(df)} rows")
    return df

def load(df, output_dir, output_format):
    setup_logging()
    logger = logging.getLogger(__name__)
    output_path = os.path.join(output_dir, f"transcriptions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_format}")
    df.to_csv(output_path, index=False, encoding='utf-8')
    logger.info(f"Saved output to {output_path}")
    return output_path

def process_etl():
    """Run the ETL pipeline and return the output CSV path."""
    config = load_config()
    data = extract()
    if data:
        df = transform(data)
        return load(df, config['etl']['output_dir'], config['etl']['output_format'])
    return None
