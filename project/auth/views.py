from flask import Blueprint, request, jsonify

from decorators import backend_decorator
from exceptions import AuthException


blueprint = Blueprint('social_auth', __name__)


@blueprint.route('/signin/', methods=['POST'])
@backend_decorator
def signin(backend):
    try:
        return backend.signin(request.form)
    except AuthException as e:
        return jsonify(dict(message=e.message)), e.status_code


@blueprint.route('/signup/', methods=['POST'])
@backend_decorator
def signup(backend):
    try:
        return backend.signup(request.form)
    except AuthException as e:
        return jsonify(dict(message=e.message)), e.status_code
