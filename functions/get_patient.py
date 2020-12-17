import http.client
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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

    logging.info('get patient %s', event)

    conn = http.client.HTTPSConnection("sandbox.api.service.nhs.uk")
    conn.request("GET", "/personal-demographics/Patient/9000000009")
    res = conn.getresponse()

    if res.status != 200:
        return {
            'statusCode': res.status,
        }

    patient = json.loads(res.read())

    return {
        'statusCode': res.status,
        'headers': {
            "Content-Type": "application/json"
        },
        'body': json.dumps(create_patient_response(patient))
    }
