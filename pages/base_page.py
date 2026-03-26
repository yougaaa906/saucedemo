import os
from config.config import TIMEOUT
from playwright.sync_api import TimeoutError

class BasePage:
    """Base class for all page objects, providing common Playwright actions."""
    
    def __init__(self, page):
        """Initialize base page with Playwright page instance."""
        self.page = page
        self.timeout = TIMEOUT * 1000  # Convert to milliseconds for Playwright

    def wait_elem_visible(self, selector, timeout=None):
        """Wait for an element to be visible on the page."""
        timeout = timeout or self.timeout
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        except TimeoutError:
            screenshot_name = f"elem_timeout_{selector.replace('/', '_')}.png"
            self.save_screen_shot(screenshot_name)
            raise TimeoutError(f"Element visibility timeout: {selector}")

    def elem_clickable(self, selector, timeout=None):
        """Wait for an element to be ready for interaction (visible & enabled)."""
        timeout = timeout or self.timeout
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        except TimeoutError:
            screenshot_name = f"elem_clickable_timeout_{selector.replace('/', '_')}.png"
            self.save_screen_shot(screenshot_name)
            raise TimeoutError(f"Element not interactable: {selector}")

    def elem_click(self, selector, timeout=None):
        """Click an element after ensuring it is ready."""
        timeout = timeout or self.timeout
        self.elem_clickable(selector, timeout)
        self.page.click(selector)

    def elem_input(self, selector, text, timeout=None):
        """Clear and fill input field with specified text."""
        timeout = timeout or self.timeout
        self.wait_elem_visible(selector, timeout)
        self.page.fill(selector, text)

    def save_screen_shot(self, filename):
        """Capture and save full page screenshot to screenshots directory."""
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        file_path = os.path.join("screenshots", filename)
        self.page.screenshot(path=file_path, full_page=True)
        return file_path

    def open_new_tab(self, selector):
        """Click an element that opens a new tab and switch to it."""
        with self.page.expect_popup() as popup_info:
            self.elem_click(selector)
        return popup_info.value

    def is_element_exist(self, selector):
        """Check if element exists in DOM within a short timeout."""
        try:
            self.page.wait_for_selector(selector, state="attached", timeout=3000)
            return True
        except TimeoutError:
            return False

    def find_elements(self, selector, timeout=None):
        """Return list of matching elements (empty list if none found)."""
        timeout = timeout or self.timeout
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            return self.page.query_selector_all(selector)
        except TimeoutError:
            return []
