from dotenv import load_dotenv
import distutils
import os
import requests
import json

#load_dotenv(verbose=True)

#ORIOLE_API_ROOT     = os.getenv('ORIOLE_API_ROOT')
#ORIOLE_API_USERNAME = os.getenv('ORIOLE_API_USERNAME')
#ORIOLE_API_PASSWORD = os.getenv('ORIOLE_API_PASSWORD')
#ORIOLE_API_TENANT   = os.getenv('ORIOLE_API_TENANT')

ORIOLE_API_ROOT     = "http://https://lara-test.library.jhu.edu"
ORIOLE_API_USERNAME = "diku_admin"
ORIOLE_API_PASSWORD = "admin"
ORIOLE_API_TENANT   = "diku"

#OKAPI_ENABLED = distutils.util.strtobool(os.getenv('OKAPI_ENABLED'))
OKAPI_ENABLED = True

headers = {'x-okapi-tenant': ORIOLE_API_TENANT, 'content-type': 'application/json'}
if OKAPI_ENABLED:
    print("1");
    payload = {'username': ORIOLE_API_USERNAME, 'password': ORIOLE_API_PASSWORD}
    response = requests.post(f'{ORIOLE_API_ROOT}/authn/login', data=json.dumps(payload), headers=headers, verify=False)
    headers['Authorization'] = f"Bearer {response.headers['x-okapi-token']}"
    print(str(headers))
