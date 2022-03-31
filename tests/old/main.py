"""
脚本名称：ceshi

步骤：
- 打开URL:https://admin.test.tiger-sec.cn:9000
- 输入用户名
- 输入密码
- 点击登录
# """
# from selenium.webdriver.common.by import By
# from webdriver_helper import *
#
# driver = get_webdriver()
# driver.get("https://admin.test.tiger-sec.cn:9000")
# driver.find_element(By.ID, 'normal_login_username').send_keys('admin')
# driver.find_element(By.ID, 'normal_login_password').send_keys('Hy123!!!')
# driver.find_element(By.XPATH, "//button[contains(.,'登 录')]").click()
#
# msg = driver.current_url
# assert msg == 'https://admin.test.tiger-sec.cn:9000/login'


# 字符串格式化
# a = 123
# b = f"aaa{a}"
# print(b)


import MySQLdb

db = MySQLdb.connect(
    host='192.168.2.101',
    port=3306,
    user='tigersec',
    password='tigersec',
    database='tigersec'
)

sql = 'SELECT `name` FROM `user`'
c = db.cursor()  # 游标，数据库的会话
c.execute(sql)

db.commit()

result = c.fetchone()
print(result)
