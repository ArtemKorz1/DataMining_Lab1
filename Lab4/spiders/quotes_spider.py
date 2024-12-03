import scrapy
from scrapy_splash import SplashRequest

from Lab3.main import MongoWork

mongo = MongoWork()
coll_name = 'quotes_with_spider'


class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    splashRequestDone = False

    def parse(self, response):
        if not self.splashRequestDone:
            yield SplashRequest(url=self.start_urls[0], callback=self.parse)
            self.splashRequestDone = True

        catalog = response.xpath("//div[@class='col-md-8']/div")

        for div in catalog:
            elem = {
                'text': div.xpath(".//span[@class='text']/text()").get(),
                'author': div.xpath(".//small[@class='author']/text()").get(),
                'tags': div.xpath(".//a[@class='tag']/text()").getall(),
            }
            mongo.add(elem, 'text', coll_name)
            yield elem

