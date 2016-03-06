import os
import unittest
import tempfile

from flask import Flask
from views import blueprint


class AuthBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask('test_app')

        self.db_fd, self.app.config['DATABASE'] = tempfile.mkstemp()
        self.app.config['TESTING'] = True

        self.app.register_blueprint(blueprint, url_prefix="")

        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.app.config['DATABASE'])

    def test_simple(self):
        res = self.client.get('/signup/')
        self.assertEqual(res.status_code, 405)
        res = self.client.get('/signin/')
        self.assertEqual(res.status_code, 405)


if __name__ == '__main__':
    unittest.main()
