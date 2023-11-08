from multiprocessing import Process
from time import sleep
from flask import Flask,jsonify
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
import pandas as pd
# from db import connect_db
from dotenv import load_dotenv
import os
# from flask_cors import CORS
load_dotenv()
app = Flask(__name__)
# existing_data = pd.read_excel('data.xlsx')
# print(len(existing_data))
# new_data = pd.DataFrame({'No':[1,2],
#                         'Name': ["tom","smiss"],
#                         'Age': [23,44],
#                         'City': ["dd","bb"]})
# updated_data = pd.concat([existing_data, new_data])
# updated_data.to_excel('data.xlsx',index=False)
def _extracted_from_startScraping_8(chrome_options):
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options,
    )
    
    driver.get("https://www.yupao.com/")
    wait = WebDriverWait(driver, 500)
    login_element=wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div/div[2]')))
    sleep(20)
    actions=ActionChains(driver)
    actions.move_to_element(login_element)
    actions.click().perform()
    print("loading finished")
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR,"div[class=\'LoginPopup_login-model__n45M8\']")))
    categories=driver.find_elements(By.CSS_SELECTOR,"div[class=\'VVOccHMC_occItemRow__ZkbNl\']")
    print(len(categories))
    # front_page=driver.current_window_handle
    # for recruiter in recruiter_list:
    #     recruiter.click()
    #     recruiter_page=driver.window_handles[-1]
    #     sleep(10)
    #     driver.switch_to.window(recruiter_page)
    #     driver.find_element(By.CSS_SELECTOR,"div[class=\'ViewPhone_view-phone-btn__WPuCm\']").click()
    #     sleep(5)
    #     phonenumber_element=driver.find_element(By.CSS_SELECTOR,"div[class=\'GetPhoneTipsDialog_fictitious-tel__uKPpQ\']")
    #     phonenumber=phonenumber_element.text
    #     print(phonenumber)
    #     driver.switch_to.window(front_page)
    #     sleep(5)
# Configure the driver to use the Astrill VPN proxy
options = webdriver.ChromeOptions()
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--force-dark-mode")
chrome_options.add_argument("--start-maximized")


try:
    _extracted_from_startScraping_8(chrome_options)
except Exception as e:
        print(e)
