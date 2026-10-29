import pytest
import requests

pytestmark = pytest.mark.api

TIMEOUT = 20


def test_get_nonexistent_booking_returns_404(api_url):
    r = requests.get(f"{api_url}/booking/99999999", timeout=TIMEOUT)
    assert r.status_code == 404


def test_update_without_token_is_forbidden(api_url, json_headers, created_booking):
    r = requests.put(
        f"{api_url}/booking/{created_booking['id']}",
        json=created_booking["payload"],
        headers=json_headers,
        timeout=TIMEOUT,
    )
    assert r.status_code == 403


def test_update_with_invalid_token_is_forbidden(api_url, created_booking):
    headers = {"Cookie": "token=not-a-real-token", "Accept": "application/json"}
    r = requests.put(
        f"{api_url}/booking/{created_booking['id']}",
        json=created_booking["payload"],
        headers=headers,
        timeout=TIMEOUT,
    )
    assert r.status_code == 403


def test_delete_without_token_is_forbidden(api_url, created_booking):
    r = requests.delete(f"{api_url}/booking/{created_booking['id']}", timeout=TIMEOUT)
    assert r.status_code == 403

    # the booking must still exist after the rejected delete
    check = requests.get(f"{api_url}/booking/{created_booking['id']}", timeout=TIMEOUT)
    assert check.status_code == 200


@pytest.mark.parametrize(
    "missing_field",
    ["firstname", "lastname", "totalprice"],
    ids=["no-firstname", "no-lastname", "no-totalprice"],
)
def test_create_booking_with_missing_required_field_fails(
    api_url, json_headers, booking_payload, missing_field
):
    del booking_payload[missing_field]
    r = requests.post(
        f"{api_url}/booking", json=booking_payload, headers=json_headers, timeout=TIMEOUT
    )
    assert r.status_code >= 400
