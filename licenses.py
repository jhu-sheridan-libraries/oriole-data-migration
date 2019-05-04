#!/usr/bin/env python3

# This script load the licenses from Serial Solutions 360 ERM
# Usage:
#
# In the oriole-data-migration folder, run
# pipenv run python ./licenses.py

import settings
from zeep import Client
from zeep.wsse.username import UsernameToken
import json
import pickle
import requests
import uuid
from datetime import datetime
from random import choice
from string import ascii_lowercase, digits
import sys

if len(sys.argv) == 2 and sys.argv[1] == 'dump':
    client = Client(settings.SS_WSDL)

    req_data = {
        'LibraryCode': settings.SS_LIBRARY_CODE,
        'UserName': settings.SS_USERNAME,
        'Password': settings.SS_PASSWORD
    }

    data = client.service.LicenseData(request=req_data)
    pickle.dump(data, open('data/licenses.pickle', 'wb'))
    sys.exit(0)

# {
#   "id": "2c91808c6a7a80d7016a7a8cf0b80017",
#   "dateCreated": "2019-05-02T21:56:58Z",
#   "links": [],
#   "customProperties": {},
#   "tags": [],
#   "lastUpdated": "2019-05-02T21:56:58Z",
#   "endDate": "2019-05-31T00:00:00Z",
#   "startDate": "2019-05-03T00:00:00Z",
#   "docs": [],
#   "name": "Test",
#   "orgs": [],
#   "type": {
#     "id": "2c91808c6a7a80d7016a7a81fded0008",
#     "value": "local",
#     "label": "Local"
#   },
#   "status": {
#     "id": "2c91808c6a7a80d7016a7a81fe2d000f",
#     "value": "active",
#     "label": "Active"
#   },
#   "supplementaryDocs": [],
#   "description": "test",
#   "_links": {
#     "linkedResources": {
#       "href": "/licenses/licenseLinks?filter=owner.id%3d2c91808c6a7a80d7016a7a8cf0b80017"
#     }
#   },
#   "openEnded": false
# }
# post to /licenses
headers = settings.build_headers()
data = pickle.load(open('data/licenses.pickle', 'rb'))

types = {
    'Consortial': {
        "id": "2c91808c6a7a80d7016a7a81fdf50009",
        "value": "consortial",
        "label": "Consortial"
    },
    'Negotiated': {
        "id": "2c91808c6a7a80d7016a7a81fe0d000b",
        "value": "negotiated",
        "label": "Negotiated"
    },
    'License not required': {
        "id": "2c91808c6a7a80d7016a7a81fdfe000a",
        "value": "license_not_required",
        "label": "License not required"
    },
    'Click-Through': {
        "id": "2c91808c6a7a80d7016a7a81fded0008",
        "value": "click_through",
        "label": "Click-Through"
    },
    None: {
        "id": "2c91808c6a7a80d7016a7a81fdce0004",
        "value": "none",
        "label": "None"
    }
}

statuses = {
    'Active': {
        "id": "2c91808c6a7a80d7016a7a81fe2d000f",
        "value": "active",
        "label": "Active"
    },
    'Pending': {
        "id": "2c91808c6a7a80d7016a7a81fe26000e",
        "value": "pending",
        "label": "Pending"
    },
    'Retired': {
        "id": "2c91808c6a7a80d7016a7a81fe3a0011",
        "value": "retired",
        "label": "Retired"
    },
    None: {
        "id": "2c91808c6a7a80d7016a7a81fe1a000d",
        "value": "none",
        "label": "None"
    }
}

# types: {'License not required', 'Negotiated', 'Click-Through', 'Consortial', None}
# statuses: {'Active', 'Retired', None, 'Pending'}

api_url = f'{settings.ORIOLE_API_ROOT}/licenses/licenses'
for license in data:
    id = ''.join(choice(ascii_lowercase+digits) for i in range(32))
    name = license['LicenseName']['Content']
    ss_id = license['LicenseId']['Content']
    type = license['Type']['Content']
    status = license['Status']['Content']
    terms = license['LicenseTerms']

    customProperties = {}
    authorizedUsers = terms['AuthorizedUsers']['Content']
    if (authorizedUsers is not None):
        customProperties['authorizedUsers'] = authorizedUsers['string']
    customProperties['authorizedUsersNote'] = terms['AuthorizedUsersNote']['Content']
    customProperties['iLLRecordKeepingNote'] = terms['ILLRecordKeepingNote']['Content']

    payload = {
        'id': id,
        'name': license['LicenseName']['Content'],
        'dateCreated': str(datetime.now()),
        'lastUpdated': str(datetime.now()),
        'type': types[type],
        'status': statuses[status],
        'description': '',
        'openEnded': False,
        'customProperties': customProperties,
        'orgs': {},
        'docs': [],
        'supplementaryDocs': [],
        "tags": [],
        "description": license['LicenseNote']['Content']
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload), verify=False)
    if response.status_code != 201:
        print(response.status_code, response.text)
