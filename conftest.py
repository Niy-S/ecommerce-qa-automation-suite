import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture
def login_page(page):
    lp = LoginPage(page)
    lp.open()
    return lp


@pytest.fixture
def inventory(page, login_page):
    login_page.login("standard_user", "secret_sauce")
    return InventoryPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)
