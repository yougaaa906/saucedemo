from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import USERNAME, PASSWORD
import logging

# Page Object for Login Page (follows POM design pattern)
# Note: This class is designed as a standalone test case executor - NOT for import/call by other modules
class LoginPage(BasePage):
    # Initialize logger for LoginPage class
    logger = logging.getLogger(__name__)

    # ------------------------------
    # Element Locators (encapsulated for maintainability)
    # ------------------------------
    # Username input field
    account_input = (By.ID, "user-name")
    # Password input field
    pwd_input = (By.ID, 'password')
    # Login submission button
    login_btn = (By.ID, 'login-button')
    # Homepage logo element (validation for successful login)
    homepage_title = (By.CLASS_NAME, 'app_logo')

    # ------------------------------
    # Core Login Action (encapsulated)
    # ------------------------------
    def login(self, username=USERNAME, password=PASSWORD):
        """
        Execute complete login flow with validation:
        - Inputs credentials (uses config defaults unless overridden)
        - Submits login form
        - Validates successful navigation to homepage
        - Returns homepage logo text for verification
        
        :param username: Optional - custom username (defaults to config.USERNAME)
        :param password: Optional - custom password (defaults to config.PASSWORD)
        :return: Stripped text of homepage logo element (for assertion)
        :raises Exception: Propagates errors for test case failure handling
        """
        try:
            # Step 1: Enter username into input field
            self.elem_input(self.account_input, username)
            
            # Step 2: Enter password into input field
            self.elem_input(self.pwd_input, password)
            
            # Step 3: Click login button to submit credentials
            self.elem_click(self.login_btn)
            
            # Step 4: Wait for homepage element to confirm login success (critical validation)
            login_success_elem = self.wait_elem_visible(self.homepage_title)
            
            # Log successful login with username context
            self.logger.info(f"Login successful for username: {username}")
            
            # Return stripped text for test case assertions
            return login_success_elem.text.strip()
        
        except Exception as e:
            # Log failure with detailed context (error level for troubleshooting)
            self.logger.error(f"Login failed for username: {username}. Error: {str(e)}")
            raise e  # Re-raise to notify test case of failure
