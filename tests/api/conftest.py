import copy

import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"
TIMEOUT = 20

BOOKING_PAYLOAD = {
    "firstname": "Niyati",
    "lastname": "Sangharajka",
    "totalprice": 500,
    "depositpaid": True,
    "bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-05"},
    "additionalneeds": "Breakfast",
}


@pytest.fixture(scope="session")
def api_url():
    return BASE_URL


@pytest.fixture(scope="session")
def token(api_url):
    r = requests.post(
        f"{api_url}/auth",
        json={"username": "admin", "password": "password123"},
        timeout=TIMEOUT,
    )
    assert r.status_code == 200
    return r.json()["token"]


@pytest.fixture
def json_headers():
    return {"Accept": "application/json"}


@pytest.fixture
def auth_headers(token):
    return {"Cookie": f"token={token}", "Accept": "application/json"}


@pytest.fixture
def booking_payload():
    return copy.deepcopy(BOOKING_PAYLOAD)


@pytest.fixture
def created_booking(api_url, json_headers, auth_headers, booking_payload):
    """Creates a booking for the test, then deletes it afterwards."""
    r = requests.post(
        f"{api_url}/booking", json=booking_payload, headers=json_headers, timeout=TIMEOUT
    )
    assert r.status_code == 200
    booking_id = r.json()["bookingid"]
    yield {"id": booking_id, "payload": booking_payload}
    requests.delete(f"{api_url}/booking/{booking_id}", headers=auth_headers, timeout=TIMEOUT)
