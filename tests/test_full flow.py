import pytest
import logging
from pages.addtocart_page import AddToCartPage
from pages.checkout_page import CheckoutPage

logger = logging.getLogger(__name__)

# Full checkout flow (login auto-executed by login_fixture)
@pytest.mark.normal
def test_full_checkout_flow(login_fixture):  # 关键：替换driver为login_fixture
    # Get driver instance from login fixture (login already completed)
    driver = login_fixture
    logger.info("\n=======Full checkout flow======")

    try:
        # Step 1: Add item to cart (login is done by fixture)
        add_to_cart_page = AddToCartPage(driver)
        add_to_cart_result = add_to_cart_page.add_to_cart()
        assert add_to_cart_result["original_num"] >= 1
        logger.info("Item added to cart successfully")

        # Step 2: Checkout process
        checkout_page = CheckoutPage(driver)
        checkout_result = checkout_page.checkout()
        
        # Verify checkout information
        assert add_to_cart_result["original_name"] in checkout_result["name"], \
            f"Checkout product name mismatch: actual={add_to_cart_result['original_name']}, checkout={checkout_result['name']}"
        assert add_to_cart_result["original_price"] in checkout_result["price"], \
            f"Checkout product price mismatch: actual={add_to_cart_result['original_price']}, checkout={checkout_result['price']}"
        logger.info("Order submitted successfully")

    except Exception as e:
        logger.error(f"Full checkout flow failed: {str(e)}", exc_info=True)
        raise e
