from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from config.config import TIMEOUT
import os

# BasePage: Encapsulates common Selenium operations for reusability across page objects
# Purpose: Reduce code duplication by centralizing frequently used actions (wait/click/input/screenshot)
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # Initialize WebDriverWait object with global timeout (fixes "self.wait undefined" error in is_element_exist)
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    # Wait for element to be visible (core wait method for input/validation)
    # :param locator: Tuple (By.XXX, "locator_value")
    # :param timeout: Optional - custom timeout (defaults to config.TIMEOUT)
    # :return: Visible WebElement
    # :raises TimeoutException: If element not visible within timeout (with screenshot)
    def wait_elem_visible(self, locator, timeout=None):
        timeout = timeout or TIMEOUT
        try:
            elem = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return elem
        except TimeoutException:
            # Save screenshot for troubleshooting (naming convention: elem_timeout_<locator_value>.png)
            self.driver.save_screenshot(f"elem_timeout_{locator[1]}.png")
            raise TimeoutException(f"Element visibility timeout: {locator}")

    # Wait for element to be clickable (prerequisite for click operations)
    # :param locator: Tuple (By.XXX, "locator_value")
    # :param timeout: Optional - custom timeout (defaults to config.TIMEOUT)
    # :return: Clickable WebElement
    # :raises TimeoutException: If element not clickable within timeout (with screenshot)
    def elem_clickable(self, locator, timeout=None):
        timeout = timeout or TIMEOUT
        try:
            elem = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            return elem
        except TimeoutException:
            self.driver.save_screenshot(f"elem_clickable_timeout_{locator[1]}.png")
            raise TimeoutException(f"Element clickable timeout: {locator}")

    # Generic click operation (uses elem_clickable to ensure element is ready)
    # :param locator: Tuple (By.XXX, "locator_value")
    # :param timeout: Optional - custom timeout (defaults to config.TIMEOUT)
    def elem_click(self, locator, timeout=None):
        timeout = timeout or TIMEOUT
        elem = self.elem_clickable(locator, timeout)
        elem.click()

    # Generic input operation (clears field first, then sends text)
    # :param locator: Tuple (By.XXX, "locator_value")
    # :param text: String to input into the element
    # :param timeout: Optional - custom timeout (defaults to config.TIMEOUT)
    def elem_input(self, locator, text, timeout=None):
        timeout = timeout or TIMEOUT
        elem = self.wait_elem_visible(locator, timeout)
        elem.clear()  # Clear existing text to avoid concatenation issues
        elem.send_keys(text)

    # Screenshot method with directory validation (ensures screenshots folder exists)
    # :param filename: Name of the screenshot file (e.g., "login_failure.png")
    # :return: Full path to the saved screenshot
    def save_screen_shot(self, filename):
        # Create screenshots directory if it doesn't exist
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        # Construct full path (cross-platform compatible)
        screenshots_path = os.path.join("screenshots", filename)
        self.driver.save_screenshot(screenshots_path)
        return screenshots_path

    # Switch to new tab after clicking a link/button (handles tab creation wait)
    # :param locator: Tuple (By.XXX, "locator_value") - element that opens new tab
    def open_new_tab(self, locator):
        original_handles = self.driver.window_handles
        original_count = len(original_handles)
        
        # Click element to open new tab
        self.elem_click(locator)
        
        # Wait for new tab to be created (max 15s - longer timeout for tab creation)
        WebDriverWait(self.driver, 15).until(lambda x: len(x.window_handles) > original_count)
        
        # Switch to the new tab
        all_windows = self.driver.window_handles
        new_window = None
        for win in all_windows:
            if win not in original_handles:
                new_window = win
                self.driver.switch_to.window(new_window)
                break

    # Check if element exists (alternative to find_elements)
    # :param locator: Tuple (By.XXX, "locator_value")
    # :return: Boolean (True = element exists, False = element not found)
    def is_element_exist(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
        except Exception as e:
            return False

    # Find multiple elements (fixes core error in clearcart.py iteration logic)
    # :param locator: Tuple (By.XXX, "locator_value")
    # :param timeout: Optional - custom timeout (defaults to config.TIMEOUT)
    # :return: List of WebElements (empty list if no elements found)
    def find_elements(self, locator, timeout=None):
        timeout = timeout or TIMEOUT
        try:
            elems = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elems
        except TimeoutException:
            return []  # Return empty list to avoid iteration errors
        except Exception as e:
            return []
