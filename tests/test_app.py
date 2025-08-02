import unittest
import os
from src.app import save_uploaded_file
from io import BytesIO

class TestApp(unittest.TestCase):
    def test_save_uploaded_file(self):
        # Mock a file-like object
        uploaded_file = type('MockFile', (), {
            'name': 'test.wav',
            'getbuffer': lambda: BytesIO(b"test data")
        })()
        file_path = save_uploaded_file(uploaded_file)
        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(os.path.basename(file_path), 'test.wav')
        os.remove(file_path)

if __name__ == '__main__':
    unittest.main()
