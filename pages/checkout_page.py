from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import FIRSTNAME,LASTNAME,POSTALCODE
import logging



class CheckoutPage(BasePage):
    logger = logging.getLogger(__name__)
    #[去购物车结算]按钮
    shopping_cart_btn = (By.CLASS_NAME, 'shopping_cart_link')
    #产品确认页面
    product_cart_name = (By.CLASS_NAME,'inventory_item_name')
    product_cart_price = (By.CLASS_NAME,"inventory_item_price")

    #结算按钮
    checkout_btn = (By.ID,"checkout")
    # 填入个人信息
    first_name_field = (By.ID, 'first-name')
    last_name_field = (By.ID, "last-name")
    postal_code_field = (By.ID, "postal-code")
    continue_btn = (By.ID, "continue")

    #确认订单页面
    product_order_name = (By.CLASS_NAME,"inventory_item_name")
    product_order_price = (By.CLASS_NAME,"inventory_item_price")

    def checkout(self,firstname=FIRSTNAME,lastname=LASTNAME,postalcode=POSTALCODE):
        try:
            self.elem_click(self.shopping_cart_btn)
            self.wait_elem_visible(self.product_cart_name)
            self.wait_elem_visible(self.product_cart_price)
            self.elem_click(self.checkout_btn)
            self.elem_input(self.first_name_field,firstname)
            self.elem_input(self.last_name_field,lastname)
            self.elem_input(self.postal_code_field,postalcode)
            self.elem_click(self.continue_btn)
            product_final_name = self.wait_elem_visible(self.product_cart_name).text.strip()
            product_fianl_price = self.wait_elem_visible(self.product_order_price).text.strip()
            product_info = {
                "name":product_final_name,
                "price":product_fianl_price
            }
            self.logger.info("结算操作成功")
            return product_info
        except Exception as e:
            self.logger.info(f"结算操作失败，失败原因：{str(e)}")
            raise e













