from pages.base_page import BasePage
from playwright.sync_api import expect

class CalculatorPage(BasePage):
    BUTTONS = {
        # Numbers
        '0': "div[jsname='bkEvMb']",
        '1': "div[jsname='N10B9']",
        '2': "div[jsname='lVjWed']",
        '3': "div[jsname='KN1kY']",
        '4': "div[jsname='xAP7E']",
        '5': "div[jsname='Ax5wH']",
        '6': "div[jsname='abcgof']",
        '7': "div[jsname='rk7bOd']",
        '8': "div[jsname='T7PMFe']",
        '9': "div[jsname='XoxYJ']",
        
        # Basic Operations
        '+': "div[jsname='XSr6wc']",
        '-': "div[jsname='pPHzQc']",
        '×': "div[jsname='YovRWb']",
        '÷': "div[jsname='WxTTNd']",
        '=': "div[jsname='Pt8tGc']",
        
        # Other buttons
        '.': "div[jsname='YrdHyf']",
        'AC': "div[jsname='SLn8gc']",
        'CE': "div[jsname='H7sWPd']",
        '%': "div[jsname='F0gbu']",
    }
    
    def __init__(self, page):
        super().__init__(page)
        self.display = page.locator("span#cwos")
        
    def verify_calculator_ready(self):
        """Verify calculator buttons are present and clickable"""
        try:
            # Check a sample of buttons
            test_buttons = ['1', '5', '9', '+', '-', '×', '÷', '=']
            
            for button in test_buttons:
                btn = self.page.locator(self.BUTTONS[button])
                expect(btn).to_be_visible(timeout=2000)
                expect(btn).to_be_enabled(timeout=2000)
                
            # Verify display is present
            expect(self.display).to_be_visible(timeout=2000)
            
            return True
        except Exception as e:
            self.page.screenshot(path="reports/calculator_not_ready.png")
            raise Exception(f"Calculator buttons not available: {str(e)}")

    def click_button(self, button):
        """Universal reliable button click with enhanced error handling"""
        if button not in self.BUTTONS:
            raise ValueError(f"Button '{button}' not found")
        
        try:
            btn = self.page.locator(self.BUTTONS[button])
            
            # Special pre-click activation for AC button
            if button == 'AC':
                try:
                    btn.click(timeout=5000, force=True)
                except:
                    # If direct AC fails, activate calculator first
                    self.page.locator(self.BUTTONS['1']).click(timeout=3000)
                    btn.click(timeout=5000, force=True)
            else:
                btn.click(timeout=5000, force=True)
            
            # Verify number buttons
            if button in '0123456789':
                current_value = self.get_display_value()
                if button not in current_value:
                    raise Exception(f"Button press not registered. Display: {current_value}")
                    
        except Exception as e:
            self.page.screenshot(path=f"reports/click_failed_{button}.png")
            raise Exception(f"Failed to click {button}: {str(e)}")

    def get_display_value(self):
        """Get the current calculator display value"""
        try:
            expect(self.display).to_be_visible(timeout=1500)
            return self.display.inner_text()
        except Exception as e:
            self.page.screenshot(path="reports/display_read_failed.png")
            raise Exception(f"Failed to read display: {str(e)}")
            
    def perform_calculation(self, expression):
        """Perform calculation and return result (without assertions)"""
        try:
            # Clear calculator first
            self.click_clear_button('CE')

            # Enter each character
            for char in expression:
                self.click_button(char)
                                
            return self.get_display_value()
            
        except Exception as e:
            self.page.screenshot(path="reports/operation_failed.png")
            raise Exception(f"Calculation failed: {str(e)}")
    
    def assert_result(self, expected):
        """Assert the current display matches expected value"""
        current_value = self.get_display_value()
        assert current_value == expected, f"Expected {expected}, got {current_value}"
    
    def clear_entry(self):
        """Clear last entry using CE button"""
        ce_button = self.page.locator(self.BUTTONS['CE'])
        ce_button.click(timeout=3000)
        
    def click_clear_button(self, button_type='CE'):
        """Click either CE or AC button normally"""
        if button_type not in ['CE', 'AC']:
            raise ValueError("button_type must be either 'CE' or 'AC'")
        
        try:
            btn = self.page.locator(self.BUTTONS[button_type])
            btn.click(timeout=5000)
        except Exception as e:
            self.page.screenshot(path=f"reports/{button_type}_click_failed.png")
            raise Exception(f"Failed to click {button_type} button: {str(e)}")

    def long_press_clear_button(self, button_type='CE'):
        """Long press (1 second) either CE or AC button"""
        if button_type not in ['CE', 'AC']:
            raise ValueError("button_type must be either 'CE' or 'AC'")
        
        try:
            btn = self.page.locator(self.BUTTONS[button_type])
            btn.click(timeout=5000, delay=1000)  # 1000ms = 1 second press
        except Exception as e:
            self.page.screenshot(path=f"reports/{button_type}_long_press_failed.png")
            raise Exception(f"Failed to long press {button_type} button: {str(e)}")