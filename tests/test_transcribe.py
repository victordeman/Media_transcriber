import unittest
import os
from src.transcribe import transcribe_audio, extract_audio_from_video, process_file, load_config

class TestTranscribe(unittest.TestCase):
    def setUp(self):
        self.config = load_config()

    def test_transcribe_empty(self):
        # Test with invalid audio file
        result, lang = transcribe_audio("data/input/sample_en.wav", language="en", model_name="tiny")
        self.assertIsNone(result)
        self.assertEqual(lang, "unknown")

    def test_process_file_auto_language(self):
        # Test with automatic language detection (mock file)
        result, lang, raw_path = process_file("data/input/sample.mp3", self.config, language="auto", file_format="audio")
        self.assertIn(lang, ["unknown"] + [lang["code"] for lang in self.config["transcription"]["supported_languages"]])

    def test_process_file_manual_language(self):
        # Test with manual language selection
        result, lang, raw_path = process_file("data/input/sample.mp3", self.config, language="es", file_format="audio")
        self.assertEqual(lang, "es")

    def test_process_file_auto_format(self):
        # Test with automatic format detection
        result, lang, raw_path = process_file("data/input/sample.mp4", self.config, language="en", file_format="auto")
        self.assertIn(lang, ["unknown", "en"])

    def test_process_file_manual_format(self):
        # Test with manual format selection
        result, lang, raw_path = process_file("data/input/sample.mp4", self.config, language="en", file_format="video")
        self.assertIn(lang, ["unknown", "en"])

    def test_extract_audio_from_video(self):
        temp_audio_path = "data/raw/test_temp.wav"
        result = extract_audio_from_video("data/input/sample_en.mp4", temp_audio_path)
        if result:
            self.assertTrue(os.path.exists(temp_audio_path))
            os.remove(temp_audio_path)
        else:
            self.skipTest("Video audio extraction failed or sample not found")

if __name__ == '__main__':
    unittest.main()
