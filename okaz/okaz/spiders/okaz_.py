import scrapy
import pandas as pd
class OkazSpider(scrapy.Spider):
    name = 'okaz_'
    allowed_domains = ['okaz.com.sa']
    start_urls = ['https://www.okaz.com.sa/news/local/2150775']

    def start_requests(self):
        df=pd.read_csv(f'links.csv')
        # there are two columns: Category, Link
        for index, row in df.iterrows():
            category = row['Category']
            yield scrapy.Request(url=row['Link'], callback=self.parse, meta={'category': category})


    def parse(self, response):
        # Extract the text from the response
        subtitle1=response.xpath('//h3[@class="article-subtitle"]/text()').get()
        subtitle2=response.xpath('//h1[@class="autoHeight"]/text()').get()
        if subtitle1 is None:
            subtitle1 = ""
        if subtitle2 is None:
            subtitle2 = ""
        title = subtitle1 + " "+subtitle2
        article_meta_text = response.xpath('//li[@class="media_article_publish_time"]/p/text()').getall()
        article_meta_text = " ".join(article_meta_text)
        body_text = response.xpath('//div[@class="bodyText"]/text()').getall()
        body_text = " ".join(body_text)
        yield {
            'Category': response.meta['category'],
            'Page_link': response.url,
            'title': title,
            'article_meta_text': article_meta_text,
            'body_text': body_text
        }

