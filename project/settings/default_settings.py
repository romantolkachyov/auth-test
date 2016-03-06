from project.auth.backends import backends
from project.auth.storage import SQLAlchemyStorage

from project.db import db
from project.models import User, UserConnection

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

AUTH_BACKENDS = backends
AUTH_STORAGE = SQLAlchemyStorage(db.session, User, UserConnection)

FACEBOOK_REDIRECT_URI = 'https://www.facebook.com/connect/login_success.html'
