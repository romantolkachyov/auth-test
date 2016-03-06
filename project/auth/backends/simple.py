# -*- coding: utf-8 -*
from hashlib import sha1
from base import BaseAuthBackend

from project.auth.exceptions import AuthException


class SimpleAuthBackend(BaseAuthBackend):
    def signup(self, data):
        email = data.get('email')
        password = self.hashpassword(data.get('password'))
        user_id = self.storage.get_user(email)
        if user_id is None:
            user_id = self.storage.create_user(email)
        else:
            raise AuthException("User already exists")
        self.storage.create_connection(user_id, 'simple', password)
        return ""

    def signin(self, data):
        email = data.get('email')
        password = self.hashpassword(data.get('password'))

        user_id = self.storage.get_user(email)
        pass_uid = self.storage.get_by_external_id(password)
        if user_id is None or user_id != pass_uid:
            raise AuthException("User does not exists")
        return ""

    def hashpassword(self, password):
        return sha1(password).hexdigest()
