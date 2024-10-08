# import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from datetime import datetime, timedelta
import requests
# import utils
import schedule
import config
import sys

# 问卷链接
url = config.url

# 每题选项的比例
prob = config.prob

# 填空题答案
answerList = config.answerList

# 填写份数
epochs = config.epochs

# IP API代提取链接
api = config.api

# UA库
UA = config.UA

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('--disable-gpu')
# ip = requests.get(api).text
# option.add_argument(f'--proxy-server={ip}')
# option.add_argument("--proxy-server=http://202.20.16.82:10152")
option.add_argument("--window-size=1920x1080")
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=option)

def task(btn):
    btn.click()
    time.sleep(1)
    driver.quit()
    sys.exit(0)

if __name__ == "__main__":

    for epoch in range(epochs):

        # driver = webdriver.Chrome(options=option)
        # 修改User-Agent
        num = 0
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": UA[num]})
        option.add_argument('user-agent={0}'.format(UA[num]))
        # 将webdriver属性置为undefined
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                               {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})

        driver.get(url)
        
        # 题号
        index = 1
        # 获取题目数量
        questions = driver.find_elements(By.CLASS_NAME, "field.ui-field-contain")
        for i in range(1, len(questions) + 1):
            # xpath = '//*[@id="div{}"]'.format(i)
            # question = driver.find_element(By.XPATH, xpath)
            time.sleep(1)
            if i == 1:
                xpath = '//*[@id="div1"]/div[2]/div[1]/span/a'
                ActionChains(driver).move_to_element(driver.find_element(By.XPATH, xpath)).click().perform()
            elif i == 2:
                xpath = '//*[@id="q{}"]'.format(i)
                driver.find_element(By.XPATH, xpath).send_keys("李明泽")
            elif i == 3:
                xpath = '//*[@id="q{}"]'.format(i)
                driver.find_element(By.XPATH, xpath).send_keys("华虹半导体无锡")
            elif i == 4:
                xpath = '//*[@id="q{}"]'.format(i)
                driver.find_element(By.XPATH, xpath).send_keys("15843805961")
            elif i == 5:
                # 获取当前日期和时间
                now = datetime.now()
                
                if now.hour < 1:
                	next_1am = now.replace(hour=1, minute=0, second=0, microsecond=0)
                else:
                	next_1am = (now + timedelta(days=1)).replace(hour=1, minute=0, second=0, microsecond=0)
                
                formatted_date = next_1am.strftime("%y年{}月{}日13时-15时").format(next_1am.month, next_1am.day)
                
                xpath = '//*[@id="q{}"]'.format(i)
                driver.find_element(By.XPATH, xpath).send_keys(formatted_date)
                
        time.sleep(1)

        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        # print("当前时间:", current_time)

        submit_button = driver.find_element(By.XPATH, '//*[@id="ctlNext"]')
        schedule_time = "01:00"  # 指定时间，格式为HH:MM
        schedule.every().day.at(schedule_time).do(task, submit_button)
        while True:
            schedule.run_pending()
        # submit_button.click()
        time.sleep(1)

        # # 请点击智能验证码进行验证！
        # try:
        #     comfirm = driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a')
        #     comfirm.click()
        #     time.sleep(1)
        # except Exception as e:
        #     print(e)

        # # 点击按钮开始智能验证
        # try:
        #     button = driver.find_element(By.XPATH, '//*[@id="SM_BTN_WRAPPER_1"]')
        #     button.click()
        #     time.sleep(0.5)
        # except Exception as e:
        #     print(e)

        # # 滑块验证
        # try:
        #     slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        #     time.sleep(0.3)
        #     if str(slider.text).startswith("请按住滑块，拖动到最右边"):
        #         width = slider.size.get('width')
        #         ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
        #         time.sleep(1)
        # except Exception as e:
        #     print(e)
        driver.quit()
        print("已完成{}份".format(epoch))
        
    print("全部完成{}份填写".format(epochs))
