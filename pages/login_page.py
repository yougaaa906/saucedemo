from pages.base_page import BasePage
from config.config import USERNAME, PASSWORD
import logging

class LoginPage(BasePage):
    logger = logging.getLogger(__name__)

    # Element locators (CSS selector format for Playwright)
    account_input = "#user-name"
    pwd_input = "#password"
    login_btn = "#login-button"
    homepage_title = ".app_logo"

    def login(self, username=USERNAME, password=PASSWORD):
        """Execute complete login flow and validate success."""
        try:
            self.elem_input(self.account_input, username)
            self.elem_input(self.pwd_input, password)
            self.elem_click(self.login_btn)
            
            # Verify login success
            self.wait_elem_visible(self.homepage_title)
            self.logger.info(f"Login successful for username: {username}")
            
            # Get and return element text for assertion
            return self.page.text_content(self.homepage_title).strip()

        except Exception as e:
            self.logger.error(f"Login failed for username: {username}. Error: {str(e)}"
            raise e
