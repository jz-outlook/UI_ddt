import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)


class FakeElement:

    def __new__(cls, args):
        return args


class basePage:
    _url = ''

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        self.check_url()
        self.check_element()

    def find_element(self, xpath):
        def f(_):
            return self.driver.find_element(By.XPATH, xpath)

        return self.wait.until(f)

    def check_url(self):
        assert self.driver.current_url == self._url, self.driver.current_url

    def check_element(self):
        for attr in dir(self):
            if attr.startswith('_ele_'):
                loc = getattr(self, attr)
                ele = self.find_element(loc)

                key = attr.replace('_ele_', '_ele_')
                setattr(self, key, ele)

    def get_msg(self):
        """获取弹窗提示"""
        ele = self.find_element('')
        return ele.text


class RegPage(basePage):
    """
    用户登录页面
    """
    _url = 'https://admin.test.tiger-sec.cn:9000/login'

    _ele_username = FakeElement('//*[@id="normal_login_username"]')
    _ele_password = FakeElement('//*[@id="normal_login_password"]')
    _ele_login = FakeElement("//button[contains(.,'登 录')]")

    def input_username(self, username):
        self._ele_username.send_keys(username)

    def input_password(self, password):
        self._ele_password.send_keys(password)

    def click_login(self):
        self._ele_login.click()

    def submit(self, username, password):
        self._ele_username.send_keys(username)
        self._ele_password.send_keys(password)
        self._ele_login.click()


class Equipment(basePage):
    _url = 'https://admin.test.tiger-sec.cn/app_login'
    _ele_username = FakeElement('//*[@id="login-form_username"]')
    _ele_password = FakeElement('//*[@id="login-form_password"]')
    _ele_login = FakeElement('//button[@type="submit"]')

    def submit(self, username, password):
        self._ele_username.send_keys(username)
        self._ele_password.send_keys(password)
        self._ele_login.click()
