#!/usr/bin/env python
from app import create_app

if __name__ == "__main__":
    application = create_app()
    application.debug = False
    application.run()
