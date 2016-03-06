from flask import Flask


def create_app(config='local'):
    app = Flask(__name__)
    app.config.from_object('project.settings.{}'.format(config))

    # db
    from db import db
    db.init_app(app)

    # auth blueprint
    from auth import blueprint as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app
