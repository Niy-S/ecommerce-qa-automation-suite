class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page):
        self.page = page
        self.username = page.locator('[data-test="username"]')
        self.password = page.locator('[data-test="password"]')
        self.login_btn = page.locator('[data-test="login-button"]')
        self.error = page.locator('[data-test="error"]')

    def open(self):
        self.page.goto(self.URL)

    def login(self, user, pwd):
        self.username.fill(user)
        self.password.fill(pwd)
        self.login_btn.click()
