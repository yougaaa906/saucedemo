import logging

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AddToCartPage(BasePage):
    logger = logging.getLogger(__name__)
    # 商品卡片
    products_01 = (By.XPATH, '//div[@class="inventory_list"]/div[1]')
    # 第一个商品名称（正确）
    product01_name = (By.XPATH,
                      '//div[@class="inventory_list"]/div[@class="inventory_item"][1]//div[contains(@class,"inventory_item_name")]')
    # 修正1：By.CLASS_NAME → By.XPATH（因为值是XPATH表达式）
    products01_price = (By.XPATH,
                        '//div[@class="inventory_list"]/div[@class="inventory_item"][1]//div[contains(@class,"inventory_item_price")]')

    # 修正2：data-time → data-test（属性名写错）
    product_detail_name = (
    By.XPATH, '//div[contains(@class,"inventory_details_name") and @data-test="inventory-item-name"]')

    # 修正3：By.ID → By.XPATH（add-to-cart是data-test属性，不是id）
    product_add_cart = (By.XPATH, '//button[@data-test="add-to-cart"]')
    # 购物车数量
    cart_count = (By.CLASS_NAME, 'shopping_cart_badge')

    def add_to_cart(self):
        try:
            self.wait_elem_visible(self.products_01)
            product_original_name = self.wait_elem_visible(self.product01_name).text.strip()
            product_original_price = self.wait_elem_visible(self.products01_price).text.strip()
            self.elem_click(self.product01_name)

            self.wait_elem_visible(self.product_detail_name)
            self.elem_click(self.product_add_cart)

            # 修正4：加容错处理（购物车为空时没有badge，默认0）
            try:
                product_original_num = int(self.wait_elem_visible(self.cart_count).text.strip())
            except:
                product_original_num = 0  # 加购前为空，加购后会变成1

            self.logger.info("加入购物车操作已完成")
            product_original_info = {
                "original_name": product_original_name,
                "original_price": product_original_price,
                "original_num": product_original_num + 1  # 加购后数量+1
            }
            return product_original_info
        except Exception as e:
            self.logger.error(f"加入购物车操作失败，失败原因：{str(e)}")  # 建议用error级别，更易排查
            raise e