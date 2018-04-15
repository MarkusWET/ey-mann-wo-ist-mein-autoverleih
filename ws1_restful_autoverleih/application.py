#!/usr/bin/env python
import os
from app import create_app
from app.data_models import Car, RentalHistory, User

# from app.currency_exchange import convert_from_eur, convert_to_eur


if __name__ == "__main__":
    application = create_app()
    application.debug = False
    application.run()
