import json

import requests
from jose import jwt


class ApiError(Exception):
    def __init__(self, status, content=None):
        self.status = status
        self.content = content

    def __str__(self):
        err_str = "API call failed: {}".format(self.status)

        if self.content:
            err_str += " " + self.content

        return repr(err_str)


def client(application_id, key_location):
    """Creates a new vapi client from the given application id and key file
    location.
    """
    key = None
    with open(key_location, "r") as f:
        key = f.read()

    return ApiClient(application_id, key)


class ApiClient(object):
    BASE_URL = 'http://api.nexmo.com/v1/calls'

    def __init__(self, application_id, key):
        if not application_id:
            raise ValueError('you need to specify an application_id')
        if not key:
            raise ValueError('you need to specify an key')

        self.application_id = application_id
        self.key = key

    def transfer_call(self, call_id, ncco_url):
        url = ApiClient.BASE_URL + '/' + call_id

        payload = {
            "action": "transfer",
            "destination": {
                "type": "ncco",
                "url": [ncco_url]
            }
        }

        jwt = self._generate_jwt()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(jwt)
        }

        response = requests.put(url, data=json.dumps(payload), headers=headers)

        if (response.status_code != 200):
            raise ApiError(status=200, content=response.content)

    def _generate_jwt(self):
        claims = {
            'application_id': self.application_id
        }
        return jwt.encode(claims, self.key, algorithm='RS256')
