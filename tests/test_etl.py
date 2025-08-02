import unittest
import pandas as pd
from src.etl import transform

class TestETL(unittest.TestCase):
    def test_transform(self):
        data = [{'filename': 'test', 'transcription': '  Hello World  ', 'language': 'en', 'timestamp': '2025-08-02 12:05:00'}]
        df = transform(data)
        self.assertEqual(df['transcription'].iloc[0], 'hello world')

if __name__ == '__main__':
    unittest.main()
