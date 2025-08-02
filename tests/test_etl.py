import unittest
import pandas as pd
from src.etl import transform

class TestETL(unittest.TestCase):
    def test_transform(self):
        data = [{'filename': 'test', 'transcription': '  Hallo Welt  ', 'language': 'de-DE', 'timestamp': '2025-08-02 12:05:00'}]
        df = transform(data)
        self.assertEqual(df['transcription'].iloc[0], 'hallo welt')

if __name__ == '__main__':
    unittest.main()
