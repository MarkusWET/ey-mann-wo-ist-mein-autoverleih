#!/usr/bin/env python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate

# initialization
app = Flask(__name__)
app.config[
    'SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'  # TODO @markuswet: look into secure config for key
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(os.path.dirname(os.path.abspath(__file__)), "db.sqlite"))

# extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()
