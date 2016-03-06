import os
import unittest
import tempfile

from app import create_app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()

        self.app.config['TESTING'] = True

        self.client = self.app.test_client()

    def test_simple(self):
        res = self.client.get('/auth/signup/')
        self.assertEqual(res.status_code, 405)

        res = self.client.get('/auth/signin/')
        self.assertEqual(res.status_code, 405)


if __name__ == '__main__':
    unittest.main()
