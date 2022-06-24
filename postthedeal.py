from selenium import webdriver
import time
import os
# 创建浏览器对象,发请求
#System.setProperty("webdriver.chrome.driver", );


class WeiBoSpider11:
    def __init__(self):
        self.baseurl="https://login.sui.com/"


    def readcookies(self):
        print('开始')

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_experimental_option('useAutomationExtension', False)
        chromeOptions.add_argument('--no-sandbox') 
        chromeOptions.add_argument('headless')

        
        user_ag='MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; '+'CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
        chromeOptions.add_argument('user-agent=%s'%user_ag)

        driver = webdriver.Chrome(options= chromeOptions)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => False,
        })
         """
         })        
        aaa="https://www.sui.com/data/alipay.do"
               
        driver.get(self.baseurl)
        driver.get_screenshot_as_file('login.png')
        time.sleep(1)
        try:
            uname1 = driver.find_element_by_xpath('//div//input[@id="email"]')
            uname1.send_keys(13173026163)

            uname1 = driver.find_element_by_xpath('//div//input[@type="password"]')

            uname1.send_keys("3475495a")

            uname1 = driver.find_element_by_xpath('//a[@id="loginSubmit"]')
            uname1.click()
            time.sleep(2)
        except:
            pass
        asda=[]
        for root, dirs, files in os.walk(os.getcwd()+"/Class"):
            for a in files:

                if "csv" in a :
                    asda.append(a)
        for i in range(len(asda)):

            driver.get(aaa)
            driver.get_screenshot_as_file('login.png')    
            path=driver.find_element_by_xpath('//div//input[@type="file"]')
            path.send_keys(os.getcwd()+"/Class/"+asda[i])
            
            uname1 = driver.find_element_by_xpath('//input[@type="submit"]')
            uname1.click()
            time.sleep(1)
            driver.get_screenshot_as_file('login.png')  
            uname1 = driver.find_element_by_xpath('//div[@id="step2"]//div[@class="payout"]//div[@class="list-box"]//input')
            uname1.click()
            time.sleep(1)
            uname1 = driver.find_element_by_xpath('//div[@id="step2"]//div[@class="payout"]//div[@class="list-box"]//ul//li[@title='+'"'+asda[i][0:-4]+'"]')
            uname1.click()
            
            uname1 = driver.find_element_by_xpath('//div[@id="step2"]//div[@class="account"]//div[@class="list-box"]//input[@id="account1_input"]')
            uname1.click()
            time.sleep(1)
            uname1 = driver.find_element_by_xpath('//div[@id="step2"]//div[@class="account"]//div[@class="list-box"]//ul//li[@title="现金(CNY)"]')
            uname1.click()
            
            uname1 = driver.find_element_by_xpath('//a[@class="common-btn"]')
            uname1.click()
            time.sleep(1)

            uname1 = driver.find_element_by_xpath('//div[@id="confirm_model"]//div[@id="confirm_btn"]//a')
            uname1.click()
            time.sleep(1)
            print(asda[i][0:-4])
        #driver.get("https://api2.pushdeer.com/message/push?pushkey=PDU6037TrRIr4U3ijcEBbdItgZt2XVwDBcohruSs&text=上传完成")
        driver.quit()    
        print("点完拉到")
    def workon(self):

            
        self.readcookies()
#pinglun=driver.find_elements_by_xpath('//h3')
#for i in pinglun:

 #   print(i.text)
"""
# 获取截图(验证码)
#driver.save_screenshot("验证码.png")
# 找 用户名、密码、验证、登陆豆瓣按钮
#uname = driver.find_element_by_name("form_email")
#uname.send_keys("309435365@qq.com")
# 密码
pwd = driver.find_element_by_name("form_password")
pwd.send_keys("zhanshen001")
# 验证码
key = input("请输入验证码：")
yzm = driver.find_element_by_id("captcha_field")
yzm.send_keys(key)
driver.save_screenshot("完成.png")
# 点击登陆按钮
login = driver.find_element_by_class_name("bn-submit")
login.click()
time.sleep(1)
driver.save_screenshot("登陆成功.png")
"""

if __name__ == "__main__":
    spider11 = WeiBoSpider11()
    spider11.workon()
