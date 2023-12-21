import requests
import json
import re
import pandas as pd
import os
from time import sleep


file_path = f'{os.getcwd()}\links.csv'

# Check if the CSV file exists
if os.path.exists(file_path):
    # Read the existing CSV file
    df = pd.read_csv(file_path, encoding='utf-8')
else:
    # Create a new DataFrame
    df = pd.DataFrame(columns=['Category', 'Link','Page_number'])

def get_links(df, category_name, category_page_url, page_number_limit, section, sub_section):
    """
    Collects links from a specified category page on okaz.com.sa and saves them to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to store the collected links.
        category_name (str): The name of the category.
        category_page_url (str): The URL of the category page.
        page_number_limit (int): The maximum number of pages to scrape.
        section (int): The section ID.
        sub_section (int): The sub-section ID.
    """
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en,en-US;q=0.9,en-GB;q=0.8,ar;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.okaz.com.sa",
        "Referer": category_page_url,
        "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = "https://www.okaz.com.sa/ajax-more-articles"
    
    for page_number in range(1, page_number_limit):
        links = []
        data = {
            "page": str(page_number),
            "section": section,
            "sub_section": sub_section
        }
        response = requests.post(url, headers=headers, data=data)
        text = response.json()['html']
        links = re.findall(r'href=\"(.*?)\"', text)
        new_data = pd.DataFrame({'Category': category_name, 'Link': links, 'Page_number': page_number})
        df = pd.concat([df, new_data])  
        df.to_csv(file_path, index=False, encoding='utf-8')
        print('collected and saved ' + str(len(links)) + ' links from page ' + str(page_number))
        sleep(3)
        
get_links(df, 'articles_authors', 'https://www.okaz.com.sa/morearticles/articles/authors', 10, 57, 247)

# links_category = {
#     'https://www.okaz.com.sa/morearticles/articles/authors': 'articles_authors',
#     'https://www.okaz.com.sa/morearticles/articles/people-voice': 'articles_people-voice',
#     'https://www.okaz.com.sa/morearticles/variety': 'variety',
#     'https://www.okaz.com.sa/morearticles/culture/other': 'culture_other',
#     'https://www.okaz.com.sa/morearticles/culture/culture': 'culture_culture',
#     'https://www.okaz.com.sa/morearticles/culture/art': 'culture_art',
#     'https://www.okaz.com.sa/morearticles/economy/international': 'economy_international',
#     'https://www.okaz.com.sa/morearticles/economy/arabian': 'economy_arabian',
#     'https://www.okaz.com.sa/morearticles/economy/saudi': 'economy_saudi',
#     'https://www.okaz.com.sa/morearticles/sport/special-interviews': 'sport_special-interviews',
#     'https://www.okaz.com.sa/morearticles/sport/miscellaneous-games': 'sport_miscellaneous-games',
#     'https://www.okaz.com.sa/morearticles/sport/international': 'sport_international',
#     'https://www.okaz.com.sa/morearticles/sport/arabian': 'sport_arabian',
#     'https://www.okaz.com.sa/morearticles/sport/saudi': 'sport_saudi',
#     'https://www.okaz.com.sa/morearticles/news/politics': 'news_politics',
#     'https://www.okaz.com.sa/morearticles/news/local': 'news_local'
# }
