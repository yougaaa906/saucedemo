UI Automation Framework for Saucedemo (E-commerce)
Project Overview
A robust, maintainable UI automation framework built with Selenium WebDriver and Pytest, designed to test the core functionalities of the Saucedemo E-commerce Platform. This framework follows the Page Object Model (POM) design pattern, integrates Allure for comprehensive test reporting, and leverages GitHub Actions for continuous integration/continuous deployment (CI/CD) to ensure test reliability and efficiency.
The framework focuses on end-to-end (E2E) testing of critical user flows, with a focus on reusability, scalability, and ease of debugging—aligned with industry best practices for QA automation in enterprise environments.
Tech Stack & Dependencies
Core Technologies
•	Programming Language: Python 3.9
•	Automation Tool: Selenium WebDriver 4.15.2
•	Testing Framework: Pytest 7.4.0 (with plugins for reporting/ordering)
•	Reporting Tool: Allure 2.24.1 (via allure-pytest 2.9.45)
•	CI/CD Integration: GitHub Actions
•	Design Pattern: Page Object Model (POM)
Key Dependencies
See requirements.txt for the full dependency list (no redundant packages):
txt
pytest==7.4.0
allure-pytest==2.9.45
selenium==4.15.2
webdriver-manager==4.0.2
pytest-html==3.1.1
pytest-ordering==0.6
python-dotenv==1.2.1
requests==2.26.0
ddt==1.7.2
retrying==1.3.3
Project Structure (POM Architecture)
The framework follows a modular, maintainable structure based on the Page Object Model, separating test logic from page interactions for better scalability:
bash
ui-automation-saucedemo/
├── .github/
│   └── workflows/
│       └── main.yml          # GitHub Actions CI/CD configuration
├── common/                   # Common utility functions
│   ├── clearcart.py          # Universal cart-clearing utility
├── config/                   # Configuration files
│   ├── config.py             # Global constants (credentials, timeout, etc.)
│   └── .env                  # Environment variables (gitignored)
├── pages/                    # Page Object Classes (POM core)
│   ├── base_page.py          # Base Page with common Selenium operations
│   ├── login_page.py         # Login Page elements & actions
│   ├── addtocart_page.py     # Add to Cart Page elements & actions
│   ├── checkout_page.py      # Checkout Page elements & actions
│   └── clearproduct_page.py  # Cart-clearing Page elements & actions
├── tests/                    # Test Cases (E2E flows)
│   └── test_checkout_flow.py # End-to-end checkout flow test
├── screenshots/              # Auto-generated screenshots (on test failure)
├── requirements.txt          # Dependencies
├── pytest.ini                # Pytest configuration
└── README.md                 # Project documentation (you're here)
Key Module Explanations
•	pages/base_page.py: Encapsulates common Selenium operations (wait, click, input, screenshot, etc.) to reduce code duplication.
•	pages/*_page.py: Page-specific classes (e.g., LoginPage, AddToCartPage) that inherit from BasePage and encapsulate page elements/actions.
•	common/: Utility functions (e.g., clearcart.py) for cross-page reusable logic.
•	tests/: E2E test cases that reuse page objects and fixtures (e.g., login fixture) for clean, maintainable test logic.
•	.github/workflows/main.yml: GitHub Actions workflow to run tests automatically on code push, generate Allure reports, and deploy reports to GitHub Pages.
Core Test Scenarios Covered
The framework focuses on critical E2E user flows for the Saucedemo platform:
1.	User Login: Automated login with configurable credentials (from config.py), with success/failure validation.
2.	Add to Cart: Add a product to the shopping cart, validate cart count update, and capture product details (name/price).
3.	Checkout Flow: End-to-end checkout process (cart → shipping info → order review), with validation of product name/price consistency.
4.	Cart Clearing: Universal cart-clearing functionality (compatible with empty/multiple-item carts) for test isolation.
How to Run the Tests
Prerequisites
1.	Install Python 3.9+.
2.	Clone the repository: git clone <repository-url>
3.	Install dependencies: pip install -r requirements.txt
4.	Configure environment variables (optional): Update config/config.py with valid Saucedemo credentials.
Run Tests Locally
•	Run all tests: pytest tests/ -v
•	Run tests with Allure report generation: pytest tests/ -v --alluredir=allure-results
•	View Allure report: allure serve allure-results
CI/CD with GitHub Actions
Tests are automatically triggered on:
      Push to the main branch (only for test-related file changes).Manual trigger via GitHub Actions UI (workflow_dispatch).
CI/CD Workflow Steps:
      Checkout repository code.Set up Python 3.9 and install dependencies.Install Microsoft Edge browser (for UI testing).Run E2E tests (with timeout control and error handling).Upload test artifacts (logs, screenshots, Allure results).Generate Allure HTML report and deploy to GitHub Pages for easy access.
Framework Highlights (Best Practices)
•	Page Object Model (POM): Separates page interactions from test logic, reducing duplication and improving maintainability.
•	Test Isolation: Reusable fixtures (e.g., login fixture) and cart-clearing logic ensure tests are independent and reliable.
•	Robust Error Handling: Timeout control, failure screenshots, and detailed logging (with context) for easy debugging.
•	CI/CD Integration: Automated test execution and report deployment via GitHub Actions, enabling DevOps collaboration.
•     Dependencies: No redundant packages, ensuring fast installation and reduced conflicts.
•	Configurable & Scalable: Global constants and modular design make it easy to extend to new test scenarios or environments.
Test Reporting
Two types of reports are generated for comprehensive test visibility:
1.	Allure Report: Interactive, detailed report with test steps, screenshots (on failure), environment information, and trends. Deployed to GitHub Pages for easy sharing.
2.	Pytest HTML Report: Lightweight HTML report for quick overview of test results (passed/failed/skipped).
Troubleshooting
•	Test Failures: Check screenshots/ for auto-generated failure screenshots and logs for detailed error messages.
•	Browser Compatibility: The framework uses Microsoft Edge (configured in GitHub Actions) – update the browser setup in main.yml for other browsers.
•	Dependency Conflicts: Use the provided requirements.txt to ensure consistent dependency versions.
•	Allure Report Access: After CI/CD execution, the report is available at https://<username>.github.io/<repository-name>/.
Future Enhancements
•	Add more test scenarios (e.g., invalid login, product filtering, checkout with multiple items).
•	Integrate parallel test execution to reduce test runtime.
•	Add database integration for validating order data post-checkout.
•	Implement cross-browser testing (Chrome, Firefox) via GitHub Actions matrix.
•	Add Slack/email notifications for test result alerts.
