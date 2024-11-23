import scrapy

from Lab3.main import MongoWork

mongo = MongoWork()
coll_name = 'regard_with_spider'


class ExperimentalSpider(scrapy.Spider):
    name = "Experimental"
    allowed_domains = ["www.regard.ru"]
    start_urls = ["https://www.regard.ru/catalog/1018/vneshnie-zhestkie-diski-i-ssd"]

    def parse(self, response):
        catalog = response.xpath("//div[@class='rendererWrapper']/div/div/div")

        for div in catalog:
            elem = {
                'id': int(div.xpath(".//p[@class='CardId_id__mCbo0 swiper-no-swiping Card_cardId__mhbeZ CardId_listing__HxeVI']/text()").get().split(' ')[1]),
                'name': div.xpath(".//a[@class='CardText_link__C_fPZ link_black']/div/text()").get(),
                'info': div.xpath(".//p[@class='CardText_text__fZPl_ CardText_withMods__0O7T4 CardText_listing__6mqXC Card_cardText__j_k2t']/text()").get(),
                'cost': int(div.xpath(".//span[@class='Price_price__m2aSe notranslate']/text()").get() +
                            div.xpath(".//span[@class='Price_price__m2aSe notranslate']/text()")[2].get()),
                'status': div.xpath(".//p[@class='Card_inStockText__ciAyD']/text()").get()
            }
            mongo.add(elem, 'id', coll_name)
            yield elem
