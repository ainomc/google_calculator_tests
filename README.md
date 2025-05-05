# Google Calculator E2E Test Suite

**Senior SDET Challenge Solution**  
*Automated testing for Google's search calculator using Playwright + Python*

---

## Challenge Overview
As a **Senior SDET at Google**, your task is to validate a calculator that appears when users search for "calculator." This test suite verifies core functionality including:
- Basic operations (`+`, `-`, `×`, `÷`)
- Decimal handling (`.`)
- Clear functions (`AC`, `CE`)
- Complex expressions

---

## Technical Implementation
| Key Aspect               | Details                                                                 |
|--------------------------|-------------------------------------------------------------------------|
| **Tooling**              | Playwright + Python                                                    |
| **Architecture**         | Page Object Model (POM) with OOP principles                            |
| **Reporting**            | pytest-html with self-contained reports                                |
| **Parallel Execution**   | Supported via `pytest-xdist`                                           |
| **Browser**              | Chromium (headed/headless modes)                                       |

---

## Setup & Execution
```bash
# Install dependencies
pip install -r requirements.txt
playwright install

# Run tests (headed mode)
pytest tests/ -v --html=reports/report.html --self-contained-html

# Parallel execution (4 workers)
pytest tests/ -v -n 4 --html=reports/report.html --self-contained-html

# Headless mode
pytest tests/ --headless --html=reports/report.html


Project Structure
├── pages/
│   ├── base_page.py            # Core page interactions
│   ├── calculator_page.py      # Calculator operations
│   └── google_search_page.py   # Search functionality
├── tests/
│   └── test_calculator.py      # Parameterized test cases
├── conftest.py                 # Fixtures & hooks
├── reports/                    # HTML reports
└── TEST_CASES.md               # Test coverage documentation