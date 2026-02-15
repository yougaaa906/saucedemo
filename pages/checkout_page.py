from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import FIRSTNAME, LASTNAME, POSTALCODE
import logging

# Page Object for Checkout Flow (follows POM design pattern)
# Encapsulates all checkout-related elements and actions
class CheckoutPage(BasePage):
    # Initialize logger for CheckoutPage class
    logger = logging.getLogger(__name__)

    # ------------------------------
    # Element Locators (encapsulated for maintainability)
    # ------------------------------
    # Shopping cart link (navigates to cart page)
    shopping_cart_btn = (By.CLASS_NAME, 'shopping_cart_link')
    
    # Cart page - product name/price elements (validation)
    product_cart_name = (By.CLASS_NAME, 'inventory_item_name')
    product_cart_price = (By.CLASS_NAME, "inventory_item_price")

    # Cart page - checkout button (initiates checkout flow)
    checkout_btn = (By.ID, "checkout")
    
    # Checkout info page - personal info fields
    first_name_field = (By.ID, 'first-name')
    last_name_field = (By.ID, "last-name")
    postal_code_field = (By.ID, "postal-code")
    
    # Checkout info page - continue button (submits personal info)
    continue_btn = (By.ID, "continue")

    # Order review page - product name/price elements (final validation)
    product_order_name = (By.CLASS_NAME, "inventory_item_name")
    product_order_price = (By.CLASS_NAME, "inventory_item_price")

    # ------------------------------
    # Core Checkout Action (encapsulated)
    # ------------------------------
    def checkout(self, firstname=FIRSTNAME, lastname=LASTNAME, postalcode=POSTALCODE):
        """
        Execute complete checkout flow from cart to order review:
        1. Navigates to shopping cart page
        2. Validates cart items are loaded
        3. Clicks checkout button to enter personal info step
        4. Enters shipping information (defaults from config, overridable)
        5. Submits info and navigates to order review page
        6. Captures final product info for validation
        7. Returns product name/price dict for assertion
        
        :param firstname: Optional - custom first name (defaults to config.FIRSTNAME)
        :param lastname: Optional - custom last name (defaults to config.LASTNAME)
        :param postalcode: Optional - custom postal code (defaults to config.POSTALCODE)
        :return: Dictionary with final product name and price
        :raises Exception: Propagates errors for test case failure handling
        """
        try:
            # Step 1: Navigate to shopping cart page
            self.elem_click(self.shopping_cart_btn)
            
            # Step 2: Wait for cart items to load (validation before checkout)
            self.wait_elem_visible(self.product_cart_name)
            self.wait_elem_visible(self.product_cart_price)
            
            # Step 3: Initiate checkout process
            self.elem_click(self.checkout_btn)
            
            # Step 4: Enter personal shipping information
            self.elem_input(self.first_name_field, firstname)
            self.elem_input(self.last_name_field, lastname)
            self.elem_input(self.postal_code_field, postalcode)
            
            # Step 5: Submit info and proceed to order review
            self.elem_click(self.continue_btn)
            
            # Step 6: Capture final product info for validation
            product_final_name = self.wait_elem_visible(self.product_order_name).text.strip()  # Fixed typo: product_cart_name → product_order_name
            product_final_price = self.wait_elem_visible(self.product_order_price).text.strip()  # Fixed typo: fianl → final
            
            # Compile product info for test case assertions
            product_info = {
                "name": product_final_name,
                "price": product_final_price
            }
            
            # Log successful checkout flow
            self.logger.info(f"Checkout flow completed successfully with postal code: {postalcode}")
            return product_info
        
        except Exception as e:
            # Log detailed failure with context (error level for troubleshooting)
            self.logger.error(f"Checkout flow failed. Error: {str(e)} | Used postal code: {postalcode}")
            raise e  # Re-raise to notify test case of failure
