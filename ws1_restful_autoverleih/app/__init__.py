#!/usr/bin/env python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate

# initialization
app = Flask(__name__)
app.config[
    'SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'  # TODO @markuswet: look into secure config for key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()
