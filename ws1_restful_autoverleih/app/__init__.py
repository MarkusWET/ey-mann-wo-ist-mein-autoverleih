#!/usr/bin/env python
import os
from flask import Flask
from flask_misaka import Misaka
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate

# initialization
# FYI: AWS ElaticBeanstalk needs the app to be called "application".
# The starting script also has to be called "application.py"
application = Flask(__name__, template_folder="../templates")

# TODO @markuswet: look into secure config for key
application.config["SECRET_KEY"] = "the quick brown fox jumps over the lazy dog"
application.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db.sqlite")
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "db.sqlite"))

# extensions
db = SQLAlchemy(application)
migrate = Migrate(application, db)
md = Misaka()
md.init_app(application)
auth = HTTPBasicAuth()
