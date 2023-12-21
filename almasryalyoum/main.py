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

# Get the current working directory
current_path = os.getcwd()

# Set the path for the Chrome webdriver
webdriver_path = f'{current_path}\chromedriver.exe'

# Set the path for the CSV data file
csv_data_file_path = f'{current_path}\data.csv'

# Set the path for the file to store failed links
failed_links_file = f'{current_path}\failed_links.csv'

# Check if the CSV data file exists
if os.path.exists(csv_data_file_path):
    # Read the existing CSV file
    df = pd.read_csv(csv_data_file_path, encoding='utf-8')
else:
    # Create a new DataFrame
    df = pd.DataFrame(columns=['Page_link', 'Title', 'Page_info', 'Story'])

# Check if the file to store failed links exists
if os.path.exists(failed_links_file):
    df_failed = pd.read_csv(failed_links_file)
else:
    df_failed = pd.DataFrame(columns=['Page_link'])

# Set the start and end page numbers to scrape
start_num_page = 1
end_num_page = 30

# Set the time to wait for a page to load
time_to_load_page = 2

# Set the save rate for the CSV data file
save_rate = 5

# Set the maximum number of attempts to load a page
max_attempts = 7

# Create driver object with undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-javascript")
options.add_argument('--blink-settings=imagesEnabled=false')
driver = uc.Chrome(driver_executable_path=webdriver_path, options=options, use_subprocess=True)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,)

# Loop through the page numbers to scrape
for page_num in range(start_num_page, end_num_page+1):
    try:
        start_time = time.time()
        link = f'https://www.almasryalyoum.com/news/details/{page_num}'
        
        # Set the page load timeout for the driver
        driver.set_page_load_timeout(time_to_load_page)
        
        try:
            # Load the page
            driver.get(link)
        except:
            pass
        
        # Stop the page from loading further
        driver.execute_script("window.stop();")
        
        # Attempt to find the article element on the page
        for attempt in range(max_attempts):
            try:
                element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//div[@class="article"]/h1')))
                break
            except TimeoutException:
                if attempt < max_attempts - 1:
                    # Refresh the page and increase the page load timeout for each attempt
                    print(f'refreshing in {(attempt+2)*time_to_load_page} seconds')
                    driver.set_page_load_timeout((attempt+2)*time_to_load_page)
                    try:
                        driver.get(link)
                    except:
                        continue
                else:
                    print('last attempt')
        
        # Extract the title, page info, and news story from the page
        title = driver.find_element(By.XPATH, '//div[@class="article"]/h1')
        p_info = driver.find_element(By.XPATH, '//div[@class="pinfo"]').text
        news_story = driver.find_element(By.XPATH, '//div[@id="NewsStory"]').text
        
        # Write the data to the CSV file
        new_data = pd.DataFrame({'Page_link': [link], 'Title': [title], 'Page_info': [p_info], 'Story': [news_story]})
        df = pd.concat([df, new_data], ignore_index=True)
        
        # Drop duplicates for the subset 'Page_link'
        df.drop_duplicates(subset=['Page_link'], inplace=True)
        
        # Save the data to the CSV file at the specified save rate
        if page_num % save_rate == 0:
            df.to_csv(csv_data_file_path, index=False, encoding='utf-8')
        
        print(f'Page {page_num} done in {time.time() - start_time} seconds')
    
    except Exception as e:
        # Handle any exceptions that occur during scraping
        print(f'Link {link} failed because of {e}')
        new_data = pd.DataFrame({'Page_link': [link]})
        df_failed = pd.concat([df_failed, new_data], ignore_index=True)
        df_failed.to_csv(failed_links_file, index=False)
        continue

# Quit the driver
driver.quit()