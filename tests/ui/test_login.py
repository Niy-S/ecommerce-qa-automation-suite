import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_valid_login(inventory):
    expect(inventory.title).to_have_text("Products")


def test_wrong_password_shows_error(login_page):
    login_page.login("standard_user", "wrong_password")
    expect(login_page.error).to_contain_text("do not match")


def test_locked_out_user_cannot_login(login_page):
    login_page.login("locked_out_user", "secret_sauce")
    expect(login_page.error).to_contain_text("locked out")


def test_empty_username_shows_error(login_page):
    login_page.login("", "secret_sauce")
    expect(login_page.error).to_contain_text("Username is required")


def test_empty_password_shows_error(login_page):
    login_page.login("standard_user", "")
    expect(login_page.error).to_contain_text("Password is required")


def test_logout_returns_to_login_page(inventory, login_page):
    inventory.logout()
    expect(login_page.login_btn).to_be_visible()
