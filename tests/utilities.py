from flask.testing import FlaskClient
from modules.parking import resize_parking, parking_slots_size
import script


def clear_parking():
    resize_parking(parking_slots_size)


def authenticate(client: FlaskClient, username, password):
    return client.post('/authenticate', data=dict(username=username, password=password))


class Auth:
    _currentKey = ""

    def get_authentication_key(client: FlaskClient) -> str:
        if Auth._currentKey != '':
            return Auth._currentKey

        auth_response = authenticate(client, 'admin', 'AdminPassword')
        decoded_json = auth_response.json

        assert 'key' in decoded_json
        Auth._currentKey = decoded_json['key']
        return decoded_json['key']
