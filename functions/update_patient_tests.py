import json

from update_patient import lambda_handler
from get_patient import lambda_handler as get_patient

def get_event():
  return {
    'version': '2.0',
    'routeKey': 'POST /test',
    'rawPath': '/test',
    'rawQueryString': '',
    'headers': {
        'accept': '*/*',
        'content-length': '16',
        'content-type': 'application/json',
        'host': 'yjoz8bsx1k.execute-api.us-east-1.amazonaws.com',
        'user-agent': 'curl/7.68.0',
        'x-amzn-trace-id': 'Root=1-5fdb76e9-58fb425b5535cf1875b3b678',
        'x-forwarded-for': '86.175.70.114',
        'x-forwarded-port': '443',
        'x-forwarded-proto': 'https'
    },
    'requestContext': {
        'accountId': '148765512092',
        'apiId': 'yjoz8bsx1k',
        'domainName': 'yjoz8bsx1k.execute-api.us-east-1.amazonaws.com',
        'domainPrefix': 'yjoz8bsx1k',
        'http': {
            'method': 'POST',
            'path': '/test',
            'protocol': 'HTTP/1.1',
            'sourceIp': '86.175.70.114',
            'userAgent': 'curl/7.68.0'
        }, 'requestId': 'Xs-EijwSIAMEM-w=',
        'routeKey': 'POST /test', 'stage': '$default', 'time': '17/Dec/2020:15:19:05 +0000', 'timeEpoch': 1608218345745
    },
    'body': '{"test": "data"}',
    'isBase64Encoded': False
}

def test_update_patient_nochanges():
    get = get_patient()
    patient = json.loads(get['body'])
    event = get_event()
    event['body'] = json.dumps(patient)
    result = lambda_handler(event)
    assert result['statusCode'] == 304


def test_update_postcode():
    get = get_patient()
    patient = json.loads(get['body'])
    event = get_event()
    current_postcode = patient['address']['postcode']
    new_postcode = 'WF1 2JJ' if current_postcode != 'WF1 2JJ' else 'LS1 4JL'
    patient['address']['postcode'] = 'WF1 2JJ' if current_postcode != 'WF1 2JJ' else 'LS1 4JL'
    event['body'] = json.dumps(patient)
    result = lambda_handler(event)
    assert result['statusCode'] == 200
    actual = json.loads(result['body'])
    assert actual['address']['postcode'] == new_postcode


def test_update_patient_address():
    get = get_patient()
    patient = json.loads(get['body'])
    event = get_event()
    line_0 = patient['address']['lines'][0]
    new_line_0 = 'fake1' if line_0 != 'fake1' else 'fake2'
    patient['address']['lines'][0] = new_line_0
    event['body'] = json.dumps(patient)
    result = lambda_handler(event)
    assert result['statusCode'] == 200
    actual = json.loads(result['body'])
    assert actual['address']['lines'][0] == new_line_0
