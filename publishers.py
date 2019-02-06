#!/usr/bin/env python3

# This script extracts publishers from the xml exported from Xerxes MySQL

# Usage:
# In the /data directory, run
# ../scripts/load.py

import xml.etree.ElementTree as ET
import csv
import settings

tree = ET.parse('data/data.xml')
root = tree.getroot()

# Read DB data
db_data = []

def extract_text(root, tag):
    elem = root.find(tag)
    return elem.text if elem is not None else ''

for child in root:
    title_elem = child.find('title_display')
    if title_elem is None:
        title_elem = child.find('title_full')
    title = title_elem.text if title_elem is not None else ''

    jhu_id = extract_text(child, 'metalib_id')
    url = extract_text(child, 'link_native_home')
    publisher = extract_text(child, 'publisher')
    creator = extract_text(child, 'creator')

    if title == '' and url == '':
        print(f'ID {jhu_id}: no title and url.')
    else:
        payload = {'id': jhu_id, 'title': title, 'url': url, 'publisher': publisher, 'creator': creator}
        db_data.append(payload)

with open('data/publishers.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, ['id', 'title', 'url', 'publisher', 'creator'])
    writer.writeheader()
    for payload in db_data:
        writer.writerow(payload)
