import pytest

@pytest.fixture
def setup(page):
    from pages.google_search_page import GoogleSearchPage
    from pages.calculator_page import CalculatorPage
    
    search_page = GoogleSearchPage(page)
    calculator_page = CalculatorPage(page)
    
    # Navigate and search with retries
    max_attempts = 1
    for attempt in range(max_attempts):
        try:
            search_page.navigate("https://www.google.com")
            search_page.search_for_calculator()
            
            # Verify calculator is ready
            calculator_page.verify_calculator_ready()
            
            # Clear calculator before tests
            calculator_page.click_clear_button('AC')
            # time.sleep(0.5)
            
            return calculator_page
            
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            page.reload()
            # time.sleep(2)

@pytest.mark.parametrize("expression,expected", [
    ("2+3=", "5"),
    ("5-2=", "3"),
    ("4×3=", "12"),
    ("8÷2=", "4"),
    ("1.5+2.5=", "4"),
    ("10÷2+3×4-5=", "12")
])
def test_arithmetic_operations(setup, expression, expected):
    calc = setup
    result = calc.perform_calculation(expression)
    calc.assert_result(expected)

def test_clear_functionality(setup):
    calc = setup
    
    # Test normal CE click (clears last entry)
    calc.click_button('1')
    calc.click_button('2')
    calc.click_button('3')
    calc.click_clear_button('CE')  # Normal click
    assert calc.get_display_value() == "12", "CE should remove last digit"
    
    # Test long press CE (full clear)
    calc.long_press_clear_button('CE')  # Long click
    assert calc.get_display_value() == "0", "CE should fully clear"
    
    # Test normal CE click(clears last digit from expression)
    calc.click_button('4')
    calc.click_button('-')
    calc.click_button('6')
    calc.click_clear_button('CE')  # Normal click
    assert calc.get_display_value() == "4 -", "Long CE press left first digit and operand"
    
    # Test long press CE (extra assurance)
    calc.click_button('7')
    calc.click_button('+')
    calc.click_button('9')
    calc.long_press_clear_button('CE')  # Long press
    assert calc.get_display_value() == "0", "Long CE press should fully clear"