#!/usr/bin/env python
# -*- coding: utf-8 -*-
import suds
from suds.client import Client
import hashlib

# Get SOAP Service via suds
# TODO @markuswet: implement error handling when CurrencyService is offline.
url = "http://currencyconverterservice-dev.eu-central-1.elasticbeanstalk.com/CurrencyService.svc?wsdl"
client = Client(url)

SECRET_SOAP_KEY = b"CorrectHorseBatteryStaple"
HASHED_SOAP_KEY = hashlib.sha256(SECRET_SOAP_KEY).hexdigest()

VALID_CURRENCIES = (
    "EUR", "USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF", "ISK", "NOK", "HRK", "RUB",
    "TRY", "AUD", "BRL", "CAD", "CNY", "HKD", "IDR", "ILS", "INR", "KRW", "MXN", "MYR", "NZD", "PHP", "SGD", "THB",
    "ZAR")


def convert_from_eur(target_currency, amount):
    return client.service.CrossConvert("EUR", target_currency, amount, HASHED_SOAP_KEY)


def convert_to_eur(input_currency, amount):
    return client.service.ConvertToEur(input_currency, amount, HASHED_SOAP_KEY)
