import script
import pytest
from flask.testing import FlaskClient
from modules.parking import resize_parking, parking_slots_size


@pytest.fixture
def client():
    script.app.config['TESTING'] = True
    with script.app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clean_test():
    resize_parking(50)


def test_server_connection(client: FlaskClient):
    r = client.get("/")
    assert b"Successful connection" in r.data
