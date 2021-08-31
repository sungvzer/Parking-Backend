from tests.utilities import resize_parking, script, Auth, clear_parking, authenticate
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
