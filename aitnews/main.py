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

# Set the latest page number to scrape
latest_page_number = 535749

# Set the save rate for saving data to CSV file
save_rate = 10

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
    df = pd.DataFrame(columns=['Page_link','Redirected_link', 'Title', 'Page_info', 'Body'])

# Create driver object with undetected_chromedriver
options = uc.ChromeOptions()
# comment the below line if you want to see the browser
options.add_argument("--headless")
options.add_argument("--disable-javascript")
options.add_argument('--blink-settings=imagesEnabled=false')
driver = uc.Chrome(driver_executable_path=webdriver_path, options=options, use_subprocess=True)

# Loop through the range of page numbers
for i in range(1, latest_page_number):
    # Navigate to the page URL
    driver.get(f'https://aitnews.com/?p={i}')
    try:
        print('link:', f'https://aitnews.com/?p={i}')
        
        # Find and print the title of the page
        title = driver.find_element(By.XPATH, '//h1[@class="post-title entry-title"]')
        title = title.text
        # print('title', title)
        
        # Find and print the date of the page
        date = driver.find_elements(By.XPATH, '//div[@class="entry-header"]//div[@class="single-post-meta post-meta clearfix"]/span')
        date = ' '.join([d.text for d in date])
        # print('date', date)
        
        # Find and print the body content of the page
        body = driver.find_elements(By.XPATH, '//div[@class="entry-content entry clearfix"]/p')
        body = ' '.join([d.text for d in body])
        # print('body', body)
        # print('----------------------------------------')
        
        # Create a new DataFrame with scraped data
        new_data = pd.DataFrame({'Page_link': f'https://aitnews.com/?p={i}','Redirected_link':driver.current_url, 'Title': title, 'Page_info': date, 'Body': body}, index=[0])
        
        # Concatenate the new data with the existing DataFrame
        df = pd.concat([df, new_data], ignore_index=True)

        # Save the DataFrame to CSV file at the specified save rate
        if i % save_rate == 0:
            df.to_csv(csv_data_file_path, index=False, encoding='utf-8')

    except Exception as e:
        print("404 Error: Page not found at the URL", f'https://aitnews.com/?p={i}')
