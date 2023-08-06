# -*- coding: utf-8 -*-
"""
二次封装 selenium 功能：

py_selenium.chrome_head：        浏览器头
py_selenium.kill：               杀进程
py_selenium.requests_cookies：   获取selenium的cookie并且转换成requests可用的cookie
py_selenium.base_location：      一定会定位到对象
py_selenium.roll：               滑动到指定位置
py_selenium.definitely_click_a： 一定会点击一次
py_selenium.definitely_click_b： 点到该元素点不到为止
py_selenium.start_cookie：       使用 cookie
py_selenium.update_cookie：      更新 cookie
py_selenium.jump_iframe：        进入 iframe
py_selenium.jump_out_iframe：    跳出 iframe
py_selenium.anti_robot：         反反机器人

"""

import os
import time
import selenium
from selenium import webdriver


def chrome_head(wait=1, is_psd=True, is_image=False, is_css=False, is_audio=False, is_maximize_win=False, executable_path='Chrome/Application/chromedriver.exe'):
    """
     - 通用浏览器头部信息
     - chrome：https://www.google.cn/chrome/
     - chromedriver：http://chromedriver.storage.googleapis.com/index.html

    :param wait: 隐式等待
    :param is_psd: 不显示记住密码框
    :param is_image: 不加载页面图片
    :param is_css: 不加载 css
    :param is_audio: 静音
    :param is_maximize_win: 浏览器最大化
    :param executable_path: 浏览器路径
    :return:
    """
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('log-level=3')
    prefs = {}
    if is_psd:
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
    if is_image:
        prefs = {"profile.managed_default_content_settings.images": 2}
    if is_css:
        prefs['permissions.default.stylesheet'] = 2
    if is_audio:
        option.add_argument("--mute-audio")

    option.add_experimental_option("prefs", prefs)

    try:
        driver = webdriver.Chrome(executable_path=executable_path, chrome_options=option)
    except selenium.common.exceptions.WebDriverException:
        driver = webdriver.Chrome(chrome_options=option)
    except Exception as e:
        print(e)
        input('浏览器异常，请检查。')
        exit()
    if is_maximize_win:
        driver.maximize_window()
    driver.implicitly_wait(wait)
    return driver


def kill():
    """杀进程"""
    os.system('taskkill /f /im chromedriver.exe')


def requests_cookies(driver):
    """获取selenium的cookie并且转换成requests可用的cookie"""
    time.sleep(1)
    cookies = '; '.join(item for item in [item["name"] + "=" + item["value"] for item in driver.get_cookies()])
    return cookies


def base_location(driver, types: list, error=True, error_log=False):
    """
     - 一定会定位到对象
    :param driver:
    :param types: 定位类型（xpath、css、id、classname、name） 使用方法：[定位类型, 定位信息] 如 ['xpath', '//input[1]']
    :param error: 定位异常时是否需要重新定位；如果不需要会返回 None
    :param error_log: 是否打印报错信息
    :return: 返回定位对象，用于各种操作：click、text、send_keys...等
    """
    ec = 1
    location_obj = None
    while True:
        try:
            if types[0] == 'xpath':
                location_obj = driver.find_element_by_xpath(types[1])
            elif types[0] == 'css':
                location_obj = driver.find_element_by_css_selector(types[1])
            elif types[0] == 'id':
                location_obj = driver.find_element_by_id(types[1])
            elif types[0] == 'classname':
                location_obj = driver.find_element_by_class_name(types[1])
            elif types[0] == 'name':
                location_obj = driver.find_element_by_name(types[1])
            if location_obj:
                return location_obj
        except Exception as e:
            if error_log and ec:
                ec = 0
                print(e)
            if not error:
                return location_obj


def roll(driver, types: list, error_log=False):
    """
    - 滚动到指定位置
    :param types: 参照 py_selenium.base_location 源码
    :param driver:
    :param error_log: 是否打印报错信息
    :return:
    """
    ec = 1
    while True:
        try:
            location_obj = base_location(driver, types=types, error_log=error_log)
            driver.execute_script("arguments[0].scrollIntoView();", location_obj)
            break
        except Exception as e:
            if error_log and ec:
                ec = 0
                print(e)


def definitely_click_a(driver, types: list, error_log=False):
    """一定会点击一次"""
    ec = 1
    while True:
        try:
            location_obj = base_location(driver, types=types, error_log=error_log)
            location_obj.click()
            break
        except Exception as e:
            if error_log and ec:
                ec = 0
                print(e)


def definitely_click_b(driver, types: list, error_log=False):
    """点到该元素点不到为止"""
    ec = 1
    while True:
        try:
            location_obj = base_location(driver, types=types, error=False, error_log=error_log)
            location_obj.click()
        except Exception as e:
            if error_log and ec:
                ec = 0
                print(e)
            break


def start_cookie(path='cookies.txt'):
    """
    - 使用 cookie
    :return:

    使用教程：
    cookie_list = start_cookie()
    if cookie_list:
        for cookie in eval(cookie_list):
            driver.add_cookie(cookie)
        driver.get('登录后的url，不是登录的url')
    """
    print('使用 cookies')
    with open(path) as f:
        return f.read()


def update_cookie(driver, path='cookies.txt'):
    """
    - 更新 cookie
    :param path: 文件保存路径
    :param driver:
    :return:

    一般都是搭配 py_selenium.start_cookie 方法一起使用。
    """
    print('更新 cookies')
    with open(path, 'w') as f:
        f.write(str(driver.get_cookies()))


def jump_iframe(driver, types: list, error_log=False):
    """进入 iframe"""
    ec = 1
    while True:
        try:
            location_obj = base_location(driver, types=types, error_log=error_log)
            driver.switch_to.frame(location_obj)
            break
        except Exception as e:
            if error_log and ec:
                ec = 0
                print(e)


def jump_out_iframe(driver):
    """跳出 iframe"""
    driver.switch_to.default_content()


def anti_robot(driver):
    """反反机器人"""
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
    })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}})





