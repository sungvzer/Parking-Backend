from tests.utilities import resize_parking, script, Auth
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
