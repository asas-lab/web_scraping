from pathlib import Path
import re
import scrapy
import json
import time

class Alriyadh(scrapy.Spider):
    name = "alriyadh"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.first_page = 897201
        self.latest_page = 2045191
    def start_requests(self):
        for i in range(self.first_page,self.latest_page+1):  # Change to this after first page 897201 last page 1559429, before 2045191
            url = f'https://www.alriyadh.com/{i}'
            yield scrapy.Request(url=url, callback=self.parse)
            #time.sleep(5)  # Add a delay of 5 seconds between requests

    def parse(self, response):
        item = {}

        # Extract the title
        item['title'] = response.css('.article-title h2::text').get()

        # Extract the date
        item['date'] = response.css('.article-time time::text').get().strip()

        # Extract the content
        paragraphs = response.css('.col-md-12.article-text p::text').getall()
        item['content'] = ' '.join([p.strip() for p in paragraphs if p.strip()])

        # Add the URL of the page
        item['url'] = response.url

        # Check for specific keywords in the content (if needed)
        self.items.append(item)


    def closed(self, reason):
        # Save the chapters as a JSON file
        json_path = 'alriyadh.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)
