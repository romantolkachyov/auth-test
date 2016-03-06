import unittest

from mock import MagicMock

from flask import Flask
from views import blueprint
from flask_sqlalchemy import SQLAlchemy

from exceptions import AuthException, NoBackendProvided, BackendNotFound

from backends.facebook import FacebookAuthBackend
from backends.simple import SimpleAuthBackend

from storage import SQLAlchemyStorage

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)


class UserConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    user = db.relationship(User)
    backend = db.Column(db.String, index=True)
    external_id = db.Column(db.String, index=True)
    data = db.Column(db.Text)


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask('test_app')
        self.app.config.from_object('project.settings.tests')
        self.app.config['AUTH_STORAGE'] = SQLAlchemyStorage(db.session, User, UserConnection)

        db.init_app(self.app)
        self.app.register_blueprint(blueprint, url_prefix="")

        with self.app.test_request_context('/'):
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.test_request_context('/'):
            db.drop_all()


class AuthBlueprintTestCase(BaseTestCase):
    def test_simple(self):
        res = self.client.get('/signup/')
        self.assertEqual(res.status_code, 405)
        res = self.client.get('/signin/')
        self.assertEqual(res.status_code, 405)

    def test_no_backend(self):
        with self.assertRaises(NoBackendProvided):
            self.client.post('/signup/', {})

    def test_backend_not_found(self):
        with self.assertRaises(BackendNotFound):
            self.client.post('/signup/', data=dict(type='error'))


class FacebookBackendTestCase(BaseTestCase):
    def setUp(self):
        super(FacebookBackendTestCase, self).setUp()
        self.storage = SQLAlchemyStorage(db.session, User, UserConnection)
        self.backend = FacebookAuthBackend(self.storage)

    def _count_user(self, email):
        with self.app.test_request_context('/'):
            return User.query.filter_by(email=email).count()

    def test_signup(self):
        backend = self.backend

        test_user_id = '123'
        test_app_id = self.app.config.get('FACEBOOK_APP_ID')
        test_email = 'testsignup@gmail.com'

        success_response = dict(data={
            'user_id': test_user_id,
            'app_id': test_app_id
        })

        self.assertEqual(self._count_user(test_email), 0)

        backend._debug_token_request = MagicMock(return_value=success_response)

        data = dict(
            email=test_email,
            facebook_id=test_user_id,
            facebook_token='123DCB'
        )
        with self.app.test_request_context('/signup/'):
            self.assertTrue(backend.signup(data))
            db.session.commit()

        self.assertEqual(self._count_user(test_email), 1)

        error_message = 'Some error'
        error_response = dict(error={
            'message': error_message
        })

        backend._debug_token_request = MagicMock(return_value=error_response)

        with self.app.test_request_context('/signup/'):
            with self.assertRaises(AuthException) as e:
                backend.signup(data)
                self.assertEqual(error_message, e.message)

        self.assertEqual(self._count_user(test_email), 1)

    def _create_user_and_connection(self, external_id='123'):
        with self.app.test_request_context('/'):
            user = User(email='somemail@gmail.com')
            db.session.add(user)
            connection = UserConnection(
                user=user,
                backend='facebook',
                external_id=external_id
            )
            db.session.add(connection)
            db.session.commit()

    def test_signin(self):
        test_external_id = '123'
        test_token = 'ABC123'
        access_token = 'CBA321'

        self._create_user_and_connection(external_id=test_external_id)
        backend = self.backend

        # check positive response
        response = dict(access_token=access_token)
        backend._access_token_request = MagicMock(return_value=response)

        app_id = self.app.config.get('FACEBOOK_APP_ID')
        response = dict(data=dict(user_id=test_external_id, app_id=app_id))
        backend._debug_token_request = MagicMock(return_value=response)

        data = dict(
            facebook_token=test_token,
        )

        with self.app.test_request_context('/signin/'):
            self.assertEqual(backend.signin(data), access_token)

        # check negative response
        error_msg = 'Some error happen'
        error_response = dict(error=dict(message=error_msg))
        backend._access_token_request = MagicMock(return_value=error_response)
        backend._debug_token_request = MagicMock(return_value=error_response)

        with self.app.test_request_context('/signin/'):
            with self.assertRaises(AuthException) as e:
                backend.signin(data)
                self.assertEqual(e.message, error_msg)


class SimpleBackendTestCase(BaseTestCase):
    def setUp(self):
        super(SimpleBackendTestCase, self).setUp()
        self.storage = SQLAlchemyStorage(db.session, User, UserConnection)
        self.backend = SimpleAuthBackend(self.storage)

    def test_simple(self):
        data = dict(email='some@mail.com', password='123', type='simple')
        response = self.client.post('/signup/', data=data)
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/signin/', data=data)
        self.assertEqual(response.status_code, 200)

        data['email'] = 'notexist@mail.com'
        response = self.client.post('/signin/', data=data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
