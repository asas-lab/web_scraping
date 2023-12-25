import scrapy


class AlyoumSpider(scrapy.Spider):
    name = 'alyoum_'
    allowed_domains = ['alyaum.com']
    start_urls = ['https://www.alyaum.com/articles/1']

    # latest_page = 6505041
    latest_page = 10
    def start_requests(self):
        for i in range(1, self.latest_page+1):
            yield scrapy.Request(
                url=f'https://www.alyaum.com/articles/{i}',
                callback=self.parse
            )
    def parse(self, response):
        text =response.text
        link=text.split('window.location.href=')[1].split(';')[0].replace("'",'')
        print('link',link)
        yield scrapy.Request(
            url=link,
            callback=self.parse_article
        )
        
    def parse_article(self,response):
        # print('res text', response.text)
        title= response.xpath('//div[@class="aksa-to1-main main-article-title"]/h1/text()').get()
        # print('title: ',title)
        date= response.xpath('//div[contains(@class,"aksa-date")]/text()').get()
        # print('date: ',date)
        body= response.xpath('//div[@class="aksa-articleBody"]/text()').getall()[-1]
        # print('body: ',body)

        yield{
            'url':response.url,
            'title':title,
            'date':date,
            'body':body
        }

