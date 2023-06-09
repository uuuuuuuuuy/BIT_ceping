from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


# 创建一个类，其中包含了转换窗口、登入webvpn、登入“一体化教学服务中心”、登入评教系统、进行评教和退出浏览器的函数
class Login(object):
    # 完善初始化函数
    def __init__(self, username, password):
        self.username = username
        self.password = password

        # 初始化
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def quit(self):
        # 清除所有cookies
        self.driver.delete_all_cookies()
        # 延迟确保所有的cookies都已被删除
        time.sleep(2)
        # 退出浏览器
        self.driver.quit()

    # 登入WEBVPN网页函数
    def login_webvpn(self):
        # 打开网页
        try:
            self.driver.get('https://webvpn.bit.edu.cn/')
        except WebDriverException as e:
            html = self.driver.page_source
            if "无法访问此网站" in html:
                # return = 1表示网络错误，打不开网页
                return 1
            # return = 2表示其他原因，打不开网页
            return 2

        # 找到一个按钮并点击它
        username = self.driver.find_element_by_id('username')
        password = self.driver.find_element_by_id('password')

        # 输入用户名和密码
        username.send_keys(self.username)
        password.send_keys(self.password)

        # 点击对应元素
        button = self.driver.find_element_by_id('login_submit')
        current_url = self.driver.current_url
        current_title = self.driver.title
        button.click()
        time.sleep(1.5)

        # 检查是否加载了新页面
        new_url = self.driver.current_url
        new_title = self.driver.title
        if current_url == new_url and current_title == new_title:
            # 没有加载新页面，检查是否出现指定元素
            try:
                error_tip = self.driver.find_element_by_id('showErrorTip')
                if error_tip:
                    # return3表示用户名或密码错误，打不开网页
                    return 3
            except NoSuchElementException:
                # return 2表示其他原因，打不开网页
                return 2

        # return0表示登入成功
        return 0

    # 登入“一体化教学服务中心”函数
    def login_jxfwzx(self):
        # 通过对应元素<div>中的data-title进行查找点击
        element = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[7]/div[15]/div/div[2]/p[1]")
        # 滑动页面找到该元素并点击
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1.5)
        self.driver.execute_script("arguments[0].click();", element)

    # 转换窗口函数
    def switch_window(self):
        # 获取所有窗口的句柄
        all_handles = self.driver.window_handles
        # 获取新窗口的句柄，假设它是最后一个窗口
        new_window_handle = all_handles[-1]
        # 切换到新窗口
        self.driver.switch_to.window(new_window_handle)
        time.sleep(1)

    # 登入评教系统
    def login_pjxt(self):
        # 通过class进行查找点击
        element = self.driver.find_element_by_class_name("block3")
        time.sleep(1)
        element.click()

        # 通过元素id进行查找点击
        element = self.driver.find_element_by_id("submot")
        element.click()

    # 点击评教按钮函数
    def pj(self, count=1, page=1):
        # 临时页码计数器
        temp_page = page

        while True:
            # 回到默认的上下文
            self.driver.switch_to.default_content()

            # 等待 iframe 完全加载
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//iframe[@src="stpj/queryListStpj"]'))
            )

            # 定位到相应的iframe
            iframe = self.driver.find_element_by_xpath('//iframe[@src="stpj/queryListStpj"]')
            self.driver.switch_to.frame(iframe)

            # 如果临时页码计数器大于0，点击"下一页"到达正确的页面
            if temp_page > 1:
                temp_page -= 1
                next_page_link = self.driver.find_element_by_xpath(
                    '/html/body/div/div/div/div/div/form[1]/div/table/tbody/tr/td/div/ul/li[8]/a')
                next_page_link.click()
                time.sleep(0.5)
                continue

            # 获取<tbody>元素下的所有<tr>元素
            tr_elements = self.driver.find_elements_by_xpath('//table[@id="table_report"]/tbody/tr')

            # 如果计数器大于10或者超过了<tr>元素的数量，就点击下一页链接
            if count > len(tr_elements):
                next_page_link = self.driver.find_element_by_xpath(
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
                        button = self.driver.find_element_by_id(button_id)
                        if button.is_enabled() and button.is_displayed():
                            self.driver.execute_script("arguments[0].scrollIntoView();", button)
                            button.click()
                            time.sleep(0.5)

                    # 在文本区域输入"无"
                    text_area = self.driver.find_element_by_id("pjjy")
                    text_area.clear()
                    text_area.send_keys("无")

                    # 点击提交按钮
                    submit_button = self.driver.find_element_by_xpath(
                        "/html/body/div/div[1]/div/div/form/div/div[2]/div[2]/div[11]/a[1]")
                    submit_button.click()
                    time.sleep(1)

                    # 点击确定按钮
                    confirm_button = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/a')
                    confirm_button.click()
                    time.sleep(1)

                # 结束这次循环，因为页面状态已经改变
                count += 1

            except NoSuchElementException:
                # 如果这个<tr>元素中没有找到指定的<a>元素或<i>元素，那么就向运行日记输出该元素没有寻找到
                print(f"第 {count} 个<tr>元素中没有找到指定的<a>元素或<i>元素")
                count += 1
                continue


class LoginApp(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew") # use grid layout for this Frame
        self.create_widgets()
        self.master.title("Login")
        self.master.geometry("300x300")
        self.master.configure(background='light grey')

        # Center the window
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        position_right = int(self.master.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 2 - window_height / 2)
        self.master.geometry("+{}+{}".format(position_right, position_down))

    def create_widgets(self):
        # Load the logos
        logo1 = self.resize("logo/logo_01.png", 10)
        logo2 = self.resize("logo/logo_02.jpg", 5)

        logo_label1 = ttk.Label(self, image=logo1)
        logo_label1.image = logo1  # keep a reference!
        logo_label1.grid(row=5, column=0, rowspan=3, sticky="w")

        logo_label2 = ttk.Label(self, image=logo2)
        logo_label2.image = logo2  # keep a reference!
        logo_label2.grid(row=4, column=4, rowspan=2, sticky="e")

        username_label = ttk.Label(self, text="Username:")
        username_label.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

        password_label = ttk.Label(self, text="Password:")
        password_label.grid(row=4, column=1, columnspan=3, padx=10, pady=10)

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=5, column=1, columnspan=3, padx=10, pady=10)

        login_button = ttk.Button(self, text="Login", command=self.login)
        login_button.grid(row=6, column=1, padx=10, pady=10)

        quit_button = ttk.Button(self, text="QUIT", command=self.master.destroy)
        quit_button.grid(row=6, column=3, padx=10, pady=10)

    # 创建一个等比缩放的函数
    def resize(self, photo, ratio):
        # Load the logo image
        logo_image = Image.open(photo)

        # Resize the image proportionally
        new_width = int(logo_image.width / ratio)
        new_height = int(logo_image.height / ratio)
        logo_image = logo_image.resize((new_width, new_height), Image.LANCZOS)

        logo = ImageTk.PhotoImage(logo_image)

        return logo

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            # 创建一个登录对象
            login = Login(username, password)

            # 登录教务系统
            login_result = login.login_webvpn()
            if login_result == 1:
                messagebox.showerror("Error", "错误1: 网络错误，打不开网页")
                login.quit()
                return
            elif login_result == 2:
                messagebox.showerror("Error", "错误2: 其他原因，打不开网页")
                login.quit()
                return
            elif login_result == 3:
                messagebox.showerror("Error", "错误3: 用户名或密码错误，打不开网页")
                login.quit()
                return

            # 登录“一体化教学服务中心”
            login.login_jxfwzx()

            # 转换窗口
            login.switch_window()
            # 登录评教系统
            login.login_pjxt()

            # 转换窗口
            login.switch_window()
            # 点击评教按钮
            login.pj()

            # 退出浏览器
            login.quit()
            messagebox.showinfo("Success", "评教完成！")
        else:
            messagebox.showerror("Error", "请输入用户名和密码！")


def main():
    root = tk.Tk()
    app = LoginApp(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()

