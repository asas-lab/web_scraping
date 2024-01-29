from pathlib import Path
import re
import scrapy
import json
import time

class makkah(scrapy.Spider):
    name = "makkah"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.first_page = 1
        self.latest_page = 500000

    def start_requests(self):
        for i in range(self.first_page,self.latest_page+1):  # Change to this after first page 897201 last page 1559429, before 2045191
            url = f'https://makkahnewspaper.com/{i}'
            yield scrapy.Request(url=url, callback=self.parse)
            #time.sleep(5)  # Add a delay of 5 seconds between requests

    def parse(self, response):
        item = {}

        # # Extract the title
        item['title'] = response.css('.holder-article__title .title-article::text').get()


        # Extract the date
        item['date'] = response.css('.holder-article__cta .subtitle-article::text').get()

        # Extract the content
        elements = response.xpath('/html/body/main/div[4]/div/div[1]/div[2]/div[2]')
        paragraphs = elements.css('p::text').getall()


        # paragraphs = response.css('.article-desc.selectionShareable p::text').getall()



        # Join and store the content
        item['content'] = ' '.join([p.strip() for p in paragraphs if p.strip()])




        # # Add the URL of the page
        item['url'] = response.url

        # Check for specific keywords in the content (if needed)
        self.items.append(item)


    def closed(self, reason):
        # Save the chapters as a JSON file
        json_path = 'makkah.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)
