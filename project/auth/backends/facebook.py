# -*- coding: utf-8 -*-
import urlparse
import requests

from flask import current_app

from base import BaseAuthBackend, AuthException


class InvalidTokenException(AuthException):

    """App id or user id didn't equals expected values."""

    status_code = 400
    message = "Wrong facebook token"


class FacebookException(AuthException):

    """Facebook exception."""

    status_code = 400

    def __init__(self, result):
        self.message = result['error']['message']
        self.result = result

    def __str__(self):
        return self.message


class FacebookAuthBackend(BaseAuthBackend):

    """Facebook authentication backend.

    Requires additional flask app configuration:

        * FACEBOOK_APP_TOKEN
        * FACEBOOK_APP_ID
        * FACEBOOK_REDIRECT_URI
    """

    api_url = 'https://graph.facebook.com/'

    def signup(self, data):
        """Signup using facebook."""
        email = data.get('email')
        user_id = data.get('facebook_id')
        user_token = data.get('facebook_token')

        # TODO: check configuration
        facebook_app_id = current_app.config.get('FACEBOOK_APP_ID')

        remote_user_id, remote_app_id = self.check_token(user_token)

        # user id check
        if user_id != remote_user_id:
            raise InvalidTokenException
        # app id check
        if facebook_app_id != remote_app_id:
            raise InvalidTokenException

        self.add_connection(email, 'facebook', user_id)

        # success
        return True

    def signin(self, data):
        """Signin using facebook."""
        facebook_token = data.get('facebook_token')
        result = self._access_token_request(facebook_token)
        if 'error' in result:
            raise FacebookException(result)
        return result['access_token']

    def check_token(self, user_token):
        app_token = current_app.config.get('FACEBOOK_APP_TOKEN')

        result = self._debug_token_request(app_token, user_token)
        if 'error' in result:
            raise AuthException(result)
        return result['data']['user_id'], result['data']['app_id']

    def _access_token_request(self, facebook_token):
        """Make request to `access_token` endpoint."""
        config = current_app.config

        redirect_uri = config.get('FACEBOOK_REDIRECT_URI')
        facebook_app_token = config.get('FACEBOOK_APP_TOKEN')
        facebook_app_id = config.get('FACEBOOK_APP_ID')

        data = dict(
            client_id=facebook_app_id,
            redirect_uri=redirect_uri,
            client_secret=facebook_app_token,
            code=facebook_token
        )
        return self._request('v2.3/oauth/access_token', data)

    def _debug_token_request(self, app_token, user_token):
        """Make request to `debug_token` endpoint."""
        data = dict(input_token=user_token, access_token=app_token)
        return self._request('debug_token', data)

    def _request(self, uri, data):
        """Make request to `graph.facebook.com` and return json."""
        url = urlparse.urljoin(self.api_url, uri)
        return requests.get(url, params=data).json()
