#!/usr/bin/env python
# -*- coding: utf-8 -*-
from suds.client import Client
import hashlib

# Get SOAP Service via suds
# url = application.config["CURRENCY_CONVERTER_WSDL"]
# TODO @markuswet: temporary fix due to dependency issues.
url = "http://currencyconverterservice-dev.eu-central-1.elasticbeanstalk.com/CurrencyService.svc?wsdl"
try:
    client = Client(url)
except:
    pass

SECRET_SOAP_KEY = b"CorrectHorseBatteryStaple"
HASHED_SOAP_KEY = hashlib.sha256(SECRET_SOAP_KEY).hexdigest()

VALID_CURRENCIES = (
    "EUR", "USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF", "ISK", "NOK", "HRK", "RUB",
    "TRY", "AUD", "BRL", "CAD", "CNY", "HKD", "IDR", "ILS", "INR", "KRW", "MXN", "MYR", "NZD", "PHP", "SGD", "THB",
    "ZAR")


def convert_from_eur(target_currency, amount):
    try:
        conversion = client.service.CrossConvert("EUR", target_currency, amount, HASHED_SOAP_KEY)
    except:
        conversion = -1
    return conversion


def convert_to_eur(input_currency, amount):
    try:
        conversion = client.service.ConvertToEur(input_currency, amount, HASHED_SOAP_KEY)
    except:
        conversion = -1
    return conversion
