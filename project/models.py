from project.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.email


class UserConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
    backend = db.Column(db.String)
    external_id = db.Column(db.String)
    data = db.Column(db.Text)

    def __repr__(self):
        return "<UserConnection %r:%r:%r>" % (
            self.user_id,
            self.backend,
            self.external_id
        )
