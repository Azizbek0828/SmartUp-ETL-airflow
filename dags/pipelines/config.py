import json
import base64

ENDPOINTS = {
    'inventory': 'https://smartup.online/b/anor/mxsx/mr/inventory$export',
    'legal_person': 'https://smartup.online/b/anor/mxsx/mr/legal_person$export',
    'natural_person': 'https://smartup.online/b/anor/mxsx/mr/natural_person$export',
    'order': 'https://smartup.online/b/trade/txs/tdeal/order$export'
}

## db_url

#
with open('auth.json', 'r') as file:
    data = json.load(file)

PROJECT_CODE = data['PROJECT_CODE']
FILIAL_ID    = data['FILIAL_ID']
username = data['username']
password = data['password']
db_url = data['db_url']

def get_headers():
    token = base64.b64encode(
        f"{username}:{password}".encode()
    ).decode()

    header = {
    "Authorization": f"Basic {token}",
    "project_code": PROJECT_CODE,
    "filial_id":    FILIAL_ID,
    }

    return header


get_headers()