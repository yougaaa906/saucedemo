import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

# Page Object for Add to Cart functionality (follows POM design pattern)
class AddToCartPage(BasePage):
    # Initialize logger for AddToCartPage class
    logger = logging.getLogger(__name__)

    # ------------------------------
    # Element Locators (encapsulated for maintainability)
    # ------------------------------
    # Product card (first item in inventory list)
    products_01 = (By.XPATH, '//div[@data-test="inventory-list"]/div[@data-test="inventory-item"][1]')
    
    # First product name (primary identifier)
    product01_name = (By.XPATH,
                      '//div[@class="inventory_list"]/div[@class="inventory_item"][1]//div[contains(@class,"inventory_item_name")]')
    
    # First product price (corrected: By.CLASS_NAME → By.XPATH for valid locator type)
    products01_price = (By.XPATH,
                        '//div[@class="inventory_list"]/div[@class="inventory_item"][1]//div[contains(@class,"inventory_item_price")]')

    # Product name in detail view (corrected: data-time → data-test attribute typo)
    product_detail_name = (
        By.XPATH, '//div[contains(@class,"inventory_details_name") and @data-test="inventory-item-name"]')

    # Add to cart button (corrected: By.ID → By.XPATH for data-test attribute)
    product_add_cart = (By.XPATH, '//button[@data-test="add-to-cart"]')
    
    # Shopping cart item count badge (only visible when cart has items)
    cart_count = (By.CLASS_NAME, 'shopping_cart_badge')

    # ------------------------------
    # Core Add to Cart Action (encapsulated)
    # ------------------------------
    def add_to_cart(self):
        """
        Execute complete add-to-cart flow for the first inventory item:
        1. Validates product list is loaded
        2. Captures original product name/price from inventory list
        3. Navigates to product detail page
        4. Clicks add-to-cart button
        5. Calculates updated cart count (handles empty cart edge case)
        6. Returns product info + updated cart count for validation
        
        :return: Dictionary with product name, price, and updated cart count
        :raises Exception: Propagates errors for test case failure handling
        """
        try:
            # Wait for product list to load and capture original product name
            self.wait_elem_visible(self.product01_name)
            product_original_name = self.wait_elem_visible(self.product01_name).text.strip()
            
            # Capture original product price from inventory list
            product_original_price = self.wait_elem_visible(self.products01_price).text.strip()
            
            # Navigate to product detail page (click product name)
            self.elem_click(self.product01_name)

            # Wait for detail page to load and click add-to-cart button
            self.wait_elem_visible(self.product_detail_name)
            self.elem_click(self.product_add_cart)

            # Handle edge case: cart count badge missing (empty cart)
            try:
                product_original_num = int(self.wait_elem_visible(self.cart_count).text.strip())
            except Exception:
                # Cart was empty before add-to-cart (default count = 0)
                product_original_num = 0  

            # Log successful add-to-cart operation
            self.logger.info("Add to cart operation completed successfully")
            
            # Compile product info (updated cart count = original + 1)
            product_original_info = {
                "original_name": product_original_name,
                "original_price": product_original_price,
                "original_num": product_original_num + 1  # Increment count post-add
            }
            
            # Return product info for validation in test cases
            return product_original_info
        
        except Exception as e:
            # Log detailed failure with context (error level for troubleshooting)
            self.logger.error(f"Add to cart operation failed. Error: {str(e)}")
            raise e 
