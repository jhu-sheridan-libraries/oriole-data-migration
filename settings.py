from dotenv import load_dotenv
import distutils
import os
import requests
import json

load_dotenv(verbose=True)

ORIOLE_API_ROOT     = os.getenv('ORIOLE_API_ROOT')
ORIOLE_API_USERNAME = os.getenv('ORIOLE_API_USERNAME')
ORIOLE_API_PASSWORD = os.getenv('ORIOLE_API_PASSWORD')
ORIOLE_API_TENANT   = os.getenv('ORIOLE_API_TENANT')

OKAPI_ENABLED = distutils.util.strtobool(os.getenv('OKAPI_ENABLED'))

SS_USERNAME = os.getenv('SERIAL_SOLUTIONS_USERNAME')
SS_PASSWORD = os.getenv('SERIAL_SOLUTIONS_PASSWORD')
SS_WSDL = os.getenv('SERIAL_SOLUTIONS_WSDL')
SS_LIBRARY_CODE = os.getenv('SERIAL_SOLUTIONS_LIBRARY_CODE')

def build_headers():
    headers={'x-okapi-tenant': ORIOLE_API_TENANT, 'content-type': 'application/json'}
    if OKAPI_ENABLED:
        payload = {'username': ORIOLE_API_USERNAME, 'password': ORIOLE_API_PASSWORD}
        response = requests.post(f'{ORIOLE_API_ROOT}/authn/login', data=json.dumps(payload), headers=headers, verify=False)
        headers['x-okapi-token'] = response.headers['x-okapi-token']
    return headers
