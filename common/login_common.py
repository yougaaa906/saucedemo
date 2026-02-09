from config.config import USERNAME,PASSWORD
from pages.login_page import LoginPage
import logging

logger = logging.getLogger(__name__)



def login_common(driver,username=USERNAME, password=PASSWORD):
    login_page = LoginPage(driver)
    login_page.elem_input(login_page.account_input, username)
    login_page.elem_input(login_page.pwd_input, password)
    login_page.elem_click(login_page.login_btn)
    login_page.wait_elem_visible(login_page.homepage_title)
    login_page.logger.info(f"登录成功")


    logger.info("通⽤登录步骤完成")



