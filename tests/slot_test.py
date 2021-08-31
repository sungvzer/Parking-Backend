from tests.utilities import resize_parking, script, Auth, clear_parking
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
