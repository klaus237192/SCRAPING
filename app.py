from multiprocessing import Process
from time import sleep
from flask import Flask,jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
# from db import connect_db
from dotenv import load_dotenv
import os
# from flask_cors import CORS
load_dotenv()
app = Flask(__name__)

def _extracted_from_startScraping_8(chrome_options):
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options,
    )
    
    browser.get("https://www.yupao.com/")
    print("loading finished")
    sleep(22)
    browser.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div/div/div[2]").click()
    sleep(80)
    recruiter_list=browser.find_elements(By.CSS_SELECTOR,"div[class=\'RecruitCardList_recruit-card-list__dFqyr\']>div")
    front_page=browser.current_window_handle
    for recruiter in recruiter_list:
        recruiter.click()
        recruiter_page=browser.window_handles[-1]
        sleep(10)
        browser.switch_to.window(recruiter_page)
        browser.find_element(By.CSS_SELECTOR,"div[class=\'ViewPhone_view-phone-btn__WPuCm\']").click()
        sleep(5)
        phonenumber_element=browser.find_element(By.CSS_SELECTOR,"div[class=\'GetPhoneTipsDialog_fictitious-tel__uKPpQ\']")
        phonenumber=phonenumber_element.text
        print(phonenumber)
        browser.switch_to.window(front_page)
        sleep(5)
# Configure the browser to use the Astrill VPN proxy
options = webdriver.ChromeOptions()
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--force-dark-mode")
chrome_options.add_argument("--window-size=1024,768")


try:
    _extracted_from_startScraping_8(chrome_options)
except Exception as e:
        print(e)
