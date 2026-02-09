
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import USERNAME,PASSWORD
import logging



#如果想让登录调用，则抽离登录，只在其中写登录方法，因此单独写一个脚本，此登录脚本作为单独的用例执行，不可被调用
class LoginPage(BasePage):
    logger = logging.getLogger(__name__)
    #封装登录操作中的所有元素定位
    #用户名
    account_input = (By.ID, "user-name")
    #密码
    pwd_input =(By.ID, 'password')
    #登录按钮
    login_btn = (By.ID, 'login-button')
    #登陆后的主页元素
    homepage_title = (By.CLASS_NAME, 'app_logo')


    #封装登录操作
    def login(self,username=USERNAME,password=PASSWORD):
        try:
            self.elem_input(self.account_input,username)
            self.elem_input(self.pwd_input,password)
            self.elem_click(self.login_btn)
            login_success = self.wait_elem_visible(self.homepage_title)
            self.logger.info(f"登录成功")
            return login_success.text.strip()
        except Exception as e:
            self.logger.info(f"登录失败，失败原因是：{str(e)}")
            raise e






