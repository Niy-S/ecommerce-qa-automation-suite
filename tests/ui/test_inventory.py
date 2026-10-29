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
