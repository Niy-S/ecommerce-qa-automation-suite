class CheckoutPage:
    def __init__(self, page):
        self.page = page
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_btn = page.locator('[data-test="continue"]')
        self.finish_btn = page.locator('[data-test="finish"]')
        self.error = page.locator('[data-test="error"]')
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.item_total = page.locator('[data-test="subtotal-label"]')
        self.tax = page.locator('[data-test="tax-label"]')
        self.total = page.locator('[data-test="total-label"]')

    def fill_info(self, first, last, zip_code):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(zip_code)
        self.continue_btn.click()
