#!/usr/bin/env python3

import settings
import requests
import bisect
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# This script add the tag 'Biomedical Sciences – Core Databases' to databases.

# Usage:
# In the oriole-data-migration directory, run
# pipenv run python ./update_bm.py

headers = settings.build_headers()
url = f"{settings.ORIOLE_API_ROOT}/oriole/resources"
lines = [line.rstrip('\n') for line in open('data/biomedical_databases_test.csv')]
lines = list(filter(None, lines))
for jhu_id in lines:
    query_string = {"query": f"altId=={jhu_id}"}
    response = requests.request("GET", url, headers=headers, params=query_string, verify=False)
    if response.status_code != 200:
        print(f"[GET request failed]: {response.text}, {jhu_id}")
        continue
    data = response.json()
    if data['resultInfo']['totalRecords'] != 1:
        print(f"[request error]: found {data['resultInfo']['totalRecords']} instead of 1. {jhu_id}")
        continue
    record = data['resources'][0]
    if 'Biomedical Sciences – Core Databases' in record['tags']['tagList']:
        record['tags']['tagList'].remove('Biomedical Sciences – Core Databases')
    if 'Biomedical Sciences -- Core Databases' not in record['tags']['tagList']:
        bisect.insort(record['tags']['tagList'], 'Biomedical Sciences -- Core Databases')
    # Post record
    put_url = f"{url}/{record['id']}"
    response = requests.request("PUT", put_url, headers=headers, data=json.dumps(record), verify=False)
    if response.status_code != 204:
        print(f"[PUT request failed]: {response.text}, {jhu_id}")

