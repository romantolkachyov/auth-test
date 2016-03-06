class AuthException(Exception):
    status_code = 400

    def __unicode__(self):
        return self.message


class NoBackendProvided(AuthException):

    u"""No backend provided exception."""

    message = u"You provide backend to authorize"


class BackendNotFound(AuthException):

    u"""Authorization backend not found."""

    message = u"Authorization backend `{}` not found"

    def __init__(self, backend_name):
        self.backend_name = backend_name

    def __unicode__(self):
        return self.message.format(self.backend_name)
