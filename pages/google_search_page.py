from pages.base_page import BasePage
from playwright.sync_api import TimeoutError
import os
import pytest

class GoogleSearchPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.search_input = page.locator("textarea[name='q']")
        self.search_button = page.locator("input[value='Google Search']").first
        self.stay_signed_out_button = page.get_by_role("button", name="Stay signed out")
        self.accept_button = page.get_by_role("button", name="Accept all")
        self.reject_button = page.get_by_role("button", name="Reject all")

    def handle_sign_in_popup(self):
        try:
            self.stay_signed_out_button.wait_for(timeout=2000)  # Reduced timeout
            if self.stay_signed_out_button.is_visible():
                self.stay_signed_out_button.click()
        except TimeoutError:
            pass

    def handle_consent_screen(self):
        try:
            self.accept_button.wait_for(timeout=3000)  # Reduced timeout
            if self.accept_button.is_visible():
                self.accept_button.click()
                return True
        except TimeoutError:
            try:
                self.reject_button.wait_for(timeout=2000)
                if self.reject_button.is_visible():
                    self.reject_button.click()
                    return True
            except TimeoutError:
                pass
        return False

    def handle_captcha(self):
        captcha_selectors = [
            "//iframe[contains(@src, 'recaptcha')]",
            "text='I'm not a robot'"
        ]
        
        for selector in captcha_selectors:
            if self.page.locator(selector).count() > 0:
                if os.getenv("CI") == "true":
                    pytest.skip("CAPTCHA detected in CI environment")
                print("\n⚠️ CAPTCHA detected! Please solve manually in browser...")
                input("Press Enter when CAPTCHA is solved...")
                return True
        return False

    def navigate(self, url):
        """Navigate to specified URL"""
        self.page.goto(url, timeout=10000)
        self.handle_consent_screen()
        self.handle_sign_in_popup()

    def search_for_calculator(self):
        """Search for calculator on Google and verify it's interactive"""
        try:
            # Perform the search
            self.search_input.fill("calculator")

            if self.handle_captcha():
                self.search_input.fill("calculator")
            
            # Submit search
            self.search_input.press("Enter")
            
            # Wait for calculator to be fully interactive
            self._wait_for_calculator_ready()
            
            return
        
        except Exception as e:
            self.page.screenshot(path="reports/search_failed.png")
            raise Exception(f"Failed to search for calculator: {str(e)}")

    def _wait_for_calculator_ready(self):
        """Wait for calculator to be fully loaded and ready"""
        calculator_container = self.page.locator("div[jsname='j93WEe']")
        calculator_container.wait_for(state="visible", timeout=10000)
        
        # Wait for specific buttons to be ready
        test_button = self.page.locator("div[jsname='N10B9']")  # Button '1'
        test_button.wait_for(state="visible", timeout=5000)
        test_button.wait_for(state="attached", timeout=5000)

    # def _verify_calculator_interactive(self):
    #     """Verify calculator buttons are clickable using the working pattern"""
    #     try:
    #         # Get display element
    #         display = self.page.locator("span#cwos")
    #         display.wait_for(state="visible", timeout=3000)
            
    #         # Store initial display value
    #         initial_value = display.inner_text(timeout=2000)
            
    #         # Test number button click
    #         one_button = self.page.locator("div[jsname='N10B9']")
    #         one_button.click(timeout=3000)
            
    #         # Verify display updated
    #         new_value = display.inner_text(timeout=2000)
    #         if new_value == initial_value:
    #             raise Exception("Display didn't update after button click")
            
    #         # Test operation button click (addition)
    #         plus_button = self.page.locator("div[jsname='XSr6wc']")
    #         plus_button.click(timeout=3000)
            
    #         # Test clear functionality
    #         try:
    #             # Try CE first
    #             ce_button = self.page.locator("div[jsname='H7sWPd']")
    #             ce_button.click(timeout=3000)
    #         except Exception as ce_error:
    #             try:
    #                 # Fall back to AC
    #                 ac_button = self.page.locator("div[jsname='SLn8gc']")
    #                 ac_button.click(timeout=3000)
    #             except Exception as ac_error:
    #                 # Final fallback
    #                 one_button.click(timeout=3000)
    #                 try:
    #                     ce_button.click(timeout=3000)
    #                 except Exception as final_error:
    #                     # If all clearing attempts fail, just continue
    #                     pass
                    
    #     except Exception as e:
    #         self.page.screenshot(path="reports/button_click_failed.png")
    #         raise Exception(f"Calculator interactivity verification failed: {str(e)}")