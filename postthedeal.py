from selenium import webdriver
from selenium.webdriver.common.by import By  # 新增By模块
import time
import os

class WeiBoSpider11:
    def __init__(self):
        self.baseurl = "https://login.sui.com/"
        self.patchfile = '/root/文档/zhangdan'

    def readcookies(self):
        print('开始')

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_experimental_option('useAutomationExtension', False)
        chromeOptions.add_argument('--no-sandbox') 
        chromeOptions.add_argument('headless')

        user_ag = 'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; '+'CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
        chromeOptions.add_argument(f'user-agent={user_ag}')

        driver = webdriver.Chrome(options=chromeOptions)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => False
            })
            """
        })        
        aaa = "https://www.sui.com/data/alipay.do"
        
        driver.get(self.baseurl)
        driver.get_screenshot_as_file('login.png')
        time.sleep(1)
        
        try:
            # 更新所有find_element_by_xpath为新的写法
            uname1 = driver.find_element(By.XPATH, '//div//input[@id="email"]')
            uname1.send_keys(13173026163)

            uname1 = driver.find_element(By.XPATH, '//div//input[@type="password"]')
            uname1.send_keys("3475495a")

            uname1 = driver.find_element(By.XPATH, '//a[@id="loginSubmit"]')
            uname1.click()
            time.sleep(2)
        except Exception as e:
            print(f"登录时发生错误: {e}")
        
        asda = []
        for root, dirs, files in os.walk(self.patchfile + "/Class"):
            for a in files:
                if "csv" in a:
                    asda.append(a)
        
        for i in range(len(asda)):
            driver.get(aaa)
            driver.get_screenshot_as_file('login.png')    
            
            # 更新文件上传元素的定位
            path = driver.find_element(By.XPATH, '//div//input[@type="file"]')
            path.send_keys(self.patchfile + "/Class/" + asda[i])
            
            uname1 = driver.find_element(By.XPATH, '//input[@type="submit"]')
            uname1.click()
            time.sleep(1)
            
            driver.get_screenshot_as_file('login.png')  
            uname1 = driver.find_element(By.XPATH, '//div[@id="step2"]//div[@class="payout"]//div[@class="list-box"]//input')
            uname1.click()
            time.sleep(1)
            
            uname1 = driver.find_element(By.XPATH, f'//div[@id="step2"]//div[@class="payout"]//div[@class="list-box"]//ul//li[@title="{asda[i][0:-4]}"]')
            uname1.click()
            
            uname1 = driver.find_element(By.XPATH, '//div[@id="step2"]//div[@class="account"]//div[@class="list-box"]//input[@id="account1_input"]')
            uname1.click()
            time.sleep(1)
            
            uname1 = driver.find_element(By.XPATH, '//div[@id="step2"]//div[@class="account"]//div[@class="list-box"]//ul//li[@title="现金(CNY)"]')
            uname1.click()
            
            uname1 = driver.find_element(By.XPATH, '//a[@class="common-btn"]')
            uname1.click()
            time.sleep(1)

            uname1 = driver.find_element(By.XPATH, '//div[@id="confirm_model"]//div[@id="confirm_btn"]//a')
            uname1.click()
            time.sleep(1)
            print(asda[i][0:-4])
        
        # driver.get("https://api2.pushdeer.com/message/push?pushkey=PDU6037TrRIr4U3ijcEBbdItgZt2XVwDBcohruSs&text=上传完成")
        driver.quit()    
        print("操作完成")

    def workon(self):
        self.readcookies()

if __name__ == "__main__":
    spider11 = WeiBoSpider11()
    spider11.workon()