from tests.server_test import resize_parking, script, Auth, clear_parking
import pytest
from flask.testing import FlaskClient


@pytest.fixture
def client():
    script.app.config['TESTING'] = True
    with script.app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clean_test():
    resize_parking(50)


def test_parking_succeeds(client: FlaskClient):
    auth_key = Auth.get_authentication_key(client)
    args = {
        'auth_key': auth_key,
        'license_plate': 'LP0'
    }
    # Successfully park the car
    r = client.get('/park', query_string=args)
    assert r.status_code == 200


def test_parking_fails_on_malformed_request(client: FlaskClient):
    auth_key = Auth.get_authentication_key(client)
    # Malformed request
    args = {
        'auth_key': auth_key
    }
    r = client.get('/park', query_string=args)
    assert r.status_code == 400


def test_parking_fails_if_already_parked(client: FlaskClient):
    clear_parking()
    auth_key = Auth.get_authentication_key(client)
    args = {
        'auth_key': auth_key,
        'license_plate': 'LP0'
    }
    r = client.get('/park', query_string=args)
    assert r.status_code == 200
    r = client.get('/park', query_string=args)
    assert r.status_code == 403


def test_parking_fails_on_bad_authentication(client: FlaskClient):
    # Authentication errors
    args = {}
    r = client.get('/park', query_string=args)
    assert r.status_code == 401

    args = {
        'auth_key': 'test',
        'license_plate': '200'
    }
    r = client.get('/park', query_string=args)
    assert r.status_code == 401 and 'Wrong' in r.json['description']


def test_parking_fails_if_full(client: FlaskClient):
    resize_parking(1)

    auth_key = Auth.get_authentication_key(client)
    args = {
        'auth_key': auth_key,
        'license_plate': 'LP0'
    }

    # Successfully park the first time
    r = client.get('/park', query_string=args)
    assert r.status_code == 200

    args['license_plate'] = 'LP1'

    # The second time gets an error instead, given that no other spots are available
    r = client.get('/park', query_string=args)
    assert r.status_code == 404
