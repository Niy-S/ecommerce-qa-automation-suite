import pytest
import requests

pytestmark = pytest.mark.api

TIMEOUT = 20


def test_health_check(api_url):
    r = requests.get(f"{api_url}/ping", timeout=TIMEOUT)
    assert r.status_code == 201  # this API returns 201 for a healthy ping


def test_auth_with_valid_credentials_returns_token(api_url):
    r = requests.post(
        f"{api_url}/auth",
        json={"username": "admin", "password": "password123"},
        timeout=TIMEOUT,
    )
    assert r.status_code == 200
    assert r.json().get("token")


def test_auth_with_bad_credentials_is_rejected(api_url):
    r = requests.post(
        f"{api_url}/auth",
        json={"username": "admin", "password": "wrong-password"},
        timeout=TIMEOUT,
    )
    # Quirk: this API answers 200 but returns a reason instead of a token
    body = r.json()
    assert "token" not in body
    assert body["reason"] == "Bad credentials"


def test_create_booking(api_url, json_headers, auth_headers, booking_payload):
    r = requests.post(
        f"{api_url}/booking", json=booking_payload, headers=json_headers, timeout=TIMEOUT
    )
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body["bookingid"], int)
    assert body["booking"] == booking_payload

    # cleanup
    requests.delete(
        f"{api_url}/booking/{body['bookingid']}", headers=auth_headers, timeout=TIMEOUT
    )


def test_get_booking_by_id(api_url, json_headers, created_booking):
    r = requests.get(
        f"{api_url}/booking/{created_booking['id']}", headers=json_headers, timeout=TIMEOUT
    )
    assert r.status_code == 200
    assert r.json() == created_booking["payload"]


def test_get_all_bookings_includes_created_booking(api_url, json_headers, created_booking):
    r = requests.get(f"{api_url}/booking", headers=json_headers, timeout=TIMEOUT)
    assert r.status_code == 200
    ids = [b["bookingid"] for b in r.json()]
    assert created_booking["id"] in ids


def test_full_update_with_token(api_url, auth_headers, created_booking):
    updated = {**created_booking["payload"], "firstname": "Updated", "totalprice": 999}
    r = requests.put(
        f"{api_url}/booking/{created_booking['id']}",
        json=updated,
        headers=auth_headers,
        timeout=TIMEOUT,
    )
    assert r.status_code == 200
    assert r.json()["firstname"] == "Updated"
    assert r.json()["totalprice"] == 999

    # verify the change was really saved
    check = requests.get(
        f"{api_url}/booking/{created_booking['id']}", headers=auth_headers, timeout=TIMEOUT
    )
    assert check.json()["firstname"] == "Updated"


def test_partial_update_changes_only_sent_field(api_url, auth_headers, created_booking):
    r = requests.patch(
        f"{api_url}/booking/{created_booking['id']}",
        json={"lastname": "Patched"},
        headers=auth_headers,
        timeout=TIMEOUT,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["lastname"] == "Patched"
    assert body["firstname"] == created_booking["payload"]["firstname"]


def test_delete_booking_then_get_returns_404(api_url, auth_headers, created_booking):
    r = requests.delete(
        f"{api_url}/booking/{created_booking['id']}", headers=auth_headers, timeout=TIMEOUT
    )
    assert r.status_code == 201  # quirk: delete returns 201 Created

    check = requests.get(f"{api_url}/booking/{created_booking['id']}", timeout=TIMEOUT)
    assert check.status_code == 404
