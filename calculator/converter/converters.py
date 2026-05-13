import requests
import json
import os
from datetime import datetime, timedelta


# КОНВЕРТАЦИЯ ДЛИНЫ
def convert_length(value, from_unit, to_unit):
    to_meters = {
        'm': 1,
        'km': 1000,
        'cm': 0.01,
        'mm': 0.001,
        'mile': 1609.344,
        'ft': 0.3048,
        'in': 0.0254
    }

    meters = value * to_meters[from_unit]
    result = meters / to_meters[to_unit]
    return result


# КОНВЕРТАЦИЯ ВЕСА
def convert_weight(value, from_unit, to_unit):
    to_kg = {
        'kg': 1,
        'g': 0.001,
        'mg': 0.000001,
        'lb': 0.453592,
        'oz': 0.0283495,
        't': 1000
    }

    kg = value * to_kg[from_unit]
    result = kg / to_kg[to_unit]
    return result


# КОНВЕРТАЦИЯ ТЕМПЕРАТУРЫ
def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'c':
        celsius = value
    elif from_unit == 'f':
        celsius = (value - 32) * 5 / 9
    elif from_unit == 'k':
        celsius = value - 273.15
    else:
        celsius = value

    if to_unit == 'c':
        return celsius
    elif to_unit == 'f':
        return celsius * 9 / 5 + 32
    elif to_unit == 'k':
        return celsius + 273.15
    else:
        return celsius


# КОНВЕРТАЦИЯ ВАЛЮТ
_currency_cache = {
    'rates': {},
    'timestamp': None,
    'available': ['USD', 'EUR', 'RUB', 'GBP', 'CNY', 'JPY', 'CHF', 'CAD', 'AUD', 'TRY']
}


def get_available_currencies():
    return _currency_cache['available']


def _fetch_currency_rates():
    if _currency_cache['timestamp']:
        if datetime.now() - _currency_cache['timestamp'] < timedelta(hours=1):
            return _currency_cache['rates']

    try:
        url = "https://api.frankfurter.app/latest?from=USD"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            _currency_cache['rates'] = data['rates']
            _currency_cache['timestamp'] = datetime.now()

            all_currencies = list(data['rates'].keys())
            all_currencies.append('USD')
            all_currencies.sort()
            _currency_cache['available'] = all_currencies

            return _currency_cache['rates']
    except:
        pass

    return {
        'EUR': 0.92, 'RUB': 88.5, 'GBP': 0.79, 'CNY': 7.24,
        'JPY': 148.2, 'CHF': 0.91, 'CAD': 1.35, 'AUD': 1.52, 'TRY': 32.1
    }


def convert_currency(value, from_currency, to_currency):
    if from_currency == to_currency:
        return value

    rates = _fetch_currency_rates()

    if from_currency == 'USD':
        usd_amount = value
    else:
        if from_currency in rates:
            usd_amount = value / rates[from_currency]
        else:
            usd_amount = value

    if to_currency == 'USD':
        return usd_amount
    else:
        if to_currency in rates:
            return usd_amount * rates[to_currency]
        else:
            return value