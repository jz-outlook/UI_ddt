import logging
import time
import unittest
from pathlib import Path

import allure
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.service import Service
from webdriver_helper import get_webdriver

from libs import action
import ddt

logger = logging.getLogger(__name__)


class Runner:
    def __init__(self, case):
        self.case = case
        self.__name__ = case['info']['name']  # 对象的name属性会成为测试用例名的一部分


def creat_runner(case_list):
    """
    把test_case组成的列表，换回runner组成的列表
    :param case_list:
    :return:
    """
    new_list = []
    for case in case_list:  # 从旧的列表拿出case
        runner = Runner(case)  # 把case换成Runner
        new_list.append(runner)  # 把Runner 放进新的列表
    return new_list


def creat_test(test_suite, file):
    file_path = Path(file)  # 文件的路径
    filename = file_path.name  # 文件的名字

    @ddt.ddt
    @allure.suite(filename)
    class Test(unittest.TestCase):

        @classmethod
        def setUpClass(cls) -> None:
            service = Service(
                executable_path=r'C:\Users\zhang\.wdm\drivers\chromedriver\win32\99.0.4844.35\chromedriver.exe')
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('start-maximized')
            cls.driver = webdriver.Chrome(service=service, options=options)
            # cls.driver = get_webdriver() # 自动

        @classmethod
        def tearDownClass(cls) -> None:
            time.sleep(1)
            cls.driver.quit()

        @ddt.data(*creat_runner(test_suite['cases'].values()))  # 通过套件数据生成用例
        def test(self, runner):
            case = runner.case
            key_word = action.KeyWord(driver=self.driver)
            for step in case['steps']:
                print('步骤', step)  # 步骤 名称、关键字、参数

                @allure.step(step[1])
                def _f(关键字=step[2], 参数=step[3]):
                    f = getattr(key_word, f'key_{step[2]}')

                    try:
                        f(*step[3])
                    except Exception as e:
                        # 预期外的异常，使用error级别日志，自动记录异常信息
                        logger.error('关键字执行出错', exc_info=True)
                        raise e  # 异常捕获之后要继续抛出

                    # logger.info(f'关键字执行完成{step[2]}{step[3]}')
                    if (step[2] not in ['screenshot', 'assert', 'quit_session', 'new_session', 'mysql',
                                        'save_sql'] and key_word.is_close is False):  # 列表中的关键字不进行截图and浏览器关闭了不自动截图
                        try:
                            # 有对话框，切换成功
                            key_word.driver.switch_to.alert
                            logger.info('对话框切换成功，不进行截图')
                        except NoAlertPresentException:
                            # 切换失败，没有对话框，可以截图
                            # logger.info('条件满足，调用关键字:screenshot')
                            key_word.key_screenshot(step[1])  # 附件名称使用步骤名称

                _f()
                time.sleep(0.2)
            print('用例结束')

    return Test


class PytestExcel:
    def __init__(self, base_dir):
        """
        搜索excel目录
        :param base_dir:
        """
        self.base_dir = Path(base_dir)
        self.py_path = self.base_dir / 'test_ui.py'

    def put_py(self):
        """
        测试开始前创建一个py文件
        :return:
        """
        logger.info("创建测试文件")
        code = f"""
from libs import data, case
from glob import glob
import logging

logger = logging.getLogger(__name__)

file_list = glob(r"{self.base_dir.absolute()}\\test_*.xlsx")  # 搜索test_开头的文件

no = 0
for file in file_list:
    logger.info(f"第{{no}}个测试用例 正在创建。。（{{file}}）。。。")
    for suite in data.case_by_excel(file):  # 读取文件数据
        no += 1
        globals()[f"{{no}}_{{suite['info']['name']}}"] = case.creat_test(suite, file)  # 生成测试用例
logger.info(f"全部创建完成")
        """

        self.py_path.write_text(code, encoding='utf-8')
        logger.info("测试文件完成")

    def del_py(self):
        """
        测试结束后删除创建的py文件
        :return:
        """
        self.py_path.unlink(True)
