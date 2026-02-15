from config.config import USERNAME, PASSWORD
from pages.login_page import LoginPage
import logging

# Initialize logger for login utility module
logger = logging.getLogger(__name__)

def login_common(driver, username=USERNAME, password=PASSWORD):
    """
    Universal login function for the application:
    - Uses default credentials from config (overridable via parameters)
    - Executes complete login flow with element validation
    - Logs success status for audit/debugging
    :param driver: Selenium WebDriver instance
    :param username: Optional - custom username (defaults to config.USERNAME)
    :param password: Optional - custom password (defaults to config.PASSWORD)
    """
    # Initialize LoginPage object with driver instance
    login_page = LoginPage(driver)
    
    # Step 1: Input username to account field
    login_page.elem_input(login_page.account_input, username)
    
    # Step 2: Input password to password field
    login_page.elem_input(login_page.pwd_input, password)
    
    # Step 3: Click login button to submit credentials
    login_page.elem_click(login_page.login_btn)
    
    # Step 4: Verify login success by waiting for homepage element (critical validation)
    login_page.wait_elem_visible(login_page.homepage_title)
    
    # Log successful login with context (uses page object logger + module logger for redundancy)
    login_page.logger.info(f"Login successful with username: {username}")
    logger.info("Universal login flow completed successfully")
