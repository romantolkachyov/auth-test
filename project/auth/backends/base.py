# -*- coding: utf-8 -*-
from project.auth.exceptions import AuthException


class BaseAuthBackend(object):
    def __init__(self, storage):
        self.storage = storage

    def signup(self):
        raise NotImplemented

    def signin(self):
        raise NotImplemented

    def add_connection(self, email, backend, token, link_data=dict()):
        storage = self.storage
        user_id = storage.get_or_create_user(email)
        storage.create_connection(user_id, backend, token, link_data)
