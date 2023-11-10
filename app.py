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
import re

from dotenv import load_dotenv
import os
# from flask_cors import CORS
load_dotenv()
app = Flask(__name__)


def _extracted_from_startScraping_8(chrome_options):
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options,
    )
    try:
        driver.get("https://www.yupao.com/")
        driver.execute_script("document.charset='UTF-8';")


        #waiting until login button is prepared for clicking
        wait = WebDriverWait(driver, 500)
        login_element=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\'Header_header-topbar-content-right__Etq2J\']")))
        print("--------------Ready for clicking-----------------")
        sleep(20)


        #login button clicking
        actions=ActionChains(driver)
        actions.move_to_element(login_element)
        actions.click().perform()
        print("--------------Login modal is displayed.Please login manually------------")


        #wainting until getting verification code from client and being invisible the login modal
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR,"div[class=\'LoginPopup_login-model__n45M8\']")))
       
       
        #getting all job categories
        categories=driver.find_elements(By.CSS_SELECTOR,"div[class=\'VVOccHMC_occHMCBox__Zy8oj\']")
        del categories[0]
        print("-------------->The count of categories\n", len(categories))
       
       
        #---------------------------------------------------------Starting Scraping--------------------------------------------------------------------------
        
        No = []
        City = []
        Industry = []
        Position = []
        Company = []
        Requirements = []
        Phonenumber = []
        count=1
        elements_for_displaying_categories=driver.find_elements(By.CSS_SELECTOR,"div[class=\'VVOccHMC_occItem__3iY8y\']")
        index_for_categories=1
        for category in categories:
            industry_element=category.find_element(By.CSS_SELECTOR,"div[class=\'VVOccHMC_occTitle__FQnH1\']")
            industry_text=industry_element.get_attribute("outerHTML")
            industry_chinese_text = re.search(r'[\u4e00-\u9fff]+', industry_text).group()
            print("------------->Industry text\n", industry_chinese_text)
            position_wrapper_elements=category.find_elements(By.CSS_SELECTOR,"div[class=\'VVOccHMC_occHMCMenuItem__MnC_t\']")
            print("------------->The count of positions\n", len(position_wrapper_elements))
            if index_for_categories % 9==0:
                driver.find_element(By.CSS_SELECTOR,"span[class=\'VVOccHMC_arrowBox__nLk2q\']").click()
            
            front_page=driver.current_window_handle

            for position_wrapper_element in position_wrapper_elements:
                position_element=position_wrapper_element.find_element(By.CSS_SELECTOR,"a[class=\'VVOccHMC_oneOccName__0AH0c\']")
                position_text=position_element.get_attribute("outerHTML")
                position_chinese_text = re.search(r'[\u4e00-\u9fff]+', position_text).group()
                print("------------->Position text\n", position_chinese_text)
                actions.move_to_element(elements_for_displaying_categories[index_for_categories]).perform()
                actions.move_to_element(position_wrapper_elements[0]).perform()
                #driver.execute_script("arguments[0].scrollIntoView();", position_element)
                actions.move_to_element(position_element).click().perform()
                #sleep(5)
                job_lists_page=driver.window_handles[-1]
                driver.switch_to.window(job_lists_page)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[class=\'Footer_yp-footer-content__oId8P\']")))
                sleep(5)
                page_count_text=driver.find_element(By.CSS_SELECTOR,"li[title=\'250\']>a>span").text
                page_count_number=int(page_count_text)
                print("-------------->The count of pages\n", page_count_number)
                
                for _ in range(page_count_number-1):
                    job_cards=driver.find_elements(By.CSS_SELECTOR,"div[class=\'RecruitCard_recruit-card-wrap__B2qK1\']")
                    print("--------------------Getting job cards of each pages-----------------------")
                    print("--------------->The count of cards in one page\n", len(job_cards))
                    for job_card in job_cards:
                        job_card.click()
                        job_page=driver.window_handles[-1]
                        driver.switch_to.window(job_page)
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[class=\'Footer_yp-footer-content__oId8P\']")))
                        position_and_city_element=driver.find_element(By.CSS_SELECTOR,"h1[class=\'RecruitInfo_recruitTitle__nQr3_\']")
                        print("--------------->position and city text\n",position_and_city_element.text)
                        position_and_city_text=position_and_city_element.text
                        city_chinese_text=position_and_city_text.split('|')[1].strip()
                        print("--------------->getting city name\n",city_chinese_text)
                        requirement_elements=driver.find_elements(By.CSS_SELECTOR,"div[class=\'RecruitInfo_detailDesc__WwrJb\']>p")
                        requirement_chinese_text=""
                        company_chinese_text=""
                        for requirement_element in requirement_elements:
                            text=requirement_element.get_attribute("outerHTML")
                            chinese_text=re.search(r'[\u4e00-\u9fff]+', text).group()
                            requirement_chinese_text+=chinese_text.strip()
                        print("--------------->getting requirements\n",requirement_chinese_text)
                        try:
                            company_element=driver.find_element(By.CSS_SELECTOR,"h3[class=\'RecruitCompany_companyName__D59LN\']")
                            company_text=company_element.get_attribute("outerHTML")
                            company_chinese_text=re.search(r'[\u4e00-\u9fff]+', company_text).group()
                        except Exception as e:
                            company_element=driver.find_element(By.CSS_SELECTOR,"span[class=\'RecruitInfo_userName__Xu3Cx\']")
                            company_text=company_element.get_attribute("outerHTML")
                            company_chinese_text=re.search(r'[\u4e00-\u9fff]+', company_text).group()
                        print("---------------Company name\n", company_chinese_text)
                        No.append(count)
                        City.append(city_chinese_text)
                        Industry.append(industry_chinese_text)
                        Position.append(position_chinese_text)
                        Company.append(company_chinese_text)
                        Requirements.append(requirement_chinese_text)
                        Phonenumber.append("14582283238")
                        print("------------------------------->Completed dataset", count, "<---------------------------------")
                        count+=1
                        #Saving the datas into excel file
                        if count % 10 == 0:
                            existing_data = pd.read_excel('data.xlsx')
                            new_data = pd.DataFrame({'No':No,'City':City,'Industry':Industry,'Position':Position,'Company':Company,'Requirements':Requirements,'Phonenumber':Phonenumber})
                            updated_data = pd.concat([existing_data, new_data])
                            updated_data.to_excel('data.xlsx',index=False)
                            No.clear()
                            City.clear()
                            Industry.clear()
                            Position.clear()
                            Company.clear()
                            Requirements.clear()
                            Phonenumber.clear()
                        driver.close()
                        driver.switch_to.window(job_lists_page)
                        sleep(2)
                    next_element=driver.findnext_element(By.CSS_SELECTOR,"li[class=\'anti-pagination-next\']")
                    driver.execute_script("arguments[0].scrollIntoView();", next_element)
                    actions.move_to_element(next_element)
                    actions.click().perform()           
                driver.close()
                driver.switch_to.window(front_page)
            index_for_categories +=1         
    except Exception as e:
        print(e)
#Configure the driver options
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
