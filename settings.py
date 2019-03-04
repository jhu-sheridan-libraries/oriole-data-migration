from dotenv import load_dotenv
import distutils
import os

load_dotenv(verbose=True)

ORIOLE_API_ROOT     = os.getenv('ORIOLE_API_ROOT')
ORIOLE_API_USERNAME = os.getenv('ORIOLE_API_USERNAME')
ORIOLE_API_PASSWORD = os.getenv('ORIOLE_API_PASSWORD')
ORIOLE_API_TENANT   = os.getenv('ORIOLE_API_TENANT')

OKAPI_ENABLED = distutils.util.strtobool(os.getenv('OKAPI_ENABLED'))
