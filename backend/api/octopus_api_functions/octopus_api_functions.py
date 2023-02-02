import requests
import os
import environ
import curlify # for debugging
from requests.auth import HTTPBasicAuth

# Import environment variables
env = environ.Env()
environ.Env.read_env()


def get_gas(from_date, to_date):
    MPRN = env('MPRN')
    GAS_METER_SERIAL_NUMBER = env('GAS_METER_SERIAL_NUMBER')
    API_KEY = env('API_KEY')

    url = f'https://api.octopus.energy/v1/gas-meter-points/{MPRN}/meters/{GAS_METER_SERIAL_NUMBER}/consumption'

    params = {
        'page_size': 100,
        'period_from': from_date,
        'period_to': to_date,
        'order_by': 'period',
        'group_by': 'day'
    }

    basic = HTTPBasicAuth(API_KEY, '')

    r = requests.get(url, params=params, auth=basic)
    if r.status_code != 200:
        raise ValueError(f'Request failed with status code {r.status_code}')

    
    return r.json()

def get_electric(from_date, to_date):
    MPAN = env('MPAN')
    ELECTRIC_METER_SERIAL_NUMBER = env('ELECTRIC_METER_SERIAL_NUMBER')
    API_KEY = env('API_KEY')

    url = f'https://api.octopus.energy/v1/electricity-meter-points/{MPAN}/meters/{ELECTRIC_METER_SERIAL_NUMBER}/consumption'

    params = {
        'page_size': 100,
        'period_from': from_date,
        'period_to': to_date,
        'order_by': 'period',
        'group_by': 'day'
    }

    basic = HTTPBasicAuth(API_KEY, '')

    r = requests.get(url, params=params, auth=basic)

    if r.status_code != 200:
        raise ValueError(f'Request failed with status code {r.status_code}')

    
    return r.json()

