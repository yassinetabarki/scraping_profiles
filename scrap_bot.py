from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import logging
import os
# import wget
import time
import json
import pandas as pd

class bot:
    def login(user_name,password):    
        # driver=open_browser()
        #target username
        username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='session_key']")))
        pas = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='session_password']")))

        #enter username and password
        username.clear()
        username.send_keys(user_name)
        pas.clear()
        pas.send_keys(password)

        #target the login button and click it
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    def search(search_text):  
            # searchbox.clear()
            logging.info("Searching jobs page")
            time.sleep(5)
            driver.maximize_window()
            # searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
            searchbox = driver.find_element_by_class_name("search-global-typeahead__input")

            searchbox.clear()
            searchbox.send_keys(search_text)
            searchbox.send_keys(Keys.ENTER)
            logging.info("Keyword search successful")
        # main_url=driver.current_url


    def collect_page(pages):    
        links=[]
        names=[]
        time.sleep(3)
        try:
            for n in range(1,pages+1):
                profils = driver.find_elements(By.CLASS_NAME,'entity-result__content')
                time.sleep(1)
                name = driver.find_elements(By.XPATH,'//span[@dir="ltr"]')
                time.sleep(1)
                for x in name:
                    names.append(x.text)
                time.sleep(1)
                for i in profils:
                    links.append(i.find_element(By.TAG_NAME,'a').get_attribute('href'))
                time.sleep(5)
                main_url=driver.current_url
                ur=[i[::-1] for i in main_url[::-1].split('&', 2)][::-1]
                url=ur[0]+"&page="+str(n+1)
                driver.get(url)

        except Exception as e:
            print(logging.error(str(e)))
        return names,links

    def listing(i,v,n):
            profils_disc={}
            profils_disc["profile_id"] = n
            profils_disc["name"] = i
            profils_disc['url_link']=v
            return profils_disc
    def get_dict_profil(url,names):
        profils_list=[]
        names_d=[i.split('\n') for i in names]
        names_f=[n[0] for n in names_d]

        zobject = zip(names_f, url)
        n=1
        for e1,e2 in zobject:
            profils_list.append(bot.listing(e1,e2,n))
            n+=1
        return profils_list
    
# if __name__ == "__main__":
    def start(email,password,search,pages):
        # email="***********"
        # password="***********"
        # search="outsourcing"
        # pages=1
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)
        global driver
        driver = webdriver.Chrome('./webdriver/chromedriver.exe', chrome_options=chrome_options)
        #open the webpage
        driver.get("https://www.site.com/login")
        bot.login(email,password)
        bot.search(search)
        time.sleep(3)
        found= False
        try:
            searchbox = driver.find_element_by_xpath("//button[@aria-label='People']")
            searchbox.send_keys(Keys.ENTER)
        except :
            found = True
        if found:
            searchbox = driver.find_element_by_xpath("//button[@aria-label='Personnes']")
            searchbox.send_keys(Keys.ENTER)
            
        names,url=bot.collect_page(pages)
        profiles=bot.get_dict_profil(url,names)
        with open("profiles_dataset.json","w", encoding='utf-8') as fout:
            json.dump(profiles,fout,ensure_ascii=False,indent=2)

        df = pd.DataFrame.from_dict(profiles)

        df.to_excel('profiles.xlsx')
