from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# 创建一个类，其中包含了登入、登入“一体化教学服务中心”、转换窗口、登入评教系统的函数，并且初始化中赋值给driver = webdriver.Chrome()

driver = webdriver.Chrome()
# 设置隐式等待时间为20秒
# driver.implicitly_wait(20)
driver.maximize_window()

# 登入WEBVPN网页函数
# 打开网页
driver.get('https://webvpn.bit.edu.cn/')

# 找到一个按钮并点击它
username = driver.find_element_by_id('username')
password = driver.find_element_by_id('password')

# 输入用户名和密码
username.send_keys('1120202353')
password.send_keys('thy123')

# 点击对应元素
button = driver.find_element_by_id('login_submit')
button.click()
time.sleep(1.5)

# 登入“一体化教学服务中心”函数
# 通过对应元素<div>中的data-title进行查找点击
element = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[7]/div[15]/div/div[2]/p[1]")
# 滑动页面找到该元素并点击
driver.execute_script("arguments[0].scrollIntoView();", element)
time.sleep(1.5)
driver.execute_script("arguments[0].click();", element)

# 转换窗口函数
# 获取所有窗口的句柄
all_handles = driver.window_handles
# 获取新窗口的句柄，假设它是最后一个窗口
new_window_handle = all_handles[-1]
# 切换到新窗口
driver.switch_to.window(new_window_handle)
time.sleep(1)

# 登入评教系统
# 通过class进行查找点击
element = driver.find_element_by_class_name("block3")
time.sleep(1)
element.click()

# 通过元素id进行查找点击
element = driver.find_element_by_id("submot")
element.click()

# 转换窗口函数
# 获取所有窗口的句柄
all_handles = driver.window_handles
# 获取新窗口的句柄，假设它是最后一个窗口
new_window_handle = all_handles[-1]
# 切换到新窗口
driver.switch_to.window(new_window_handle)

# 初始化计数器
count = 1
# 初始化页码计数器
page = 0
# 临时页码计数器
temp_page = page

while True:
    # 回到默认的上下文
    driver.switch_to.default_content()

    # 等待 iframe 完全加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[@src="stpj/queryListStpj"]'))
    )

    # 获取 iframe 元素并切换
    iframe = driver.find_element_by_xpath('//iframe[@src="stpj/queryListStpj"]')
    driver.switch_to.frame(iframe)

    # 如果层数计数器大于0，点击"下一页"到达正确的页面
    if temp_page > 0:
        temp_page -= 1
        next_page_link = driver.find_element_by_xpath(
            '/html/body/div/div/div/div/div/form[1]/div/table/tbody/tr/td/div/ul/li[8]/a')
        next_page_link.click()
        time.sleep(0.5)
        continue

    # 获取<tbody>元素下的所有<tr>元素
    tr_elements = driver.find_elements_by_xpath('//table[@id="table_report"]/tbody/tr')

    # 如果计数器大于10或者超过了<tr>元素的数量，就点击下一页链接
    if count > len(tr_elements):
        next_page_link = driver.find_element_by_xpath(
            '/html/body/div/div/div/div/div/form[1]/div/table/tbody/tr/td/div/ul/li[8]/a')
        # 判断下页链接是否包含 onclick 属性
        if next_page_link.get_attribute('onclick'):
            # 如果有 onclick 属性，点击下一页链接
            next_page_link.click()
            time.sleep(0.5)
            # 重置计数器
            count = 1
            page += 1
            temp_page = page
            continue
        else:
            # 否则，跳出循环
            break

    # 在每次循环开始时，重新获取当前<tr>元素
    tr = tr_elements[count - 1]
    # tr = driver.find_element_by_xpath(f'(//table[@id="table_report"]/tbody/tr)[{count}]')

    try:
        # 尝试在这个<tr>元素中找到指定的<a>元素
        a_element = tr.find_element_by_xpath(".//a[contains(@class, 'btn btn-mini btn-purple')]")

        # 在<a>元素中找到<i>元素，并获取它的文本
        i_text = a_element.find_element_by_xpath(".//i").text

        # 如果<i>元素的文本不是 "查看"，并且<a>元素可点击，那么就点击这个元素
        if i_text == "评教":
            a_element.click()
            time.sleep(0.5)

            # 进行相应课程的评教
            # 循环点击按钮
            for i in range(1, 10):  # 假设id从pjnr_1_1到pjnr_9_1
                button_id = f"pjnr_{i}_1"
                button = driver.find_element_by_id(button_id)
                if button.is_enabled() and button.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    button.click()
                    time.sleep(0.5)

            # 在文本区域输入"无"
            text_area = driver.find_element_by_id("pjjy")
            text_area.clear()
            text_area.send_keys("无")

            # 点击提交按钮
            submit_button = driver.find_element_by_xpath(
                "/html/body/div/div[1]/div/div/form/div/div[2]/div[2]/div[11]/a[1]")
            submit_button.click()
            time.sleep(1)

            # 点击确定按钮
            confirm_button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/a')
            confirm_button.click()
            time.sleep(1)

        # 结束这次循环，因为页面状态已经改变
        count += 1

    except NoSuchElementException:
        # 如果这个<tr>元素中没有找到指定的<a>元素或<i>元素，那么就向运行日记输出该元素没有寻找到
        print(f"第 {count} 个<tr>元素中没有找到指定的<a>元素或<i>元素")
        count += 1
        continue

# 清除所有cookies
driver.delete_all_cookies()
# 延迟确保所有的cookies都已被删除
time.sleep(2)
# 退出浏览器
driver.quit()
