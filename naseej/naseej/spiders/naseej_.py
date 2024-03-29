import scrapy
from pathlib import Path
import json


class NaseejSpider(scrapy.Spider):

    name = 'naseej_'
    allowed_domains = ['naseej.com']
    start_urls = ['https://www.naseej.com/ar/news/page/1']

    # check the number of pages from the website
    number_of_pages = 1000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

    def start_requests(self):
        for i in range(1, self.number_of_pages + 1):
            yield scrapy.Request(
                url=f'https://www.naseej.com/ar/news/page/{i}',
                callback=self.parse
            )
    def parse(self, response):
        page_links = response.xpath('//h2[@itemprop="headline"]/a/@href').getall()
        for link in page_links:
            yield scrapy.Request(
                url=link,
                callback=self.parse_article
            )

    def parse_article(self, response):
        title = response.xpath('//h1[@class="title"]/text()').get()
        if title is None:
            title= response.xpath('//p[@style="text-align: center;"]/span/strong/text()').get()
        body = response.xpath('//div[@class="the_content_wrapper"]//text()').getall()
        if body is None or len(body) == 0:
            body = response.xpath('//p[@style="text-align: justify;"]/span/text()').getall()
        body=''.join(body)
        self.items.append(
        {
            'url': response.url,
            'title': title,
            'date': response.xpath('//time[@itemprop="datePublished"]/text()').get(),
            'body': body
        }
        )

    def closed(self, reason):
        # Save the chapters as a JSON file
        json_path = 'naseej.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)
