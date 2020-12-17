
from get_patient import lambda_handler

def test_get_patient():
    result =  lambda_handler()

    print(result)
