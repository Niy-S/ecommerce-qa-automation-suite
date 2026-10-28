class CartPage:
    def __init__(self, page):
        self.page = page
        self.items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.checkout_btn = page.locator('[data-test="checkout"]')
        self.continue_shopping_btn = page.locator('[data-test="continue-shopping"]')

    def remove_item(self, slug):
        self.page.locator(f'[data-test="remove-{slug}"]').click()
