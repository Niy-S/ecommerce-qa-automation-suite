import re
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


@pytest.fixture
def at_checkout_info(inventory, cart_page):
    """Logged in, backpack in cart, sitting on the checkout information form."""
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.open_cart()
    cart_page.checkout_btn.click()


def _money(text):
    return float(re.search(r"\$([\d.]+)", text).group(1))


def test_successful_checkout(at_checkout_info, checkout_page):
    checkout_page.fill_info("Niyati", "Sangharajka", "400001")
    checkout_page.finish_btn.click()
    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")


@pytest.mark.parametrize(
    "first, last, zip_code, expected_error",
    [
        ("", "Sangharajka", "400001", "First Name is required"),
        ("Niyati", "", "400001", "Last Name is required"),
        ("Niyati", "Sangharajka", "", "Postal Code is required"),
    ],
    ids=["missing-first-name", "missing-last-name", "missing-postal-code"],
)
def test_checkout_required_field_validation(
    at_checkout_info, checkout_page, first, last, zip_code, expected_error
):
    checkout_page.fill_info(first, last, zip_code)
    expect(checkout_page.error).to_contain_text(expected_error)


def test_order_total_equals_item_total_plus_tax(at_checkout_info, checkout_page):
    checkout_page.fill_info("Niyati", "Sangharajka", "400001")

    item_total = _money(checkout_page.item_total.inner_text())
    tax = _money(checkout_page.tax.inner_text())
    total = _money(checkout_page.total.inner_text())

    assert total == pytest.approx(item_total + tax, abs=0.01)
