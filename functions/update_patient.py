import http.client
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event=None, context=None):
    # TODO implement

    logging.info('update patient %s', event)
    body = str(event['body'])
    update_request = json.loads(body)

    conn = http.client.HTTPSConnection("sandbox.api.service.nhs.uk")
    conn.request("GET", "/personal-demographics/Patient/9000000009")
    res = conn.getresponse()
    patient = json.loads(res.read())

    home_address = next((addr for addr in patient.get('address', []) if addr['use'] == 'home'), None)

    existing_postcode = home_address.get('postalCode', '')
    existing_lines = home_address.get('line', [])
    existing_phones = [{'type': tel['use'], 'number': tel['value']} for tel in patient.get('telecom', [])]

    new_address = update_request.get('address', {})
    new_lines = new_address.get('lines', [])
    new_postcode = new_address.get('postcode', '')
    new_phones = update_request.get('tels', [])

    address_changed = (existing_postcode != new_postcode or existing_lines != new_lines)
    if address_changed:
        logging.info('address changed')

    tels_changed = (existing_phones != new_phones)
    if tels_changed:
        logging.info('tels changed')

    if not (address_changed or tels_changed):
        logging.info('no changes')
        return {
            'statusCode': 304,
            'headers': {
                "Content-Type": "application/json"
            },
            'body': json.dumps(update_request)
        }

    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json"
        },
        'body': json.dumps(update_request)
    }
