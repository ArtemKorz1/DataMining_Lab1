import scrapy

from Lab3.main import MongoWork, coll_name_default

mongo = MongoWork()
coll_name = coll_name_default + '_with_spider'


class TlSpider(scrapy.Spider):
    name = "tl_spider"
    # Эквивалентно 'пермь.светофор-магазин.рф'
    allowed_domains = ["xn--e1aohf5d.xn----8sbafhjsi5apda0ajr7a.xn--p1ai"]
    # Эквивалентно 'https://пермь.светофор-магазин.рф/catalog/'
    start_urls = ["https://xn--e1aohf5d.xn----8sbafhjsi5apda0ajr7a.xn--p1ai/catalog/"]

    def parse(self, response):
        # Нахождение списка элементов
        catalog = response.xpath("//div[@id='catalog']/div/div")
        for div in catalog:
            # Формирование элемента
            item_name = div.xpath(".//a/text()")
            if item_name:
                price = div.xpath(".//b/text()")[0].get() + div.xpath(".//b/span/text()")[0].get()

                item_info = div.xpath(".//div[@class='article']")
                info = {}
                for article in item_info:
                    split = article.xpath(".//text()")[0].get().split(': ')
                    if split[1] != '0 гр/ед':
                        info.update({split[0]: split[1]})

                elem = {'name': item_name[0].get(),
                        'price': price,
                        'cost': float(price.split(' ')[0]),
                        'info': info,
                        'image': "https:" + div.xpath(".//img/@src")[0].get()
                }

                mongo.add(elem, 'name', coll_name)
                yield elem
            # else: # Элемент отсутствует на сайте

        # Определение ссылки на следующую страницу
        next_page = response.xpath("//div[@class='pagination']/ul/li[@class='last']/a[text()='Вперед']/@href")[0].get()
        if next_page:
            # Переход на следующую страницу
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

