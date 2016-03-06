from project.auth.backends import backends

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

AUTH_BACKENDS = backends

FACEBOOK_REDIRECT_URI = 'https://www.facebook.com/connect/login_success.html'