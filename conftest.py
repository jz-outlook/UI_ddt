import logging

from libs import case

"""
import os
os.environ['NO_COLOR'] = '1'  # 禁用日志颜色，日志乱码
"""

logger = logging.getLogger(__name__)
obj = case.PytestExcel(r'tests\excel')


# pytest hooks
def pytest_configure():
    """
    pytest 启动的时候执行
    :return:
    """
    logger.info("测试准备启动")
    obj.put_py()


def pytest_terminal_summary():
    """
    pytest 执行完成后执行
    :return:
    """
    obj.del_py()
