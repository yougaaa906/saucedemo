import os
import sys
import urllib3
urllib3.Timeout.DEFAULT_TIMEOUT = 10  # 直接给整数，符合要求



#Log and Screenshot Path Configuration
project_path = os.path.dirname(os.path.abspath(__file__))
#Add the project root path to Python's search path
sys.path.append(project_path)

import pytest
import logging
from datetime import datetime
from selenium import webdriver
from config.config import TIMEOUT, TEST_URL  # 👇 修改处3：删掉CHROME_DRIVER_PATH（不用了）
from common.clearcart import clearcart
from common.login_common import login_common

#定义日志、截图的路径
LOG_DIR = os.path.join(project_path,"logs")
SCREENSHOTS_DIR = os.path.join(project_path,"screenshots")
#检索日志、截图的路径，没有则创建
for dir_path in [LOG_DIR,SCREENSHOTS_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

#日志配置
def setup_logger():
    log_filename = os.path.join(LOG_DIR, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s",handlers=[logging.FileHandler(log_filename, encoding="utf-8"),logging.StreamHandler()])
    return logging.getLogger(__name__)

logger = setup_logger()

@pytest.fixture(scope="module")
def driver():
    #浏览器配置 👇 修改处4：把ChromeOptions换成EdgeOptions，参数完全通用！
    edge_options = webdriver.EdgeOptions()
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option("useAutomationExtension", False)
    edge_options.add_argument("--disable-blink-features=AutomationControlled")

    #初始化浏览器 👇 修改处5：替换Edge驱动启动方式（自动下载匹配版本，不用CHROME_DRIVER_PATH了）
    driver = webdriver.Edge(options=edge_options)
    driver.maximize_window()
    driver.get(TEST_URL)
    driver.implicitly_wait(TIMEOUT)
    logger.info(f"浏览器初始化完成，已打开测试网址：{TEST_URL}")

    #返回浏览器驱动，以便后续用例使用
    yield driver

    #后置操作
    #driver.quit()
    #print("√ 所有用例执行完毕")

# ========== 3. 失败自动截图夹具（新增，自动生效） ==========
@pytest.fixture(scope="function", autouse=True)
def fail_screenshot(driver, request):
    """
    用例失败自动截图：
    - scope="function"：每个用例执行后检查
    - autouse=True：自动生效，无需手动调用
    """
    yield  # 执行用例

    # 检查用例是否失败
    if request.node.rep_call.failed:
        # 生成截图文件名（用例名+时间戳，避免重复）
        case_name = request.node.name
        screenshot_name = f"{case_name}_fail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)

        # 保存截图并记录日志
        try:
            driver.save_screenshot(screenshot_path)
            logger.error(f"用例【{case_name}】执行失败，截图已保存至：{screenshot_path}")
        except Exception as e:
            logger.error(f"用例【{case_name}】失败截图保存失败！错误原因：{str(e)}")

# ========== 4. 修复pytest用例结果获取（新增，必须加） ==========
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """获取用例执行结果，给fail_screenshot提供判断依据"""
    outcome = yield
    rep = outcome.get_result()
    # 给用例对象添加结果属性（rep_call：执行阶段结果）
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="function", autouse=True)
def clear_cart(driver):
    login_common(driver)
    clearcart(driver)
    yield
