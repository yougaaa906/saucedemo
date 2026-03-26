import pytest
import os
import logging
from datetime import datetime

# Global logging configuration for test execution
def setup_logging():
    log_dir = "logs-saucedemo"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    return root_logger

logger = setup_logging()

# Playwright page fixture (auto-manages browser, context, and page)
@pytest.fixture(scope="function")
def page(page):
    yield page

# Reusable login fixture for Saucedemo tests
@pytest.fixture(scope="function")
def login_fixture(page):
    page.goto("https://www.saucedemo.com/")
    logger.info("Navigated to saucedemo login page")

    from common.login_common import login_common
    login_common(page)

    # Wait for successful login redirect
    page.wait_for_url("**/inventory.html", timeout=30000)
    logger.info("Login fixture executed successfully")
    return page

# Pytest hook to capture test results (pass/fail)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call":
        if rep.failed:
            logger.error(f"Test {item.name} failed")
        else:
            logger.info(f"Test {item.name} passed")
