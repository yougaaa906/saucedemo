import pytest
import logging
from pages.addtocart_page import AddToCartPage
from pages.checkout_page import CheckoutPage

# Initialize logger for test module
logger = logging.getLogger(__name__)

# Test case for end-to-end checkout flow (login handled by login_fixture)
# Mark: "normal" for test suite categorization
@pytest.mark.normal
def test_end_to_end_checkout_flow(login_fixture):
    """
    End-to-end test for full checkout flow:
    1. Reuse logged-in driver from login_fixture (no duplicate login)
    2. Add first product to cart and validate cart count
    3. Complete checkout process with default shipping info
    4. Verify product name/price consistency between cart and order review
    
    :param login_fixture: Fixture providing logged-in WebDriver instance
    """
    # Extract driver instance from login fixture (login already completed)
    driver = login_fixture
    logger.info("\n======= Starting End-to-End Checkout Flow Test ======")

    try:
        # Step 1: Add product to cart and validate cart count update
        add_cart_page = AddToCartPage(driver)
        cart_product_info = add_cart_page.add_to_cart()
        
        # Assert: Cart count should be at least 1 after adding item
        assert cart_product_info["original_num"] >= 1, \
            f"Cart count validation failed: Expected ≥1, Actual={cart_product_info['original_num']}"
        logger.info(f"Product added to cart successfully | Name: {cart_product_info['original_name']} | Price: {cart_product_info['original_price']}")

        # Step 2: Execute checkout process (fill shipping info + submit)
        checkout_page = CheckoutPage(driver)
        order_product_info = checkout_page.checkout()
        
        # Step 3: Verify product name consistency (cart vs order review)
        assert cart_product_info["original_name"] == order_product_info["name"], \
            f"Product name mismatch: Cart={cart_product_info['original_name']}, Order={order_product_info['name']}"
        
        # Step 4: Verify product price consistency (cart vs order review)
        assert cart_product_info["original_price"] == order_product_info["price"], \
            f"Product price mismatch: Cart={cart_product_info['original_price']}, Order={order_product_info['price']}"
        
        logger.info("End-to-End Checkout Flow Test Completed Successfully")

    except AssertionError as ae:
        # Handle assertion failures separately (clearer error logging)
        logger.error(f"Checkout Flow Assertion Failed: {str(ae)}", exc_info=True)
        # Capture screenshot on assertion failure (for debugging)
        driver.save_screenshot("checkout_assertion_failure.png")
        raise ae
    except Exception as e:
        # Handle non-assertion errors (e.g., element not found, timeout)
        logger.error(f"Checkout Flow Execution Failed: {str(e)}", exc_info=True)
        driver.save_screenshot("checkout_execution_failure.png")
        raise e
