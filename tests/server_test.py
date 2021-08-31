from models.parking_slot import ParkingSlot
from flask.testing import FlaskClient
import pytest
import script
from modules.parking import resize_parking, parking_slots_size


@pytest.fixture
def client():
    script.app.config['TESTING'] = True
    with script.app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clean_test():
    resize_parking(50)


def clear_parking():
    resize_parking(parking_slots_size)


def test_server_connection(client: FlaskClient):
    r = client.get("/")
    assert b"Successful connection" in r.data


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


def test_authentication_succeeds(client: FlaskClient):
    r = authenticate(client, 'admin', 'AdminPassword')

    json = r.json
    assert r.status_code == 200 and 'key' in json


def test_authentication_fails_on_no_password(client: FlaskClient):
    r = authenticate(client, 'admin', '')
    assert r.status_code == 400 and 'password provided' in r.json['description']


def test_authentication_fails_on_no_username(client: FlaskClient):
    r = authenticate(client, '', 'AdminPassword')
    assert r.status_code == 400 and 'username provided' in r.json['description']


def test_authentication_fails_on_wrong_username(client: FlaskClient):
    r = authenticate(client, 'test', 'AdminPassword')
    assert r.status_code == 401 and 'unauthorized' in r.json['description']


def test_authentication_fails_on_wrong_password(client: FlaskClient):
    r = authenticate(client, 'admin', 'test')
    assert r.status_code == 401 and 'unauthorized' in r.json['description']


def test_authentication_fails_on_wrong_credentials(client: FlaskClient):
    r = authenticate(client, 'test1', 'test2')
    assert r.status_code == 401 and 'unauthorized' in r.json['description']


def test_unpark_succeeds(client: FlaskClient):
    auth_key = Auth.get_authentication_key(client)

    # First, park the car
    args = {
        'auth_key': auth_key,
        'license_plate': 'LP0'
    }
    r = client.get('/park', query_string=args)
    assert r.status_code == 200

    # Then unpark it
    r = client.get('/unpark', query_string=args)
    assert r.status_code == 200


def test_unpark_fails_on_malformed_request(client: FlaskClient):
    auth_key = Auth.get_authentication_key(client)

    args = {
        'auth_key': auth_key,
    }
    r = client.get('/unpark', query_string=args)
    assert r.status_code == 400


def test_unpark_fails_on_bad_authentication(client: FlaskClient):
    args = {
        'auth_key': 'test',
        'license_plate': 'LP1'
    }
    r = client.get('/unpark', query_string=args)
    assert r.status_code == 401


def test_unpark_fails_if_car_is_not_found(client: FlaskClient):
    args = {
        'auth_key': Auth.get_authentication_key(client),
        'license_plate': 'LP1'
    }
    r = client.get('/unpark', query_string=args)
    assert r.status_code == 404


def test_slot_succeeds(client: FlaskClient):
    auth_key = Auth.get_authentication_key(client)
    args = {
        'auth_key': auth_key,
        'license_plate': 'LP1'
    }

    r = client.get('/park', query_string=args)
    assert r.status_code == 200

    args = {
        'auth_key': auth_key,
        'number': 0
    }

    r = client.get('/slot', query_string=args)

    assert r.status_code == 200 and not r.json['is_empty'] and r.json[
        'slot_number'] == 0 and r.json['license_plate'] == 'LP1'


def test_slot_fails_on_malformed_request(client: FlaskClient):
    auth_key = Auth.get_authentication_key(client)

    args = {
        'auth_key': auth_key,
    }

    r = client.get('/slot', query_string=args)

    assert r.status_code == 400


def test_slot_fails_on_wrong_slot_numbers(client: FlaskClient):
    resize_parking(3)
    auth_key = Auth.get_authentication_key(client)
    args = {
        'auth_key': auth_key,
        'number': -1
    }
    r = client.get('/slot', query_string=args)
    assert r.status_code == 400 and 'number' in r.json['description']

    args['number'] = 3
    r = client.get('/slot', query_string=args)
    assert r.status_code == 400 and 'number' in r.json['description']


def test_slot_fails_on_bad_authentication(client: FlaskClient):
    args = {
        'auth_key': 'test',
    }
    r = client.get('/slot', query_string=args)
    assert r.status_code == 401

    del args['auth_key']
    r = client.get('/slot', query_string=args)
    assert r.status_code == 401
