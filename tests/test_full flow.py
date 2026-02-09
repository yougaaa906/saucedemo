# tests/test_full_flow.py（整合所有流程，100%按order执行）
import pytest


from pages.addtocart_page import AddToCartPage
from pages.checkout_page import CheckoutPage
import logging
from common.login_common import login_common


logger = logging.getLogger(__name__)

# 流程第1步：登录（order=1，最先执行）
@pytest.mark.normal
def test_full_checkout_flow(driver):
    logger.info("\n=======完整购买流程======")

    try:
        #登录




        #加购物车


        add_to_cart_page = AddToCartPage(driver)
        add_to_cart_result = add_to_cart_page.add_to_cart()
        assert add_to_cart_result["original_num"] >= 1
        logger.info("加入购物车成功")

        # 购买

        checkout_page = CheckoutPage(driver)
        checkout_result = checkout_page.checkout()
        assert add_to_cart_result["original_name"] in checkout_result["name"],f"结算商品名称与实际不符,实际为：{add_to_cart_result['original_name']}，结算商品名为：{checkout_result['name']}"
        assert  add_to_cart_result["original_price"] in checkout_result["price"],"结算商品价格与实际不符,实际为：{add_to_cart_result['original_price']}，结算商品名为：{checkout_result['price']}"
        logger.info("订单提交成功")

    except Exception as e:
        logger.error(f"完整购买流程失败：{str(e)},exc_info=True")
        raise e

