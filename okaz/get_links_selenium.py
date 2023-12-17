# Import necessary libraries
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
import csv
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium_stealth import stealth
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


links_category={'https://www.okaz.com.sa/morearticles/articles/authors':'articles_authors',
           'https://www.okaz.com.sa/morearticles/articles/people-voice':'articles_people-voice',
           'https://www.okaz.com.sa/morearticles/variety':'variety',
           'https://www.okaz.com.sa/morearticles/culture/other':'culture_other',
           'https://www.okaz.com.sa/morearticles/culture/culture':'culture_culture',
           'https://www.okaz.com.sa/morearticles/culture/art':'culture_art',
           'https://www.okaz.com.sa/morearticles/economy/international':'economy_international',
           'https://www.okaz.com.sa/morearticles/economy/arabian':'economy_arabian',
           'https://www.okaz.com.sa/morearticles/economy/saudi':'economy_saudi',
           'https://www.okaz.com.sa/morearticles/sport/special-interviews':'sport_special-interviews',
           'https://www.okaz.com.sa/morearticles/sport/miscellaneous-games':'sport_miscellaneous-games',
           'https://www.okaz.com.sa/morearticles/sport/international':'sport_international',
           'https://www.okaz.com.sa/morearticles/sport/arabian':'sport_arabian',
           'https://www.okaz.com.sa/morearticles/sport/saudi':'sport_saudi',
           'https://www.okaz.com.sa/morearticles/news/politics':'news_politics',
           'https://www.okaz.com.sa/morearticles/news/local':'news_local'}

# links_category={'https://www.okaz.com.sa/morearticles/sport/miscellaneous-games':'sport_miscellaneous-games'}
# Get the current working directory
current_path = os.getcwd()
# Set the path for the Chrome webdriver
webdriver_path = f'{current_path}\chromedriver.exe'
df=pd.read_csv('links.csv')

options = uc.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--disable-javascript")
options.add_argument('--blink-settings=imagesEnabled=false')
driver = uc.Chrome(driver_executable_path=webdriver_path, options=options, use_subprocess=True)
# stealth(driver,
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,)

for link in links_category.keys():
    print('collecting links from '+link+' ...')
    driver.get(link)
    stop_falg=False
    while stop_falg==False:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # body = driver.find_element(By.CSS_SELECTOR, 'body')
        # body.send_keys(Keys.PAGE_DOWN)
        # sleep(0.5)
        try:
            load_more = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="loadMoreArticle"]')))
        except:
            stop_falg = True
            print('stop')
    elements=driver.find_elements(By.XPATH, '//ul[@class="search-results"]/li/div/a')
    links=[]
    for element in elements:
        links.append(element.get_attribute('href'))
    print('collected '+str(len(links))+' links')
    new_data = pd.DataFrame({'Page_link': links, 'Category_name':links_category[link]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.drop_duplicates(subset=['Page_link'], inplace=True)
    df.to_csv('links.csv', index=False)
    print('Saving links from ',links_category[link],' completed successfully ')

driver.quit()