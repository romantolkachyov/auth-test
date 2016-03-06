from flask import current_app

from exceptions import BackendNotFound


def get_backend(name):
    backends = current_app.config.get('AUTH_BACKENDS')
    storage = current_app.config.get('AUTH_STORAGE')

    if name not in backends:
        raise BackendNotFound(name)

    BackendClass = backends.get(name)

    return BackendClass(storage)
