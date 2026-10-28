from playwright.sync_api import expect

def test_site_loads(page):
    page.goto("https://www.saucedemo.com")
    expect(page).to_have_title("Swag Labs")
