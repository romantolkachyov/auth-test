from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # db
    from db import db
    db.init_app(app)

    # auth blueprint
    from auth import blueprint as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app
