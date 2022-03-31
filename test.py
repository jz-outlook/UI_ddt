from pprint import pprint

from libs import data, case
from glob import glob

file_list = glob("tests/excel/test_*.xlsx")  # 搜索test_开头的文件

no = 0
for file in file_list:
    for suite in data.case_by_excel(file):  # 读取文件数据
        no += 1
        globals()[f'Test{no}'] = case.creat_test(suite)  # 生成测试用例

    # print('测试套件', suite['info'])
    # for case in suite['cases'].values():
    #     print('    测试用例', case['info'])
    #
    #     for step in case['steps']:
    #         print('        步骤', step)
    #
    # print('测试套件结束', '-' * 10)















