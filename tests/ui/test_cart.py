import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"
TSHIRT = "sauce-labs-bolt-t-shirt"


def test_add_single_item(inventory, cart_page):
    inventory.add_to_cart(BACKPACK)
    expect(inventory.cart_badge).to_have_text("1")

    inventory.open_cart()
    expect(cart_page.items).to_have_count(1)
    expect(cart_page.item_names).to_have_text("Sauce Labs Backpack")


def test_add_multiple_items_updates_badge(inventory, cart_page):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    inventory.add_to_cart(TSHIRT)
    expect(inventory.cart_badge).to_have_text("3")

    inventory.open_cart()
    expect(cart_page.items).to_have_count(3)


def test_remove_item_from_inventory_page(inventory):
    inventory.add_to_cart(BACKPACK)
    expect(inventory.cart_badge).to_have_text("1")

    inventory.remove_from_cart(BACKPACK)
    expect(inventory.cart_badge).to_have_count(0)


def test_remove_item_from_cart_page(inventory, cart_page):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    inventory.open_cart()

    cart_page.remove_item(BACKPACK)
    expect(cart_page.items).to_have_count(1)
    expect(cart_page.item_names).to_have_text("Sauce Labs Bike Light")


def test_cart_persists_after_navigation_and_reload(page, inventory, cart_page):
    inventory.add_to_cart(BACKPACK)
    inventory.open_cart()
    cart_page.continue_shopping_btn.click()
    expect(inventory.cart_badge).to_have_text("1")

    page.reload()
    expect(inventory.cart_badge).to_have_text("1")
