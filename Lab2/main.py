from lxml import html
import requests, os.path, bs4

from Lab1.main import json_save

lab2_suffix = 'Lab2\\'
site_name = lab2_suffix + 'светофор'
method_xpath = 'xpath'
method_bs = 'bs'

site_filename_temp = site_name + '_temp.html'
site_filename_xpath = site_name + '_xpath' + '.json'
site_filename_bs = site_name + '_bs' + '.json'
site = 'https://пермь.светофор-магазин.рф/catalog/'

def html_save(filename, html, encoding):
    file = open(filename, 'w', encoding=encoding)
    file.write(html)

def text_read(filename, encoding):
    file = open(filename, 'r', encoding=encoding)
    return file.read()

def html_get(request, filename, encoding, for_method):
    resp = requests.get(request)
    #content = resp.content.decode(encoding)
    content = resp.text

    if (for_method == method_xpath):
        res = html.fromstring(content)
    elif (for_method == method_bs):
        res = content
    else:
        res = {}

    html_save(filename, content, encoding)
    print("Request sent: {}, status: {}, reason: {}".format(request, resp.status_code, resp.reason))
    return res

def html_get_from_website(website_url, website_filename_temp, encoding, for_method):
    #Выполнение запроса и сохранение ответа в файл, чтобы не повторять запрос
    if (not os.path.exists(website_filename_temp)):
        req_body = website_url
        res = html_get(req_body, website_filename_temp, encoding, for_method)
    else:
        file = open('{}\\{}'.format(os.getcwd(), website_filename_temp), 'r', encoding=encoding)
        if (for_method == method_xpath):
            res = html.fromstring(file.read())
        else:
            res = file.read()

    return res

def clean(item):
    return item.strip().replace('&quot', '\"').replace(' ,', ',')

def get_stuff_by_xpath():
    root = html_get_from_website(site, site_filename_temp, 'cp1251', method_xpath)
    parsed_items = []

    catalog = root.xpath("//div[@id='catalog']/div/div")
    for div in catalog:
        item = div.xpath(".//div[@class='item-all-title']")

        item_name = div.xpath(".//a/text()")
        if (item_name):
            name = clean(item_name[0])

            item_price = div.xpath(".//div[@class='item-price']")
            price = div.xpath(".//b/text()")[0] + div.xpath(".//b/span/text()")[0]

            img = "https:" + div.xpath(".//img/@src")[0]

            item_info = div.xpath(".//div[@class='article']")
            info = {}
            for article in item_info:
                split = article.xpath(".//text()")[0].split(': ')
                if (split[1] != '0 гр/ед'):
                    info.update({split[0]: split[1]})

            elem = {'name': name,
                    'price': price,
                    'info': info,
                    'image': img}
            #print(elem)
            parsed_items += [elem]
        #else: #Элемент отсутствует на сайте

    json_save(site_filename_xpath, parsed_items)

def get_stuff_by_bsoup():
    text = html_get_from_website(site, site_filename_temp, 'cp1251', method_bs)
    parsed_items = []
    soup = bs4.BeautifulSoup(text, "lxml")

    catalog = soup.findAll("div", class_='catalog-item-card item-tb')

    for div in catalog:
        item_name = div.find("a", class_='item-title')

        if (item_name):
            name = clean(item_name.text)

            item_price = div.find("span", class_='catalog-item-price')
            price = div.find("b").text

            img = "https:" + div.find("img")['src']

            item_info = div.findAll("div", class_='article')
            info = {}
            for article in item_info:
                split = article.text.split(': ')
                if (split[1] != '0 гр/ед'):
                    info.update({split[0]: split[1]})

            elem = {'name': name,
                    'price': price,
                    'info': info,
                    'image': img}
            #print(elem)
            parsed_items += [elem]
        #else: #Элемент отсутствует на сайте

    json_save(site_filename_bs, parsed_items)

