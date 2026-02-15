import logging
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

# Page Object for Cart Clearing Functionality (follows POM design pattern)
# Encapsulates elements and actions to remove items from shopping cart
class ClearProductPage(BasePage):
    # Initialize logger for ClearProductPage class
    logger = logging.getLogger(__name__)

    # ------------------------------
    # Element Locators (encapsulated for maintainability)
    # ------------------------------
    # Burger menu button (opens sidebar navigation)
    menu_btn = (By.ID, "react-burger-menu-btn")
    # All items button (navigates back to inventory page)
    all_items_btn = (By.ID, "inventory_sidebar_link")
    # Shopping cart link (navigates to cart page)
    shopping_cart_btn = (By.CLASS_NAME, 'shopping_cart_link')
    # Remove button for specific product (Sauce Labs Backpack)
    remove_btn = (By.ID, "remove-sauce-labs-backpack")

    # ------------------------------
    # Core Cart Clearing Action (encapsulated)
    # ------------------------------
    def clear_product_from_cart(self):  # Renamed: clearproductpage → clear_product_from_cart (PEP 8 compliance)
        """
        Execute flow to remove specific product (Sauce Labs Backpack) from cart:
        1. Opens sidebar menu
        2. Navigates back to inventory page (reset context)
        3. Navigates to shopping cart page
        4. Clicks remove button for target product
        5. Logs success/failure with context
        
        :raises Exception: Propagates errors for test case failure handling
        """
        try:
            # Step 1: Open sidebar menu
            self.elem_click(self.menu_btn)
            
            # Step 2: Navigate back to inventory page (reset navigation context)
            self.elem_click(self.all_items_btn)
            
            # Step 3: Navigate to shopping cart page
            self.elem_click(self.shopping_cart_btn)
            
            # Step 4: Remove target product from cart
            self.elem_click(self.remove_btn)
            
            # Log successful cart clearing
            self.logger.info("Successfully removed Sauce Labs Backpack from shopping cart")
        
        except Exception as e:
            # Log detailed failure (error level for troubleshooting) + re-raise exception
            self.logger.error(f"Failed to remove product from cart. Error: {str(e)}")
            raise e
