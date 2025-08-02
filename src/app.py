import streamlit as st
import os
import sys
import pandas as pd

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.transcribe import load_config, process_file
from src.etl import process_etl
from src.utils import setup_logging

def save_uploaded_file(uploaded_file):
    """Save uploaded file to data/input/ and return the file path."""
    input_dir = "data/input/"
    os.makedirs(input_dir, exist_ok=True)
    file_path = os.path.join(input_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def main():
    setup_logging()
    st.title("Media Transcriber")
    st.markdown("Upload an audio (WAV, MP3) or video (MP4, AVI, MOV) file to transcribe (German language supported).")

    uploaded_file = st.file_uploader(
        "Choose an audio or video file",
        type=["wav", "mp3", "mp4", "avi", "mov"]
    )

    if uploaded_file is not None:
        st.write(f"Selected file: {uploaded_file.name}")
        file_path = save_uploaded_file(uploaded_file)
        
        config = load_config()

        if st.button("Transcribe"):
            with st.spinner("Transcribing..."):
                transcription, detected_lang, raw_path = process_file(file_path, config)
                
                if transcription:
                    st.success("Transcription completed!")
                    st.write(f"**Transcription**: {transcription}")
                    st.write(f"**Detected Language**: {detected_lang}")
                    
                    with open(raw_path, "rb") as f:
                        st.download_button(
                            label="Download Raw Transcription",
                            data=f,
                            file_name=os.path.basename(raw_path),
                            mime="text/plain"
                        )
                else:
                    st.error("Transcription failed. Check the logs for details.")

                os.remove(file_path)

        if st.button("Run ETL Pipeline"):
            with st.spinner("Processing ETL..."):
                csv_path = process_etl()
                if csv_path:
                    st.success("ETL pipeline completed!")
                    df = pd.read_csv(csv_path)
                    st.dataframe(df)
                    
                    with open(csv_path, "rb") as f:
                        st.download_button(
                            label="Download CSV Output",
                            data=f,
                            file_name=os.path.basename(csv_path),
                            mime="text/csv"
                        )
                else:
                    st.error("ETL pipeline failed or no transcriptions available.")

if __name__ == "__main__":
    main()