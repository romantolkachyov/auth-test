# -*- coding: utf-8 -*-
from project.app import create_app
from project.db import db

app = create_app()

with app.app_context():
    db.create_all()
