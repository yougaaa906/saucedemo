# common/clearcart.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import logging

# Initialize logger for clearcart module
logger = logging.getLogger(__name__)

def clearcart(driver):
    """
    Universal shopping cart clearing function:
    - Compatible with scenarios with 1 or multiple items in cart
    - Return directly if cart is empty
    - Log exceptions and re-raise for troubleshooting
    """
    # Locators (generalized to match all remove buttons)
    shopping_cart_btn = (By.CLASS_NAME, 'shopping_cart_link')
    remove_btns_locator = (By.XPATH, "//button[contains(@id, 'remove-')]")
    menu_btn = (By.ID, "react-burger-menu-btn")
    all_items_btn = (By.ID, "inventory_sidebar_link")

    # Initialize BasePage (driver is required parameter)
    base_page = BasePage(driver)

    try:
        # Step 1: Navigate to shopping cart page (required before item removal)
        base_page.elem_click(shopping_cart_btn)
        logger.info("Successfully navigated to shopping cart page")

        # Step 2: Locate all remove buttons (use find_elements instead of is_element_exist)
        remove_btns = base_page.find_elements(remove_btns_locator)

        # Step 3: Check if cart is empty - return immediately if true
        if not remove_btns:
            logger.info("Shopping cart is already empty, no need to clear")
            # Optional: Return to inventory page even if cart is empty (adjust per requirements)
            base_page.elem_click(menu_btn)
            base_page.elem_click(all_items_btn)
            return  # Critical: Terminate function to skip removal logic

        # Step 4: Remove all items one by one (core logic)
        for btn in remove_btns:
            btn.click()
            logger.info("Successfully removed one cart item")

        logger.info("All items in shopping cart have been cleared")

        # Step 5: Return to inventory page after successful removal (execute once)
        base_page.elem_click(menu_btn)
        base_page.elem_click(all_items_btn)

    except Exception as e:
        # Exception fallback: Return to inventory page + log error + re-raise exception
        logger.error(f"Failed to clear shopping cart. Error: {str(e)}. Attempting to return to inventory page")
        try:
            base_page.elem_click(menu_btn)
            base_page.elem_click(all_items_btn)
        except Exception as e2:
            logger.error(f"Fallback operation failed (return to inventory page). Error: {str(e2)}")
        raise  # Re-raise to notify upper-level fixtures of failure for troubleshooting
