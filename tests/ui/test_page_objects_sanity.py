import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_page_objects_full_purchase_flow(inventory, cart_page, checkout_page):
    expect(inventory.title).to_have_text("Products")

    inventory.add_to_cart("sauce-labs-backpack")
    expect(inventory.cart_badge).to_have_text("1")

    inventory.open_cart()
    expect(cart_page.items).to_have_count(1)
    cart_page.checkout_btn.click()

    checkout_page.fill_info("Niyati", "Sangharajka", "400001")
    checkout_page.finish_btn.click()
    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")
