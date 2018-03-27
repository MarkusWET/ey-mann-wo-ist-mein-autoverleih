#!/usr/bin/env python
import os
from app import app, routes, db

if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(ROOT_DIR, "app", "db.sqlite")

    if not os.path.exists(DB_PATH):
        db.create_all()
    app.run(debug=True)
