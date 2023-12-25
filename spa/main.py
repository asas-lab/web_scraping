# Import necessary libraries
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
import csv
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium_stealth import stealth
from selenium.common.exceptions import TimeoutException

# Set the latest page number to scrape
# latest_page_number = 14684
latest_page_number = 4

# Set the save rate (for the main pages) for saving data to CSV file
save_rate = 1

# Get the current working directory
current_path = os.getcwd()

# Set the path for the Chrome webdriver
webdriver_path = f'{current_path}\chromedriver.exe'
csv_data_file_path = f'{current_path}\data.csv'

# Check if the CSV data file exists
if os.path.exists(csv_data_file_path):
    # Read the existing CSV file
    df = pd.read_csv(csv_data_file_path, encoding='utf-8')
else:
    # Create a new DataFrame
    df = pd.DataFrame(columns=['Main page number','url', 'title', 'Page_info', 'Body'])

# Create driver object with undetected_chromedriver
options = uc.ChromeOptions()
# comment the below line if you want to see the browser
# options.add_argument("--headless")
options.add_argument("--disable-javascript")
options.add_argument('--blink-settings=imagesEnabled=false')
driver = uc.Chrome(driver_executable_path=webdriver_path, options=options, use_subprocess=True)

for page_num in range(1,latest_page_number+1):
    driver.get(f'https://www.spa.gov.sa/news/latest-news?page={page_num}')
    page_links=WebDriverWait(driver, 10).until(EC.presence_of_element_located ((By.XPATH, '//div[@class="MuiBox-root muirtl-1lmmdue"]/a')))
    page_links= driver.find_elements(By.XPATH, '//div[@class="MuiBox-root muirtl-1lmmdue"]/a')
    page_links = [link.get_attribute('href') for link in page_links]
    # print('page_links', page_links)
    for link in page_links:
        driver.get(link)
        # Wait until the title element is present
        title_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"MuiTypography-root")]')))
        title = title_element.text
        elements = driver.find_element(By.XPATH, '//div[@class="no-print MuiBox-root muirtl-1q9jtz8"]/div').text
        elements=elements.split('\n')
        page_info=elements[0]
        body=elements[1:-3]
        body=' '.join(body)
        # print('link:', link)
        # print('title', title)
        # print('page_info', page_info)
        # print('body', body)

        new_data = pd.DataFrame({'Main page number': page_num,'url':link, 'title': title, 'Page_info': page_info, 'Body': body}, index=[0])
        # Concatenate the new data with the existing DataFrame
        df = pd.concat([df, new_data], ignore_index=True)
    if page_num % save_rate == 0:
        df.to_csv(csv_data_file_path, index=False, encoding='utf-8')
        print(f'Saved data to CSV file at page {page_num}')