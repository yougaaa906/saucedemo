import logging
from pages.base_page import BasePage
from selenium.webdriver.common.by import By



class ClearProductPage(BasePage):
    logger = logging.getLogger(__name__)
    menu_btn = (By.ID, "react-burger-menu-btn")
    all_items_btn = (By.ID, "inventory_sidebar_link")
    shopping_cart_btn = (By.CLASS_NAME, 'shopping_cart_link')
    # 删除产品按钮
    remove_btn = (By.ID, "remove-sauce-labs-backpack")

    def clearproductpage(self):

        try:
            self.elem_click(self.menu_btn)
            self.elem_click(self.all_items_btn)
            self.elem_click(self.shopping_cart_btn)
            self.elem_click(self.remove_btn)
            self.logger.info("清除购物车已完成")
        except Exception as e:
            self.logger.info("清楚购物车失败，失败原因：{str(e)}")
            raise e


