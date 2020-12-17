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


def test_update_patient():
    get = get_patient()
    patient = json.loads(get['body'])
    event = get_event()
    patient['postcode'] = 'test'
    event['body'] = json.dumps(patient)
    event['body'] = json.dumps({"address": {"lines": ["1 Trevelyan Square", "Boar Lane", "City Centre", "Leeds", "West Yorkshire"], "postcode": "LS1 6AE"}, "tels": [{"type": "home", "number": "01632960587"}, {"type": "home", "number": "01632960587"}]})
    result = lambda_handler(event)
    actual = json.loads(result['body'])
    assert actual['postcode'] == 'test'
