# common/clearcart.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

def clearcart(driver):
    """
    通用清空购物车函数：
    - 兼容购物车有1个/多个商品的场景
    - 购物车为空时直接返回
    - 异常时记录日志并抛出，方便排查
    """
    # 定位符（通用化，匹配所有删除按钮）
    shopping_cart_btn = (By.CLASS_NAME, 'shopping_cart_link')
    remove_btns_locator = (By.XPATH, "//button[contains(@id, 'remove-')]")
    menu_btn = (By.ID, "react-burger-menu-btn")
    all_items_btn = (By.ID, "inventory_sidebar_link")

    # 初始化BasePage（必须传入driver）
    base_page = BasePage(driver)

    try:
        # 步骤1：进入购物车页面（先到购物车，再删商品）
        base_page.elem_click(shopping_cart_btn)
        logger.info("成功进入购物车页面")

        # 步骤2：查找所有删除按钮（新增find_elements方法，替代is_element_exist）
        remove_btns = base_page.find_elements(remove_btns_locator)

        # 步骤3：判断购物车是否为空，为空则直接返回
        if not remove_btns:
            logger.info("购物车已为空，无需清空")
            # 可选：空购物车时也返回列表页（根据你的需求调整）
            base_page.elem_click(menu_btn)
            base_page.elem_click(all_items_btn)
            return  # 关键：终止函数，避免执行后续删除逻辑

        # 步骤4：逐个删除所有商品（核心逻辑）
        for btn in remove_btns:
            btn.click()
            logger.info("成功删除一个购物车商品")

        logger.info("购物车所有商品已清空")

        # 步骤5：删除完成后，返回商品列表页（仅执行一次）
        base_page.elem_click(menu_btn)
        base_page.elem_click(all_items_btn)

    except Exception as e:
        # 异常兜底：返回列表页+记录日志+抛出异常
        logger.error(f"清空购物车失败，错误原因：{str(e)}，尝试返回商品列表页")
        try:
            base_page.elem_click(menu_btn)
            base_page.elem_click(all_items_btn)
        except Exception as e2:
            logger.error(f"兜底操作（返回商品列表）失败：{str(e2)}")
        raise  # 让上层夹具感知失败，便于定位问题