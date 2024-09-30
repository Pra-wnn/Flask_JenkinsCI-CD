# test_app.py
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './../')))
from app import app

class AppTestCase(unittest.TestCase):

    # Runs First and sets up the test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Check if the title of the page is in the response data
        self.assertIn(b'Flask MariaDB Examplessd', response.data)
    
    

if __name__ == '__main__':
    unittest.main()