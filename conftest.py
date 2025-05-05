import pytest
import random
from playwright.sync_api import sync_playwright
import os
from pages.google_search_page import GoogleSearchPage
from pages.calculator_page import CalculatorPage
import time

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )

@pytest.fixture(scope="session")
def browser(request):
    headless = request.config.getoption("--headless")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,  # Use the command-line option
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100, 125)}.0.0.0 Safari/537.36'
            ]
        )
        yield browser
        browser.close()

@pytest.fixture
def context(browser):
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        locale="en-US",
        timezone_id="America/New_York",
        # Add device scale factor
        device_scale_factor=1,
        # Enable JavaScript by default
        java_script_enabled=True,
        # Ignore HTTPS errors
        ignore_https_errors=True,
        # Set geolocation to US
        geolocation={"longitude": -122.08, "latitude": 37.39},
        # Set permissions
        permissions=["geolocation"]
    )
    
    # Add additional stealth scripts
    context.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
    });
    window.navigator.chrome = {
        runtime: {},
    };
    Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en'],
    });
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5],
    });
    // Override the permissions API
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
    );
    """)
    
    yield context
    context.close()
    
@pytest.fixture
def page(context):
    yield context.new_page()

@pytest.fixture
def google_search_page(page):
    return GoogleSearchPage(page)

@pytest.fixture
def calculator_page(google_search_page):
    try:
        max_attempts = 1  # Reduced from 3
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"\nAttempt {attempt}: Searching for calculator...")
                google_search_page.search_for_calculator()
                
                calc_page = CalculatorPage(google_search_page.page)
                calc_page.wait_for_calculator()
                
                # Quick verification
                calc_page.click_button('1')
                assert calc_page.get_display_value() == "1", "Button not working"
                calc_page.click_button('AC')
                
                return calc_page
                
            except Exception as e:
                if attempt == max_attempts:
                    raise
                print(f"Attempt {attempt} failed: {str(e)}")
                google_search_page.page.reload()
                time.sleep(1)  # Reduced delay
                
    except Exception as e:
        google_search_page.page.screenshot(path="reports/calculator_setup_failed.png")
        pytest.fail(f"Failed to initialize calculator: {str(e)}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        page = item.funcargs.get("page")
        if page:
            os.makedirs("reports/screenshots", exist_ok=True)
            page.screenshot(path=f"reports/screenshots/{item.name}.png")