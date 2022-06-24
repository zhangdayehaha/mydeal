from selenium import webdriver
import time
import sys
import json
import re
import os
import random
import requests
import zipfile
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from p12 import Thedate
from postthedeal import WeiBoSpider11
from selenium.webdriver.support.wait import WebDriverWait
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from PIL import Image
#System.setProperty("webdriver.chrome.driver", );


class WeiBoSpider:
    def __init__(self):
        self.baseurl="https://auth.alipay.com/login/index.htm"
        self.cookies="0"
        self.username="179949437@qq.com"
        self.password="3475495aA"
        self.timestart = 0
        self.timeend = 0
        self.timeuse = 0
        self.yan=''
        self.session = requests.session()
    def send_mail(self,iamgename):
    
        # 发送邮箱服务器
        smtp_server = 'smtp.163.com'
        # 发送邮箱用户名密码
        user = 'a782464270@163.com'
        password = 'WRNYCGPQRBOSUNOD'

        # 接收邮箱
        receives = ['782464270@qq.com']

        # 发送邮件和主题内容
        subject = '异常警告'
        content = '<html><h1 style="color:red">测试邮件发送</h1></html>'

        # 构建发送与接收信息
        msg_root = MIMEMultipart()
        msg_root.attach(MIMEText(content, 'html', 'utf-8'))
        msg_root['subject'] = subject
        msg_root['From'] = user
        msg_root['To'] = ','.join(receives)
        file = open(iamgename, "rb")
        img_data = file.read()
        file.close()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', 'imageid')
        msg_root.attach(img)

        # SSL协议端口号要使用465
        smtp = smtplib.SMTP_SSL(host='smtp.163.com')
        smtp.connect(smtp_server, 465)
        # H E L O 向服务器标识用户身份
        smtp.helo(smtp_server)
        # 服务器返回结果确认
        smtp.ehlo(smtp_server)
        # 登录邮箱服务器用户名和密码
        smtp.login(user, password)

  

        smtp.sendmail(user, receives, msg_root.as_string())

        smtp.quit()
    def readcookies(self):
                
        chromeOptions = webdriver.ChromeOptions()

        print("启动支付宝页面")
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.getcwd()+"/dan"}
        chromeOptions.add_experimental_option('prefs', prefs)

        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_experimental_option('useAutomationExtension', False)
        chromeOptions.add_argument('headless')
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-dev-shm-usage')


        driver = webdriver.Chrome(options = chromeOptions)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
          "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
            })    
        self.entrypage(driver)
    def entrypage(self,driver):


        self.pasepage(driver)


    def pasepage(self,driver):

        
        
        driver.get(self.baseurl)
        print("截下二维码")
        driver.get_screenshot_as_file('login.png')

        #uname = driver.find_element_by_xpath('//div[@class]//a[starts-with(text(), "快速登录")]')
        #driver.execute_script("arguments[0].click();", uname )
        
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-dev-shm-usage') 
        

        
        
        
        bg1 = Image.open('login.png')
        
        
        crop = bg1.crop((350,200, 620,400))

        crop.save(('loginsmall.png'))
        self.send_mail('loginsmall.png')
        
        '''#driver2 = webdriver.Chrome(options= chromeOptions)'''
        '''
        driver2.get("https://www.niupic.com/")
        
        path=driver2.find_element_by_xpath('//div[@class="home-buttons"]/a')
        path.click()
        path.send_keys(os.getcwd()+"/loginsmall.jpg")    
        time.sleep(2)        
        uname = driver2.find_element_by_xpath('//div[@class="input-group-btn input-group-append"]//a[@class="btn btn-info fileinput-upload fileinput-upload-button"]')
        driver2.execute_script("arguments[0].click();", uname )
        #uname.click()
        time.sleep(10)
        driver2.get_screenshot_as_file('geiurl.png')
        while True:
            
            uname = driver2.find_elements_by_xpath('//div[@class="dlinput_container"]//div[@class="col-md-8"]//input')
            if uname:
                
                urll=uname[len(uname)-2].get_attribute("value")
                deurll=uname[len(uname)-1].get_attribute("value")
                break
            else:
                pass
        '''
        '''driver2.get("https://api2.pushdeer.com/message/push?pushkey=PDU6037TrRIr4U3ijcEBbdItgZt2XVwDBcohruSs&text=扫描二维码")
        
        driver2.quit()'''
        print("发送二维码")
        
        while True:
            
            try:
                
                uname = driver.find_element_by_xpath('//div[@class="global"]//ul[@class]//li[@class="global-nav-item "]//a')
                  
                driver.execute_script("arguments[0].click();", uname )
                break
            except Exception as  e:
                print(e)
                driver.get_screenshot_as_file('index6.png')
                time.sleep(1)
                pass
        time.sleep(5)
        print("找到交易记录并点击")
        while True:
            
            try:
                
                uname = driver.find_element_by_xpath('//div[@class="fn-left"]//a[@class]')
                time.sleep(1)
                driver.get_screenshot_as_file('index.png')
                driver.execute_script("arguments[0].click();", uname )
                break
            except Exception as  e:
                print(e)
                driver.get_screenshot_as_file('index.png')
                driver.get("https://consumeprod.alipay.com/record/standard.htm")
                time.sleep(2)
                driver.get_screenshot_as_file('index1.png')
                
                pass
        time.sleep(5)
        print("找到下载按钮")
        try:
            
            iframe = driver.find_element_by_xpath('//div//iframe[@frameborder="no"]')
            print("开始转换")
            driver.switch_to.frame(iframe) 
            uname = driver.find_element_by_xpath('//div//span[@class="ui-button ui-button-morange"]//input')
            print("转换完成")
            driver.get_screenshot_as_file('login2.png')
            if(uname.is_displayed()):
                time.sleep(1)
                uname.click()
            else:
                
                print(hahazmzajg)
        except:
            print("需要第二次验证")
            time.sleep(10)
            driver.get_screenshot_as_file('login2.png')
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--headless")
            #driver2 = webdriver.Chrome(chrome_options = chromeOptions)
            #driver2.get("https://sm.ms/")
            bg1 = Image.open('login2.png')
            
            
            crop = bg1.crop((300,200, 520,400))

            crop.save(('loginsmall2.png'))
            '''
            path=driver2.find_element_by_xpath('//div[@tabindex]//input[@id]')
            path.send_keys(os.getcwd()+"/login2small.jpg")    
            time.sleep(2)        
            uname = driver2.find_element_by_xpath('//div[@class="input-group-btn input-group-append"]//a[@class="btn btn-info fileinput-upload fileinput-upload-button"]')
            driver2.execute_script("arguments[0].click();", uname )
            #driver2.execute_script("arguments[0].click();", uname )
            time.sleep(10)

            
            uname = driver2.find_elements_by_xpath('//div[@class="dlinput_container"]//div[@class="col-md-8"]//input')
            
            urll=uname[len(uname)-2].get_attribute("value")
            deurll=uname[len(uname)-1].get_attribute("value")
            '''
            self.send_mail('loginsmall2.png')
            #driver2.get("https://api2.pushdeer.com/message/push?pushkey=PDU6037TrRIr4U3ijcEBbdItgZt2XVwDBcohruSs&text=需要再次扫描二维码")
            
            
            #driver2.quit()
        zipname=""
        print("等待下载完成")
        while True:
            try:
                
                iframe = driver.find_element_by_xpath('//div//iframe[@scrolling="no"]')

                driver.switch_to_frame(iframe) 
                uname = driver.find_element_by_xpath('//div//span[@class="ui-button ui-button-morange"]//input')

                if(uname.is_displayed()):
                    time.sleep(1)
                    uname.click()
            except:
                
                for root, dirs, files in os.walk(os.getcwd()+"/dan"):
                    for a in files:
                        if "zip" in a[-3:] and "alip" in a:
                            zipname=a
                if zipname !="":
                    print(zipname)
                    break

            
        

            
        
        frzip = zipfile.ZipFile("./dan/"+zipname, 'r', zipfile.ZIP_DEFLATED)
        extractfile = frzip.namelist()
        frzip.extract(member=extractfile[0],path=os.getcwd()+"/dan",pwd=None)
        frzip.close()
        os.remove("./dan/"+zipname)
        lis = Thedate()
        session = requests.session()
        url = "http://www.pushplus.plus/send"
        daye={
                "token":"ba36ec49e30c4fb6ba875f7630937e4b",
                "title":"本月消费",
                "content":lis,
                "channel":"cp",
                "webhook":"1008"
            }

        resps22 = self.session.post(url=url, data= daye)
        spider11 = WeiBoSpider11()
        spider11.workon()
    def workon(self):

            
        self.readcookies()
	
if __name__ == "__main__":
    spider = WeiBoSpider()
    spider.workon()
