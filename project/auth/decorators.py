from functools import wraps

from flask import request
from exceptions import NoBackendProvided

from utils import get_backend


def backend_decorator(f):
    u"""Add backend class as a first positional argument.

    Raises NoBackendProvided if no `type` in POST data.
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        backend = request.form.get('type')
        if backend is None:
            raise NoBackendProvided
        backend = get_backend(backend)
        args = list(args)
        return f(backend, *args, **kwargs)
    return wrap
