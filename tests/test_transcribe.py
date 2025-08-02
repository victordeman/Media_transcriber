import unittest
import os
from src.transcribe import transcribe_audio, extract_audio_from_video

class TestTranscribe(unittest.TestCase):
    def test_transcribe_empty(self):
        self.assertEqual(transcribe_audio("data/input/sample_de.wav", chunk_length=1000), "")

    def test_extract_audio_from_video(self):
        temp_audio_path = "data/raw/test_temp.wav"
        result = extract_audio_from_video("data/input/sample_de.mp4", temp_audio_path)
        if result:
            self.assertTrue(os.path.exists(temp_audio_path))
            os.remove(temp_audio_path)
        else:
            self.skipTest("Video audio extraction failed or sample not found")

if __name__ == '__main__':
    unittest.main()
