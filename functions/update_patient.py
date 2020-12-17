import http.client
import json
import logging
from uuid import uuid4
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_address_patches(patient, update_request):

    index, home_address = next(
        ((ix, addr) for ix, addr in enumerate(patient.get('address', [])) if addr['use'] == 'home'), (None, None)
    )
    new_address = update_request.get('address', {})
    if not home_address and not new_address:
        return []

    if not new_address:
        return [
            {
                "op": "remove",
                "path": f"/address/{index}"
            }
        ]

    if not home_address:
        return [
            {
                "op": "add",
                "path": "/address/-",
                "value": {
                    "use": "home",
                    'line':  new_address.get('lines', []),
                    'postalCode': new_address.get('postcode', '')
                }
            }
        ]

    new_lines = new_address.get('lines', [])
    new_postcode = new_address.get('postcode', '')
    existing_postcode = home_address.get('postalCode', '')
    existing_lines = home_address.get('line', [])

    patches = []
    if new_lines == existing_lines and new_postcode == existing_postcode:
        return patches

    if new_postcode != existing_postcode:
        patches.append(
            {
                "op": "replace",
                "path": f"/address/{index}/postalCode",
                "value": new_postcode
            }
        )
    # pad lines to  avoid index out of range
    padding = ['', '', '', '', '']
    new_lines = new_lines + padding
    existing_lines = existing_lines + padding

    for i in range(5):
        new_line = new_lines[i]
        existing_line = existing_lines[i]
        if new_line == existing_line:
            continue
        patches.append(
            {
                "op": "replace",
                "path": f"/address/{index}/line/{i}",
                "value": new_line
            }
        )

    return patches


def get_telecom_patches(patient, update_request):
    return []


def create_patient_response(patient):
    home_address = next((addr for addr in patient.get('address', []) if addr['use'] == 'home'), None)
    address = {
        "lines": [],
        "postcode": ""
    }
    if home_address:
        address['lines'] = home_address.get('line', [])
        address['postcode'] = home_address.get('postalCode', '')

    phones = [{'type': tel['use'], 'number': tel['value']} for tel in patient.get('telecom', [])]

    result = dict(address=address, tels=phones)
    return result


def lambda_handler(event=None, context=None):
    # TODO implement

    logging.info('update patient %s', event)
    body = str(event['body'])
    update_request = json.loads(body)

    conn = http.client.HTTPSConnection("sandbox.api.service.nhs.uk")
    conn.request("GET", "/personal-demographics/Patient/9000000009")
    res = conn.getresponse()

    if res.status != 200:
        return {
            'statusCode': res.status,
        }
    etag = res.headers.get('etag')
    patient = json.loads(res.read())

    address_patches = get_address_patches(patient, update_request) or []
    telecom_patches = get_telecom_patches(patient, update_request) or []

    if address_patches:
        logging.info('address changed')

    if telecom_patches:
        logging.info('tels changed')
    patches = address_patches + telecom_patches
    if not patches:
        logging.info('no changes')
        return {
            'statusCode': 304,
            'headers': {
                "Content-Type": "application/json"
            },
            'body': json.dumps(update_request)
        }

    conn.request(
        "PATCH", "/personal-demographics/Patient/9000000009",
        json.dumps({
            "patches": patches
        }),
        {
            'Content-Type': 'application/json',
            'If-Match': etag
        }
    )
    res = conn.getresponse()

    if res.status != 202:
        error = str(res.read())
        return {
            'statusCode': res.status,
            'body': error
        }

    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json"
        },
        'body': json.dumps(update_request)
    }
