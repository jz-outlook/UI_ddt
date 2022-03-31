# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
#
# from libs.action import KeyWord
# import time
#
# import pytest
# from selenium.webdriver.common.by import By
# from webdriver_helper import get_webdriver
#
#
#
# @pytest.fixture()
# def user_login(cache):
#     """
#     登录夹具
#     :return:
#     """
#     service = Service(executable_path=r'C:\Users\zhang\.wdm\drivers\chromedriver\win32\99.0.4844.35\chromedriver.exe')
#     options = webdriver.ChromeOptions()
#     options.add_argument('--ignore-certificate-errors')
#     options.add_argument('start-maximized')
#     driver = webdriver.Chrome(service=service, options=options)
#     # driver = get_webdriver()
#     driver.get('https://admin.test.tiger-sec.cn:9000/login')
#     cookie = cache.get('user_cookie', {})
#     for c in cookie:
#         driver.add_cookie(c)
#     # driver.refresh()
#
#     ele = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[1]/div/div[3]/span/svg')
#     if ele:
#         pass
#     else:
#         driver.get("https://admin.test.tiger-sec.cn:9000/login")
#         driver.find_element(By.XPATH, '//*[@id="normal_login_username"]').send_keys('admin')
#         driver.find_element(By.XPATH, '//*[@id="normal_login_password"]').send_keys('Hy123!!!')
#         driver.find_element(By.XPATH, "//button[contains(.,'登 录')]").click()
#         time.sleep(1)
#         cache.set('user_cookie', driver.get_cookies())
#     yield driver
#
#     driver.quit()
#
#
# def test_new(user_login):
#     keyword = KeyWord(user_login)
#     keyword.key_get('https://admin.test.tiger-sec.cn:9000/devices/list/list')
#     keyword.key_input('//input[@name="deviceId"]', 1234567890)
#     keyword.key_click('//*[@id="root"]/div/div[2]/div[2]/div/div/div/form/div/div[1]/div/div[2]/div/div/div')
#     keyword.key_click('//span[@class="ant-select-selection-search"]')
#     time.sleep(5)
#
#
# def test_new1(user_login):
#     keyword = KeyWord(user_login)
#     # print(keyword.find_elements('//div[@role="menuitem"]', 1))
#     keyword.key_clicks('//div[@role="menuitem"]', 6)
#     time.sleep(1)
#     keyword.key_click('//a[@href="/networkInvisible"]')
#     time.sleep(1)
#     keyword.key_get_text('//span[@class="ant-select-selection-item"]', 'msg')  # 获取实际结果保存在变量当中
#     keyword.key_assert('微隧道模式', 'equal', '{msg}')
#     user_login.get_screenshot_as_file('a.png')
#
#
# def test_new1_error(user_login):
#     keyword = KeyWord(user_login)
#     # print(keyword.find_elements('//div[@role="menuitem"]', 1))
#     keyword.key_clicks('//div[@role="menuitem"]', 6)
#     time.sleep(1)
#     keyword.key_click('//a[@href="/networkInvisible"]')
#     time.sleep(1)
#     keyword.key_get_text('//span[@class="ant-select-selection-item"]', 'msg')  # 获取实际结果保存在变量当中
#     keyword.key_assert('微隧道模式123', 'not_equal', '{msg}')
#     user_login.get_screenshot_as_file('a.png')
