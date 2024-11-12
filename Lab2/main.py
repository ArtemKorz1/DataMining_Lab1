from lxml import html
import requests
import os.path
import bs4

from Lab1.main import JsonWork
from Lab3.main import MongoWork, coll_name_default, lab3_suffix

lab2_suffix = 'Lab2\\'


class TextFileWork:
    @staticmethod
    def save(filename, text, encoding):
        file = open(filename, 'w', encoding=encoding)
        file.write(text)

    @staticmethod
    def read(filename, encoding):
        file = open(filename, 'r', encoding=encoding)
        return file.read()


class ParserTlPerm:
    site_name = lab2_suffix + 'светофор'
    method_xpath = 'xpath'
    method_bs = 'bs'

    site_filename_temp = site_name + '_temp.html'
    site_filename_xpath = site_name + '_xpath' + '.json'
    site_filename_bs = site_name + '_bs' + '.json'
    site = 'https://пермь.светофор-магазин.рф/catalog/'

    mongo_items_with_cost_filename = lab3_suffix + 'items_from_mongoDB.json'
    mongo = MongoWork()

    @staticmethod
    def html_get(request, filename, encoding, for_method):
        resp = requests.get(request)
        # content = resp.content.decode(encoding)
        content = resp.text

        if for_method == ParserTlPerm.method_xpath:
            res = html.fromstring(content)
        elif for_method == ParserTlPerm.method_bs:
            res = content
        else:
            res = {}

        TextFileWork.save(filename, content, encoding)
        print("Request sent: {}, status: {}, reason: {}".format(request, resp.status_code, resp.reason))
        return res

    @staticmethod
    def html_get_from_website(website_url, website_filename_temp, encoding, for_method):
        # Выполнение запроса и сохранение ответа в файл, чтобы не повторять запрос
        if not os.path.exists(website_filename_temp):
            req_body = website_url
            res = ParserTlPerm.html_get(req_body, website_filename_temp, encoding, for_method)
        else:
            file = open('{}\\{}'.format(os.getcwd(), website_filename_temp), 'r', encoding=encoding)
            if for_method == ParserTlPerm.method_xpath:
                res = html.fromstring(file.read())
            else:
                res = file.read()

        return res

    @staticmethod
    def clean(item):
        return item.strip().replace('&quot', '\"').replace(' ,', ',')

    @staticmethod
    def get_stuff_by_xpath(use_db=False):
        root = ParserTlPerm.html_get_from_website(ParserTlPerm.site,
                                                  ParserTlPerm.site_filename_temp,
                                                  'cp1251',
                                                  ParserTlPerm.method_xpath)
        parsed_items = []

        catalog = root.xpath("//div[@id='catalog']/div/div")
        for div in catalog:
            item = div.xpath(".//div[@class='item-all-title']")

            item_name = div.xpath(".//a/text()")
            if item_name:
                name = ParserTlPerm.clean(item_name[0])

                item_price = div.xpath(".//div[@class='item-price']")
                price = div.xpath(".//b/text()")[0] + div.xpath(".//b/span/text()")[0]

                img = "https:" + div.xpath(".//img/@src")[0]

                item_info = div.xpath(".//div[@class='article']")
                info = {}
                for article in item_info:
                    split = article.xpath(".//text()")[0].split(': ')
                    if split[1] != '0 гр/ед':
                        info.update({split[0]: split[1]})

                elem = {'name': name,
                        'price': price,
                        'cost': float(price.split(' ')[0]),
                        'info': info,
                        'image': img}
                # print(elem)
                parsed_items += [elem]
            # else: # Элемент отсутствует на сайте

        if use_db:
            #ParserTlPerm.mongo.resave(parsed_items)
            ParserTlPerm.mongo.add(parsed_items, 'name')
        else:
            JsonWork.save(ParserTlPerm.site_filename_xpath, parsed_items)

    @staticmethod
    def get_stuff_by_bsoup(use_db=False):
        text = ParserTlPerm.html_get_from_website(ParserTlPerm.site,
                                                  ParserTlPerm.site_filename_temp,
                                                  'cp1251',
                                                  ParserTlPerm.method_bs)
        parsed_items = []
        soup = bs4.BeautifulSoup(text, "lxml")

        catalog = soup.findAll("div", class_='catalog-item-card item-tb')

        for div in catalog:
            item_name = div.find("a", class_='item-title')

            if item_name:
                name = ParserTlPerm.clean(item_name.text)

                item_price = div.find("span", class_='catalog-item-price')
                price = div.find("b").text

                img = "https:" + div.find("img")['src']

                item_info = div.findAll("div", class_='article')
                info = {}
                for article in item_info:
                    split = article.text.split(': ')
                    if split[1] != '0 гр/ед':
                        info.update({split[0]: split[1]})

                elem = {'name': name,
                        'price': price,
                        'cost': float(price.split(' ')[0]),
                        'info': info,
                        'image': img}
                # print(elem)
                parsed_items += [elem]
            # else: #Элемент отсутствует на сайте

        if use_db:
            #ParserTlPerm.mongo.resave(parsed_items, coll_name=coll_name_default + '_bs')
            ParserTlPerm.mongo.add(parsed_items, 'name', coll_name=coll_name_default + '_bs')
        else:
            JsonWork.save(ParserTlPerm.site_filename_bs, parsed_items)

    #Lab3: mongoDB
    @staticmethod
    def choose_products_by_cost(threshold):
        collection = ParserTlPerm.mongo.collection_by_name()
        cost = float(threshold)

        found = collection.find({'cost': {'$gte': 100.0}}).to_list()
        restricted = ["_id"]
        items = JsonWork.choose_not(found, restricted)

        JsonWork.save(ParserTlPerm.mongo_items_with_cost_filename, items)
        return items
