import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def _prices(inventory):
    return [float(p.replace("$", "")) for p in inventory.prices.all_text_contents()]


def test_inventory_shows_six_products(inventory):
    expect(inventory.items).to_have_count(6)


@pytest.mark.parametrize("option", ["az", "lohi", "hilo"])
def test_sorting(inventory, option):
    expect(inventory.items).to_have_count(6)
    inventory.sort_by(option)

    if option == "az":
        names = inventory.item_names.all_text_contents()
        assert names == sorted(names)
    elif option == "lohi":
        prices = _prices(inventory)
        assert prices == sorted(prices)
    else:
        prices = _prices(inventory)
        assert prices == sorted(prices, reverse=True)


def test_sort_name_z_to_a(inventory):
    expect(inventory.items).to_have_count(6)
    inventory.sort_by("za")

    names = inventory.item_names.all_text_contents()
    assert names == sorted(names, reverse=True)
    assert names[0] == "Test.allTheThings() T-Shirt (Red)"
    assert names[-1] == "Sauce Labs Backpack"
