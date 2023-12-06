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
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re

from dotenv import load_dotenv
import os
# from flask_cors import CORS
load_dotenv()
app = Flask(__name__)

#Function for scraping recruiter's data
def _startScraping_recruiters(chrome_options):
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
        sleep(6)


        #login button clicking
        actions=ActionChains(driver)
        actions.move_to_element(login_element)
        actions.click().perform()
        print("--------------Login modal is displayed.Please login manually------------")


        #waiting until getting verification code from client and being invisible the login modal
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR,"div[class=\'LoginPopup_login-model__n45M8\']")))
       
       
        #getting all job categories
        categories=driver.find_elements(By.CSS_SELECTOR,"div[class=\'VVOccHMC_occHMCBox__Zy8oj\']")
        del categories[0]
        print("-------------->The count of categories\n", len(categories))
       
       
        #---------------------------------------------------------Starting Scraping--------------------------------------------------------------------------
        
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
                #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[class=\'Footer_yp-footer-content__oId8P\']")))
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
                        #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[class=\'Footer_yp-footer-content__oId8P\']")))
                        sleep(2)
                        city_chinese_text=""
                        try:
                            position_and_city_element=driver.find_element(By.CSS_SELECTOR,"h1[class=\'RecruitInfo_recruitTitle__nQr3_\']")
                            print("--------------->position and city text\n",position_and_city_element.text)
                            position_and_city_text=position_and_city_element.text
                            city_chinese_text=position_and_city_text.split('|')[1].strip()
                        except Exception as e:
                            print(e)
                        print("--------------->getting city name\n",city_chinese_text)
                        requirement_elements=driver.find_elements(By.CSS_SELECTOR,"div[class=\'RecruitInfo_detailDesc__WwrJb\']>p")
                        requirement_chinese_text=""
                        company_chinese_text=""
                        for requirement_element in requirement_elements:
                            try:
                                text=requirement_element.get_attribute("outerHTML")
                                chinese_text=re.search(r'[\u4e00-\u9fff]+', text).group()
                                requirement_chinese_text+=chinese_text.strip()
                            except Exception as e:
                                print("--------------->Error was occured while getting requirement information\n",e)
                        print("--------------->getting requirements\n",requirement_chinese_text)
                        try:
                            company_element=driver.find_element(By.CSS_SELECTOR,"h3[class=\'RecruitCompany_companyName__D59LN\']")
                            company_text=company_element.get_attribute("outerHTML")
                            company_chinese_text=re.search(r'[\u4e00-\u9fff]+', company_text).group()
                        except Exception as e:
                            company_element=driver.find_element(By.CSS_SELECTOR,"span[class=\'RecruitInfo_userName__Xu3Cx\']")
                            company_text=company_element.get_attribute("outerHTML")
                            company_chinese_text=re.search(r'[\u4e00-\u9fff]+', company_text).group()
                        print("--------------->Company name\n", company_chinese_text)
                        button_element=driver.find_element(By.CSS_SELECTOR, "div[class=\'ViewPhone_view-phone__5n59_\']")
                        actions.move_to_element(button_element).click().perform()
                        sleep(4)
                        phonenumber_text=""
                        try:
                            phonenumber_element=driver.find_element(By.CSS_SELECTOR,"span[class=\'GetPhoneTipsDialog_fictitious-tel__uKPpQ\']")
                            phonenumber_text=phonenumber_element.text
                        except Exception as e:
                            print("There isn't enough points")
                        print("--------------->Phone Number\n", phonenumber_text)
                        City.append(city_chinese_text)
                        Industry.append(industry_chinese_text)
                        Position.append(position_chinese_text)
                        Company.append(company_chinese_text)
                        Requirements.append(requirement_chinese_text)
                        Phonenumber.append(phonenumber_text)
                        print("------------------------------->Completed dataset", count, "<---------------------------------")
                        count+=1
                        #Saving the datas into excel file
                        if count % 10 == 0:
                            existing_data = pd.read_excel('recruiters.xlsx')
                            new_data = pd.DataFrame({'City':City,'Industry':Industry,'Position':Position,'Company':Company,'Requirements':Requirements,'Phonenumber':Phonenumber})
                            updated_data = pd.concat([existing_data, new_data])
                            updated_data.to_excel('recruiters.xlsx',index=False)
                            sleep(2)
                            print("-------------------------------10 datasets are stored to excel file-------------------------------")
                            City.clear()
                            Industry.clear()
                            Position.clear()
                            Company.clear()
                            Requirements.clear()
                            Phonenumber.clear()
                        driver.close()
                        driver.switch_to.window(job_lists_page)
                    sleep(2)
                    next_element=driver.find_element(By.CSS_SELECTOR,"li[class=\'ant-pagination-next\']")
                    next_element.click()
                    sleep(2)         
                driver.close()
                driver.switch_to.window(front_page)
            index_for_categories +=1         
    except Exception as e:
        print(e)
#Function for scraping worker's data
def _startScraping_workers(chrome_options):
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options,
    )
    try:
        driver.get("https://www.yupao.com/")
        driver.execute_script("document.charset='UTF-8';")

        #waiting until login button is prepared for clicking
        wait = WebDriverWait(driver, 500)
        login_element=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\'Header_header-topbar-content-right__Etq2J\']")))
        print("***************Ready for clicking***************")
        sleep(6)


        #login button clicking
        actions=ActionChains(driver)
        actions.move_to_element(login_element)
        actions.click().perform()
        print("***************Login modal is displayed.Please login manually***************")


        #waiting until getting verification code from client and being invisible the login modal
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR,"div[class=\'LoginPopup_login-model__n45M8\']")))
        workers_element=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div/div/div[1]/div/div/div[3]")
        actions.move_to_element(workers_element).click().perform()
        industry_page=driver.window_handles[-1]
        driver.switch_to.window(industry_page)
        #getting all job categories
        categories=driver.find_elements(By.CSS_SELECTOR,"span[class=\'FilterComponent_yp-filter-worktype-item__zNeYK\']")
        del categories[0]
        print("***************>The count of categories\n", len(categories))
       
       
        #---------------------------------------------------------Starting Scraping--------------------------------------------------------------------------
        
        City = []
        Industry = []
        Position = []
        Name = []
        Introduction = []
        Phonenumber = []
        count=1
        index_for_categories=0
        for category in categories:
            industry_element=category.find_element(By.TAG_NAME,"a")
            industry_text=industry_element.get_attribute("outerHTML")
            industry_chinese_text = re.search(r'[\u4e00-\u9fff]+', industry_text).group()
            print("***************>Industry text\n", industry_chinese_text)
            position_wrapper_elements=[]
            try:
                if index_for_categories==0 or index_for_categories==1:
                    actions.move_to_element(category).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
                    position_page=driver.window_handles[-1]
                    driver.switch_to.window(position_page)
                    sleep(2)
                    position_wrapper_elements=driver.find_elements(By.CSS_SELECTOR,"span[class=\'FilterComponent_yp-filter-worktype-item__zNeYK\']")
                    
                else:
                    actions.move_to_element(category).click().perform()
                    sleep(2)
                    elements_for_position=driver.find_elements(By.CSS_SELECTOR,"div[class=\'FilterComponent_type-item-box__c_T79\']")
                    element_for_position=elements_for_position[1]
                    position_wrapper_elements=element_for_position.find_elements(By.CSS_SELECTOR,"span[class=\'FilterComponent_yp-filter-worktype-item__zNeYK\']")
            except Exception as e:
                print(e)
            print("***************>The count of positions\n", len(position_wrapper_elements))

            for position_wrapper_element in position_wrapper_elements:
                position_element=position_wrapper_element.find_element(By.TAG_NAME,"a")
                position_text=position_element.get_attribute("outerHTML")
                position_chinese_text = re.search(r'[\u4e00-\u9fff]+', position_text).group()
                print("***************>Position text\n", position_chinese_text)
                actions.move_to_element(position_wrapper_element).click().perform()
                detailed_position_elements=driver.find_elements(By.CSS_SELECTOR,"span[class=\'WorkTypeBox_worktype-item__3_Buo\']")
                print("***************>Counts of subposition\n", len(detailed_position_elements))
                for detailed_position_element in detailed_position_elements:
                    print("***************>Subposition text\n", detailed_position_element.text)
                    actions.move_to_element(detailed_position_element).click().perform()
                    sleep(2)
                    page_count_number=0
                    try:
                        page_count_wrapper_element=driver.find_element(By.CSS_SELECTOR,"ul[class=\'ant-pagination\']")
                        page_count_elements=page_count_wrapper_element.find_elements(By.TAG_NAME,"li")
                        page_count_element=page_count_elements[-2]
                        page_count_text=page_count_element.text
                        page_count_number=int(page_count_text)
                        print("***************>The count of pages\n", page_count_number)
                    except Exception as e:
                        print("There isn't any results.")
                    for _ in range(page_count_number):
                        job_cards=driver.find_elements(By.CSS_SELECTOR,"div[class=\'ResumeCard_resume-card__nQknm\']")
                        print("***************Getting job cards of each pages***************")
                        print("***************>The count of cards in one page\n", len(job_cards))
                        job_lists_page=driver.current_window_handle
                        for job_card in job_cards:
                            city_chinese_text=""
                            try:
                                city_wrapper_element=job_card.find_element(By.CSS_SELECTOR,"p[class=\'ResumeCard_resume-address__judlQ\']")
                                city_element=city_wrapper_element.find_elements(By.TAG_NAME,"span")[1]
                                city_chinese_text=city_element.text
                                print("***************>getting city name\n",city_chinese_text)
                            except Exception as e:
                                print("There isn't city text")
                            job_card.click()
                            job_page=driver.window_handles[-1]
                            driver.switch_to.window(job_page)
                            #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[class=\'Footer_yp-footer-content__oId8P\']")))

                            
                            self_introduction_chinese_text=""
                            name_chinese_text=""
                            try:
                                self_introduction_element=driver.find_element(By.CSS_SELECTOR,"div[class=\'ResumeInfo_resume-other-content__tBafj\']")
                                text=self_introduction_element.get_attribute("outerHTML")
                                chinese_text=re.search(r'[\u4e00-\u9fff]+', text).group()
                                self_introduction_chinese_text+=chinese_text.strip()
                            except Exception as e:
                                print("***************>Error was occured while getting self introduction information\n",e)
                            print("***************>getting self introduction texts\n",self_introduction_chinese_text)
                            name_element=driver.find_element(By.CSS_SELECTOR,"span[class=\'ResumeInfo_infoname__h68AM\']")
                            name_text=name_element.get_attribute("outerHTML")
                            name_chinese_text=re.search(r'[\u4e00-\u9fff]+', name_text).group()
                            print("***************>Name text\n", name_chinese_text)
                            try:
                                button_element=driver.find_element(By.CSS_SELECTOR, "div[class=\'ViewPhone_view-phone-btn__WPuCm\']")
                                actions.move_to_element(button_element).click().perform()
                            except Exception as e:
                                print(e)
                            phonenumber_text="123456789"
                            try:
                                phonenumber_element=driver.find_element(By.CSS_SELECTOR,"span[class=\'GetPhoneTipsDialog_fictitious-tel__uKPpQ\']")
                                phonenumber_text=phonenumber_element.text
                            except Exception as e:
                                print("There isn't enough points")
                            print("***************>Phone Number\n", phonenumber_text)
                            City.append(city_chinese_text)
                            Industry.append(industry_chinese_text)
                            Position.append(position_chinese_text)
                            Name.append(name_chinese_text)
                            Introduction.append(self_introduction_chinese_text)
                            Phonenumber.append(phonenumber_text)
                            print("******************************>Completed dataset", count, "<******************************")
                            count+=1
                            #Saving the datas into excel file
                            if count % 10 == 0:
                                existing_data = pd.read_excel('workers.xlsx')
                                new_data = pd.DataFrame({'City':City,'Industry':Industry,'Position':Position,'Name':Name,'Introduction':Introduction,'Phonenumber':Phonenumber})
                                updated_data = pd.concat([existing_data, new_data])
                                updated_data.to_excel('workers.xlsx',index=False)
                                sleep(2)
                                print("*****************************10 datasets are stored to excel file*****************************")
                                City.clear()
                                Industry.clear()
                                Position.clear()
                                Name.clear()
                                Introduction.clear()
                                Phonenumber.clear()
                            driver.close()
                            driver.switch_to.window(job_lists_page)
                        try:
                            next_element=driver.find_element(By.CSS_SELECTOR,"li[class=\'ant-pagination-next\']")
                            next_element.click()
                            sleep(2)   
                        except Exception as e:
                            print(e)
                    actions.move_to_element(detailed_position_element).click().perform()
            if index_for_categories==0 or index_for_categories==1:
                driver.close()
                driver.switch_to.window(industry_page)
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
if __name__ == "__main__":
    try:
        recruiter_process=Process(target=_startScraping_recruiters, args=(chrome_options,))
        recruiter_process.start()
        worker_process=Process(target=_startScraping_workers,args=(chrome_options,))
        worker_process.start()
        recruiter_process.join()
        worker_process.join()

    except Exception as e:
            print(e)
