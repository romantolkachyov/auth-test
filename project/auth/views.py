from flask import Blueprint, request

blueprint = Blueprint('social_auth', __name__)


@blueprint.route('/signin/', methods=['POST'])
def signin():
    return "ok"


@blueprint.route('/signup/', methods=['POST'])
def signup():
    return "ok"
