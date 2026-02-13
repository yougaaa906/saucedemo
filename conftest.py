import pytest
import os
import logging
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # 新增：导入WebDriverWait
from datetime import datetime
from common.login_common import login_common

# --------------------------
# Configure logging (saucedemo exclusive)
# --------------------------
def setup_logging():
    # Create saucedemo exclusive log directory
    log_dir = "logs-saucedemo"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate log file with timestamp
    log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Configure logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# --------------------------
# Pytest fixture for WebDriver (Edge)
# --------------------------
@pytest.fixture(scope="function")
def driver(request):
    # Configure Edge options
    edge_options = Options()
    edge_options.add_argument("--headless=new")  # Headless mode for CI
    edge_options.add_argument("--no-sandbox")    # Required for Ubuntu CI
    edge_options.add_argument("--disable-dev-shm-usage")  # Fix resource limit issue
    edge_options.add_argument("--window-size=1920,1080")  # 补充：适配CI页面布局
    edge_options.add_argument("--disable-cache")          # 补充：禁用缓存减少渲染问题
    
    # Initialize driver
    driver = webdriver.Edge(options=edge_options)
    driver.implicitly_wait(10)  # Global implicit wait
    driver.set_page_load_timeout(30)  # 补充：页面加载超时配置
    driver.maximize_window()
    
    # Teardown: Take screenshot on failure + quit driver
    def teardown():
        # Capture screenshot if test failed
        if request.node.rep_call.failed:
            # Create saucedemo exclusive screenshot directory
            screenshot_dir = "screenshots-saucedemo"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            # Generate screenshot filename with test name + timestamp
            screenshot_name = f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            
            # Save screenshot
            driver.save_screenshot(screenshot_path)
            logger.error(f"Test failed! Screenshot saved to: {screenshot_path}")
        
        # Quit driver
        driver.quit()
        logger.info("Driver closed successfully")
    
    request.addfinalizer(teardown)
    logger.info("Driver initialized successfully")
    return driver

# --------------------------
# Login fixture (critical: add @pytest.fixture decorator)
# --------------------------
@pytest.fixture(scope="function")  # 新增：夹具装饰器，pytest才能识别
def login_fixture(driver):
    """Fixture for saucedemo login, reuse existing login_common function"""
    # Navigate to login page first
    driver.get("https://www.saucedemo.com/")
    logger.info("Navigated to saucedemo login page")
    
    # Call your existing login_common function
    login_common(driver)  # Use default USERNAME/PASSWORD from config
    
    # Verify login success (double insurance for CI)
    WebDriverWait(driver, 30).until(
        lambda d: "inventory.html" in d.current_url
    )
    logger.info("Login fixture executed successfully")
    
    # Return driver to test case
    return driver

# --------------------------
# Pytest hook to capture test result
# --------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to get the report object
    outcome = yield
    rep = outcome.get_result()
    
    # Store test result in node object (used in teardown)
    setattr(item, "rep_" + rep.when, rep)
    
    # Log test result
    if rep.when == "call":
        if rep.failed:
            logger.error(f"Test {item.name} failed")
        else:
            logger.info(f"Test {item.name} passed")
