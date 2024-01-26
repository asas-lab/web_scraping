from pathlib import Path
import re
import scrapy
import json
import time

class Almadina (scrapy.Spider):
    name = "almadina"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.first_page = 500083
        self.last_page = 500083 + 1
    def start_requests(self):
        for i in range(self.first_page,self.last_page):  # Change to this after first page 897201 last page 1559429, before 2045191
            url = f'https://www.al-madina.com/article/{i}'
            yield scrapy.Request(url=url, callback=self.parse)
            time.sleep(5)  # without a delay it shows 503 error. 

    def parse(self, response):
        item = {}

        # Extract the title
        item['title'] = response.css('h1.article-title::text').get()

        # Extract the date
        date_text = response.css('.article-date::text').get()
        if date_text:
            date_text = date_text.replace('تاريخ النشر:', '').strip()
        item['date'] = date_text

        # Extract the content
        content_paragraphs = response.css('.article-body *::text').getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        # Add the URL of the page
        item['url'] = response.url

        self.items.append(item)

    def closed(self, reason):
        # Save the chapters as a JSON file
        json_path = 'almadina.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)
