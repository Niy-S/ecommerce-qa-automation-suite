class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.prices = page.locator('[data-test="inventory-item-price"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.menu_btn = page.locator('#react-burger-menu-btn')
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')

    def add_to_cart(self, slug):
        self.page.locator(f'[data-test="add-to-cart-{slug}"]').click()

    def remove_from_cart(self, slug):
        self.page.locator(f'[data-test="remove-{slug}"]').click()

    def sort_by(self, value):  # "az", "za", "lohi", "hilo"
        self.sort_dropdown.select_option(value)

    def open_cart(self):
        self.page.locator('[data-test="shopping-cart-link"]').click()

    def logout(self):
        self.menu_btn.click()
        self.logout_link.click()
