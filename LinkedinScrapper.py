from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import re
import pandas as pd
import numpy as np


from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)

username = "soclose.crm@gmail.com"
password = "soclose@123"


search_query = "director in energy"
search_query = search_query.replace(" ", "%20")

place_name = "Paris, Île-de-France, France"


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)  # version_main allows to specify your chrome version instead of following chrome global version
driver.maximize_window()



def loging():
    driver.get('https://www.linkedin.com')  
    WebDriverWait(driver, 10).until(expect.visibility_of_element_located((By.XPATH, '//input[@id="session_key"]')))
    driver.find_element(By.XPATH, '//input[@id="session_key"]').send_keys(username)
    driver.find_element(By.XPATH,"//input[@id='session_password']").send_keys(password)
    driver.find_element(By.XPATH,"//button[contains(text(),'Sign in')]").click()
    


def scrap_available_profie():
    Linkedin_link = [] 
    Linked_in_designation = []

    total_pages = []
    count = 0

    driver.get('https://www.linkedin.com/search/results/PEOPLE/?keywords='+search_query)
    WebDriverWait(driver, 10).until(expect.visibility_of_element_located((By.XPATH, '//button[text()="Locations"]')))

    driver.find_element(By.XPATH, '//button[text()="Locations"]').click()

    WebDriverWait(driver, 10).until(expect.visibility_of_element_located((By.XPATH, "//input[@placeholder='Add a location']")))
    driver.find_element(By.XPATH, "//input[@placeholder='Add a location']").send_keys(place_name)
    time.sleep(2)
    driver.find_element(By.XPATH, "//*[contains(@id, 'basic-result-')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[text()="Locations"]').click()

    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    # html = driver.page_source
    # soup = BeautifulSoup(html)
    # with open("output4.html", "w", encoding = 'utf-8') as file:    
    #     file.write(str(soup.prettify()))
    # pegination = driver.find_element(By.CSS_SELECTOR, '.artdeco-pagination.artdeco-pagination--has-controls.ember-view.pv5.ph2')
    # list = driver.find_element(By.CLASS_NAME, 'artdeco-pagination__indicator')

    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")

    for ultag in soup.find_all('ul'):
        for litag in ultag.find_all('li'):
            #print(litag.text)
            li_text = litag.text
            li_text = li_text.strip()
            if(li_text.isnumeric()):
                total_pages.append(litag.text)

    for search_rslt_tag in soup.find_all("div", {"class": "ph0 pv2 artdeco-card mb2"}):
        for a in search_rslt_tag.find_all('a', href=True):
            #print ("Found the URL:", a['href'])
            if (count % 2) == 0:
                Linkedin_link.append(a['href'])

            count = count + 1
            
        for designation in search_rslt_tag.find_all('div', {"class":"entity-result__primary-subtitle t-14 t-black t-normal"}):
            #print (designation.text)  
            Linked_in_designation.append(designation.text)


    last_page = int(re.search(r'\d+', total_pages[len(total_pages)-1]).group())
    # last_page = 2

    print(driver.current_url)

    for x in range(2, last_page+1):
        time.sleep(10)
        count = 0
        driver.get(driver.current_url+'&page='+str(x))

        time.sleep(4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # html = driver.page_source
        # soup = BeautifulSoup(html)
        # with open("output4.html", "w", encoding = 'utf-8') as file:    
        #     file.write(str(soup.prettify()))
        # pegination = driver.find_element(By.CSS_SELECTOR, '.artdeco-pagination.artdeco-pagination--has-controls.ember-view.pv5.ph2')
        # list = driver.find_element(By.CLASS_NAME, 'artdeco-pagination__indicator')

        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")

        for ultag in soup.find_all('ul'):
            for litag in ultag.find_all('li'):
                #print(litag.text)
                li_text = litag.text
                li_text = li_text.strip()
                if(li_text.isnumeric()):
                    total_pages.append(litag.text)

        for search_rslt_tag in soup.find_all("div", {"class": "ph0 pv2 artdeco-card mb2"}):
            for a in search_rslt_tag.find_all('a', href=True):
                #print ("Found the URL:", a['href'])
                if (count % 2) == 0:
                    Linkedin_link.append(a['href'])

                count = count + 1
                
            for designation in search_rslt_tag.find_all('div', {"class":"entity-result__primary-subtitle t-14 t-black t-normal"}):
                #print (designation.text)  
                Linked_in_designation.append(designation.text)


    #Linkedin_link = list(dict.fromkeys(Linkedin_link))
    Linked_in_designation = list(dict.fromkeys(Linked_in_designation))

    print(len(Linkedin_link))
    print(len(Linked_in_designation))

    a = np.array(Linkedin_link)
    b = np.array(Linked_in_designation)



    df = pd.DataFrame({"name1" : a, "name2" : b})
    df.to_csv("test1.csv", index=False)
    # items = list.find_element(By.TAG_NAME,"li")
    # for item in items:
    #     text = item.text
    #     print(text)





    




 

loging()
time.sleep(15)
scrap_available_profie()
# print("Put any of  one choice:\n[1] For massage with connects\n[2] For massage to people of  selected profiles (This feature is avalable  only for Premium)")
# choice = int(input("Enter choice:"))
# if choice==1:
#     loging()
#     messaging_to_connects()
#     #print("Normal")
# elif choice==2:
#     loging()
#     messaging_to_anyone_for_permium()
#     #print("Premium")
# else:
#     print("Exit")
