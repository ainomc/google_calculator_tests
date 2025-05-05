from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 10000

    def wait_for_selector(self, selector, timeout=None):
        self.page.wait_for_selector(selector, timeout=timeout or self.timeout)

    def take_screenshot(self, name):
        self.page.screenshot(path=f"reports/screenshots/{name}.png", full_page=True)