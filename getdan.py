# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import json
import re
import os
import random
import requests
import zipfile
from selenium.webdriver.chrome.options import Options
from p12 import Thedate
from postthedeal import WeiBoSpider11
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from PIL import Image

class WeiBoSpider:
    def __init__(self):
        self.baseurl = "https://auth.alipay.com/login/index.htm"
        self.cookies = "0"
        self.username = "179949437@qq.com"
        self.password = "3475495aA"
        self.timestart = 0
        self.timeend = 0
        self.timeuse = 0
        self.yan = ''
        self.session = requests.session()
        self.patchfile = '/root/文档/zhangdan'

    def send_mail(self, iamgename):
        # 保持原有邮件发送逻辑完全不变
        smtp_server = 'smtp.163.com'
        user = 'a782464270@163.com'
        password = 'WOTQGZBXVGIKNUBV'
        receives = ['782464270@qq.com']

        msg_root = MIMEMultipart()
        msg_root.attach(MIMEText('Body of the email. <img src="cid:imageid">', 'html', 'utf-8'))
        msg_root['Subject'] = '异常警告'
        msg_root['From'] = user
        msg_root['To'] = ','.join(receives)

        with open(iamgename, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', 'imageid')
            msg_root.attach(img)

        with open(iamgename, 'rb') as f:
            img2 = MIMEImage(f.read())
        img2.add_header('Content-Disposition', 'attachment', filename='image.jpg')
        msg_root.attach(img2)

        with smtplib.SMTP_SSL(host='smtp.163.com') as smtp:
            smtp.connect(smtp_server, 465)
            smtp.login(user, password)
            smtp.sendmail(user, receives, msg_root.as_string())

    def readcookies(self):
        # 完整保留原始浏览器配置
        chrome_options = Options()
        print("启动支付寶頁面，os.getcwd()")
        prefs = {
            'profile.default_content_settings.popups': 0, 
            'download.default_directory': self.patchfile + "/dan"
        }
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--log-level=3")
        
        # 更新Service初始化方式
        service = Service(executable_path='/root/文档/zhangdan/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 保留防检测脚本
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
        })
        self.entrypage(driver)

    def entrypage(self, driver):
        self.pasepage(driver)

    def pasepage(self, driver):
        # 完整页面加载流程
        driver.get(self.baseurl)
        print("截取二维码")
        driver.save_screenshot('login.png')

        # 保持原有图片处理逻辑
        bg1 = Image.open('login.png')
        crop = bg1.crop((350, 200, 620, 400))
        crop.save('loginsmall.png')
        self.send_mail('loginsmall.png')

        # 完整保留第一个循环点击逻辑
        print("发送二维碼")
        while True:
            try:
                element = driver.find_element(By.XPATH, '//div[@class="global"]//ul[@class]//li[@class="global-nav-item "]//a')
                driver.execute_script("arguments[0].click();", element)
                break
            except Exception as e:
                print(e)
                driver.save_screenshot('index6.png')
                time.sleep(1)

        # 完整保留交易记录点击逻辑
        print("找到交易记录并点击")
        while True:
            try:
                element = driver.find_element(By.XPATH, '//div[@class="fn-left"]//a[@class]')
                time.sleep(1)
                driver.save_screenshot('index.png')
                driver.execute_script("arguments[0].click();", element)
                break
            except Exception as e:
                print(e)
                driver.get("https://consumeprod.alipay.com/record/standard.htm")
                time.sleep(2)
                driver.save_screenshot('index1.png')

        # 完整二次验证处理逻辑
        print("找到下载按钮")
        try:
            iframe = driver.find_element(By.XPATH, '//div//iframe[@frameborder="no"]')
            print("开始转换")
            driver.switch_to.frame(iframe)
            element = driver.find_element(By.XPATH, '//div//span[@class="ui-button ui-button-morange"]//input')
            print("转换完成")
            driver.save_screenshot('login2.png')
            if element.is_displayed():
                time.sleep(1)
                element.click()
            else:
                print("元素不可见")  # 保留原始错误触发逻辑
                print("需要二次验证")
                time.sleep(10)
                driver.save_screenshot('login2.png')
                # 完整保留二次验证截图处理
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                bg1 = Image.open('login2.png')
                crop = bg1.crop((300, 200, 520, 400))
                crop.save('loginsmall2.png')
                self.send_mail('loginsmall2.png')
        except Exception as e:
            print("需要二次验证", e)
            time.sleep(10)
            driver.save_screenshot('login2.png')
            # 完整保留二次验证截图处理
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            bg1 = Image.open('login2.png')
            crop = bg1.crop((300, 200, 520, 400))
            crop.save('loginsmall2.png')
            self.send_mail('loginsmall2.png')

        # 完整文件等待逻辑
        print("等待下载完成")
        zipname = ""
        while True:
            try:
                iframe = driver.find_element(By.XPATH, '//div//iframe[@scrolling="no"]')
                driver.switch_to.frame(iframe)
                element = driver.find_element(By.XPATH, '//div//span[@class="ui-button ui-button-morange"]//input')
                if element.is_displayed():
                    element.click()
            except:
                for root, dirs, files in os.walk(self.patchfile + "/dan"):
                    for a in files:
                        if "zip" in a[-3:] and "alip" in a:
                            zipname = a
                if zipname != "":
                    print("找到压缩包:", zipname)
                    break

        # 完整文件处理逻辑
        frzip = zipfile.ZipFile(os.path.join(self.patchfile, "dan", zipname), 'r')
        extractfile = frzip.namelist()
        frzip.extract(member=extractfile[0], path=os.path.join(self.patchfile, "dan"))
        frzip.close()
        os.remove(os.path.join(self.patchfile, "dan", zipname))

        # 最终数据提交
        lis = Thedate()
        url = "http://www.pushplus.plus/send"
        daye = {
            "token": "ba36ec49e30c4fb6ba875f7630937e4b",
            "title": "本月消费",
            "content": lis,
            "channel": "cp",
            "webhook": "1008"
        }
        self.session.post(url=url, data=daye)
        spider11 = WeiBoSpider11()
        spider11.workon()

    def workon(self):
        self.readcookies()

if __name__ == "__main__":
    spider = WeiBoSpider()
    spider.workon()