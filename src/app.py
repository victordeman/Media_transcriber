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
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Error saving file {uploaded_file.name}: {e}")
        return None

def check_raw_transcriptions():
    """Check if any .txt files exist in data/raw/."""
    raw_dir = "data/raw/"
    if not os.path.exists(raw_dir):
        return False
    return any(filename.endswith('.txt') for filename in os.listdir(raw_dir))

def main():
    setup_logging()
    st.title("Media Transcriber")
    st.markdown("Upload an audio (WAV, MP3) or video (MP4, AVI, MOV) file to transcribe.")

    # Load configuration
    config = load_config()

    # Language selection
    st.subheader("Language Settings")
    language_mode = st.radio(
        "Language Detection",
        ["Automatic", "Manual"],
        help="Choose 'Automatic' to detect the language or 'Manual' to select a specific language."
    )
    selected_language = None
    if language_mode == "Manual":
        language_options = {lang["name"]: lang["code"] for lang in config["transcription"]["supported_languages"]}
        selected_language_name = st.selectbox(
            "Select Language",
            list(language_options.keys()),
            help="Choose the language for transcription."
        )
        selected_language = language_options[selected_language_name]
    else:
        selected_language = "auto"

    # File format selection
    st.subheader("File Format")
    format_mode = st.radio(
        "File Format Detection",
        ["Automatic", "Manual"],
        help="Choose 'Automatic' to detect file type or 'Manual' to specify audio or video."
    )
    selected_format = None
    if format_mode == "Manual":
        selected_format = st.selectbox(
            "Select File Type",
            ["Audio", "Video"],
            help="Specify whether the file is audio or video."
        )
        selected_format = selected_format.lower()

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an audio or video file",
        type=config["transcription"]["audio_formats"] + config["transcription"]["video_formats"],
        help="Supported formats: WAV, MP3 (audio); MP4, AVI, MOV (video)"
    )

    if uploaded_file is not None:
        st.write(f"Selected file: {uploaded_file.name}")
        file_path = save_uploaded_file(uploaded_file)
        
        if file_path:
            if st.button("Transcribe"):
                with st.spinner("Transcribing..."):
                    transcription, detected_lang, raw_path = process_file(
                        file_path, config, language=selected_language, file_format=selected_format
                    )
                    
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
                        os.remove(file_path)  # Delete only on success
                    else:
                        st.error("Transcription failed. Check the logs for details.")

            if st.button("Run ETL Pipeline"):
                with st.spinner("Processing ETL..."):
                    if check_raw_transcriptions():
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
                            st.error("ETL pipeline failed. Check the logs for details.")
                    else:
                        st.error("No transcriptions available in data/raw/. Please transcribe a file first.")
        else:
            st.error("Failed to save uploaded file.")

if __name__ == "__main__":
    main()
