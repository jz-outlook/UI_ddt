"""
关键字
"""
import logging
import time

import MySQLdb
import allure
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_helper import get_webdriver

logger = logging.getLogger(__name__)


class KeyWord:
    """
    关键字类：代表了用户操作的指令集
    """
    _db = None
    is_close = False

    def __init__(self, driver: Chrome):
        """
        实例化： 如果没有webdriver就自动获取
        :param driver:
        """
        if not driver:
            driver = get_webdriver()

        # self.driver = get_webdriver()
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.__vars = {}  # 存储变量

        driver.stop_client = self.driver_stop_client  # 当浏览器关闭是，会自动调用_f函数然后修改is_close为True

    def driver_stop_client(self):
        self.is_close = True



    def __del__(self):
        """
        销毁的时候自动执行
        :return:
        """
        if self._db:
            self._db.close()  # 关闭数据库

    def find_element(self, xpath) -> WebElement:
        """
        封装元素定位方法，自动使用xpath
        :param xpath:
        :return:
        """

        def f(_):
            try:
                ele = self.driver.find_element(By.XPATH, xpath)
            except Exception as e:
                logger.debug(f'元素定位失败{e}')
                raise e

            logger.info(f'元素定位成功:{ele.tag_name}')
            return ele

        return self.wait.until(f)

    def find_elements(self, xpath, a) -> WebElement:
        """
        封装元素定位方法，自动使用xpath，自动使用显示等待
        :param a: 切片[1]
        :param xpath:
        :return:
        """

        def f(_):
            return self.driver.find_elements(By.XPATH, xpath)[a]

        return self.wait.until(f)

    @classmethod
    def all_keyword(cls):
        """
        列出所有可用的关键字
        1、key_开头
        2、可调用
        :return:
        """
        _all_keyword = []  # 所有可用的关键字
        for attr in dir(cls):  # 遍历自己所有的成员
            if attr.startswith('key_'):  # 关键字前缀
                method = getattr(cls, attr)
                if callable(method):  # 如果是可调用的
                    _all_keyword.append(attr[4:])
        return _all_keyword

    def key_new_session(self):
        self.driver = get_webdriver()
        self.driver.stop_client = self.driver_stop_client

    def key_quit_session(self):
        self.driver.quit()

    def key_mysql(self, host, port, user, password, database):
        """
        建立数据库连接
        :return:
        """
        self._db = MySQLdb.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database
        )

    def key_save_sql(self, var_name, sql):
        """
        保存sdl的执行结果
        :return:
        """
        assert self._db
        with self._db.cursor() as c:
            c.execute(sql)
            result = c.fetchone()
        self._db.commit()
        self.__vars[var_name] = str(result)
        print(f"sql执行结果{result}")

    def key_sleep(self, times):
        times = float(times)
        time.sleep(times)

    def key_get(self, url):
        """
        关键字： get
        跳转到指定的页面
        :param url: 指定页面的url
        :return:
        """
        self.driver.get(url)

    def key_click(self, xpath, force=False):
        """
        关键字 ： click
            自定表达式然后进行点击
        :param xpath: 定位元素表达式
        :param force: 是否强制点击，True
        :return:
        """
        ele = self.find_element(xpath)
        if force:  # 使用js强制点击
            self.driver.execute_script('arguments[0].click()', ele)
        else:
            ele.click()

    def key_clicks(self, xpath, a):
        """
        关键字 ： click
            自定表达式然后进行点击
        :param xpath: 定位元素表达式
        :return:
        """
        ele = self.find_elements(xpath, a)
        ele.click()

    def key_input(self, xpath, value, force=False):
        """
        关键字： input
            向指定的元素，输入内容
        :param xpath: 定位元素表达式
        :param value: 要输入的内容
        :param force: 通过js强制输入
        :return:
        """
        ele = self.find_element(xpath)
        # 可增加等待元素就绪后操作
        if force:  # 使用js强制输入
            self.driver.execute_script(f'arguments[0].value={value}', ele)
        else:
            ele.clear()
            ele.send_keys(value)

    def key_iframe(self, xpath):
        """
        进入到iframe页面
        :param xpath: 元素定位表达式
        :return:
        """
        ele = self.find_element(xpath)
        assert ele.tag_name == 'iframe'
        self.driver.switch_to.frame(ele)

    def key_iframe_exit(self):
        """
        退出当前iframe页面
        :param xpath:
        :return:
        """
        self.driver.switch_to.parent_frame()

    def key_iframe_top(self):
        """
        退出顶层iframe页面
        :param xpath:
        :return:
        """
        self.driver.switch_to.default_content()

    def key_get_text(self, xpath, var_name):
        """
        获取页面上的text内容
        :param var_name:
        :param xpath: 要保存的变量名
        :return:
        """
        ele = self.find_element(xpath)
        self.__vars[var_name] = ele.text
        print('断言实际结果是：', ele.text)

    def key_assert(self, value, assert_name, actual_value=''):
        """
        关键字断言
        :param value: 预期结果
        :param assert_name: 断言方法
        :param actual_value: 实结结果，支持字符串格式化的写法来使用变量{var}
        :return:
        """
        print('断言预期结果:', value)
        actual_value = actual_value.format_map(self.__vars)
        validator = Validator(value, assert_name, actual_value)
        assert validator.is_vaild() is True

    def key_screenshot(self, name):
        """
        截屏当前画面，附加到allure报告中
        :param name:
        :return:
        """
        allure.attach(
            self.driver.get_screenshot_as_png(),
            "截图",
            allure.attachment_type.PNG
        )


class Validator:

    def __init__(self, value, assert_name, actual_value):
        """
        :param value: 实际结果
        :param assert_name: 断言方法
        :param actual_value: 预期结果
        """
        self.value = value
        self.assert_name = assert_name
        self.actual_value = actual_value

    def is_vaild(self):
        """
        执行断言，如果返回True表示断言成功
        :return:
        """

        _assert = getattr(self, f'assert_{self.assert_name}')  # 反射断言方法
        _assert(self.value, self.actual_value)

        return True

    def assert_in(self, a, b):
        """
        断言 in a 在 b 中
        :param a:
        :param b:
        :return:
        """
        assert a in b

    def assert_contains(self, a, b):
        """
        断言 in a 包含 b
        :param a:
        :param b:
        :return:
        """
        assert b in a

    def assert_equal(self, a, b):
        """
        断言 in a 等于 b
        :param a:
        :param b:
        :return:
        """
        assert a == b

    def assert_not_equal(self, a, b):
        """
        断言 in a 不等于 b
        :param a:
        :param b:
        :return:
        """
        assert a != b
