# -*- coding: utf-8 -*-
import json


class BaseStorage(object):
    def create_user(self, email):
        """Create new user with provided email.

        Will raise UserAlreadyExists exception if user already in storage.
        """
        raise NotImplemented

    def create_connection(self, user_id, backend_name, external_id, data={}):
        """Create new connection or update external_id with data."""
        raise NotImplemented

    def get_user(self, email):
        """Return user id by email.

        Return None if user does not exists.
        """
        raise NotImplemented

    def is_user_exists(self, email):
        """Check user existance by email."""
        raise NotImplemented

    def get_or_create_user(self, email):
        """Get or create user by email.

        Can be overriden if storage has custom (preferred) get or create.
        """
        if self.is_user_exists(email):
            user_id = self.get_user(email)
        else:
            user_id = self.create_user(email)
        return user_id


class SQLAlchemyStorage(BaseStorage):
    def __init__(self, db_session, user_model, connection_model):
        self.db_session = db_session
        self.user_model = user_model
        self.connection_model = connection_model

    def create_user(self, email):
        obj = self.user_model(email=email)
        self.db_session.add(obj)
        self.db_session.flush()
        return obj.id

    def create_connection(self, user_id, backend_name, external_id, data={}):
        obj = self.connection_model(
            user=user_id,
            backend=backend_name,
            external_id=external_id,
            data=json.dumps(data)
        )
        self.db_session.add(obj)

    def get_user(self, email):
        obj = self._query().filter_by(email=email).first()
        if obj is not None:
            return obj.id
        return None

    def by_external_id(self, external_id):
        obj = self._query().filter_by(external_id=external_id).first()
        if obj is not None:
            return obj.id

    def is_user_exists(self, email):
        return self._query().filter_by(email=email).count() > 0

    def _query(self):
        return self.db_session.query(self.user_model)
