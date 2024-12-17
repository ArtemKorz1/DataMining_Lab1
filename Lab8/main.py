from playwright.sync_api import Playwright, sync_playwright
from lxml import html
import bs4

from Lab1.main import JsonWork

lab8_suffix = 'Lab8\\'
link = 'https://twitch.tv'


def get_screenshot_by_playwright():
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto('https://twitch.tv/')
        page.screenshot(path="twitch.jpg")
        browser.close()


def get_list_by_locator(page):
    return page.locator("//div[@class='OBUFH ScTransitionBase-sc-hx4quq-0 tw-transition']")

def get_list_by_xpath(page):
    content = html.fromstring(page.content())
    list = content.xpath("//div[@class='OBUFH ScTransitionBase-sc-hx4quq-0 tw-transition']")
    return list

def get_list_by_bs(page):
    soup = bs4.BeautifulSoup(page.content(), "lxml")
    list = soup.findAll("div", class_='OBUFH ScTransitionBase-sc-hx4quq-0 tw-transition')
    return list

def get_element_by_locator(page, numb):
    elem = {
        'title': page.locator("//h3[@class='CoreText-sc-1txzju1-0 kBMZbI']").nth(numb).inner_text(),
        'author': page.locator("//div[@class='Layout-sc-1xcs6mc-0 bQImNn']").nth(numb).inner_text(),
        'category': page.locator("//a[@class='ScCoreLink-sc-16kq0mq-0 jRnnHH tw-link']").nth(numb).inner_text(),
        'viewers': page.locator("//div[@class='ScMediaCardStatWrapper-sc-anph5i-0 jRUNHm tw-media-card-stat']").nth(
            numb).inner_text(),
        'ref': link + page.locator("//a[@class='ScCoreLink-sc-16kq0mq-0 hcWFnG preview-card-image-link tw-link']").nth(
            numb).get_attribute('href'),
        'tags': page.locator("//div[@class='InjectLayout-sc-1i43xsx-0 gNgtQs']").nth(numb).inner_text().split('\n')
    }
    return elem

def get_element_by_xpath(list, numb):
    el = list[numb]
    elem = {
        'title': el.xpath(".//h3[@class='CoreText-sc-1txzju1-0 kBMZbI']/text()")[0],
        'author': el.xpath(".//div[@class='Layout-sc-1xcs6mc-0 bQImNn']/text()")[0],
        'category': el.xpath(".//a[@class='ScCoreLink-sc-16kq0mq-0 jRnnHH tw-link']/text()")[0],
        'viewers': el.xpath(".//div[@class='ScMediaCardStatWrapper-sc-anph5i-0 jRUNHm tw-media-card-stat']/text()")[0],
        'ref': link + el.xpath(".//a[@class='ScCoreLink-sc-16kq0mq-0 hcWFnG preview-card-image-link tw-link']/@href")[0],
        'tags': el.xpath(".//div[@class='ScTruncateText-sc-i3kjgq-0 ickTbV']/span/text()")
    }
    return elem

def get_element_by_bs(list, numb):
    el = list[numb]
    tags_el = el.findAll("div", class_="ScTruncateText-sc-i3kjgq-0 ickTbV")
    tags = []
    for tag in tags_el:
        tags += [tag.text]
    elem = {
        'title': el.find("h3", class_="CoreText-sc-1txzju1-0 kBMZbI").text,
        'author': el.find("div", class_="Layout-sc-1xcs6mc-0 bQImNn").text,
        'category': el.find("a", class_="ScCoreLink-sc-16kq0mq-0 jRnnHH tw-link").text,
        'viewers': el.find("div", class_="ScMediaCardStatWrapper-sc-anph5i-0 jRUNHm tw-media-card-stat").text,
        'ref': link + el.find("a", class_="ScCoreLink-sc-16kq0mq-0 hcWFnG preview-card-image-link tw-link")['href'],
        'tags': tags
    }
    return elem


def get_content(method):
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto('https://twitch.tv')
        page.locator("//div[@class='Layout-sc-1xcs6mc-0 cVWYqz']").wait_for()

        parsed = []
        if method == 'locator':
            list = get_list_by_locator(page)
        elif method == 'xpath':
            list = get_list_by_xpath(page)
        elif method == 'bs':
            list = get_list_by_bs(page)

        numb = 0
        while numb < 6:
            if method == 'locator':
                elem = get_element_by_locator(page, numb)
            elif method == 'xpath':
                elem = get_element_by_xpath(list, numb)
            elif method == 'bs':
                elem = get_element_by_bs(list, numb)

            parsed += [elem]
            print(elem)
            numb += 1

        print(parsed)
        JsonWork.save(lab8_suffix + "by_" + method + ".json", parsed)
        browser.close()


def get_with_request():
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto('https://twitch.tv')
        input = page.locator("//input[@class='ScInputBase-sc-vu7u7d-0 ScInput-sc-19xfhag-0 gNGlOQ gnCxBd InjectLayout-sc-1i43xsx-0 eRDdjS tw-input tw-input--large']")
        input.wait_for()
        input.type("league of legends", delay=0.2)
        page.locator("//button[@class='ScCoreButton-sc-ocjdkq-0 gFUsAR tw-combo-input__button-icon tw-combo-input__button-icon--large']").click()

        page.locator("//p[@class='CoreText-sc-1txzju1-0 MveHm']").last.wait_for()
        content = html.fromstring(page.content())
        list = content.xpath("//div[@class='Layout-sc-1xcs6mc-0 ivrFkx']")
        list.pop(0)
        parsed = []
        numb = 0
        while numb < 10:
            el = list[numb]
            try:
                title = el.xpath(".//p[@class='CoreText-sc-1txzju1-0 MveHm']/text()")[1]
            except:
                page.locator("//button[@class='ScCoreButton-sc-ocjdkq-0 gjSLzh']").nth(0).click()
                page.locator("//p[@class='CoreText-sc-1txzju1-0 MveHm']").last.wait_for()
                page.locator("//div[@class='Layout-sc-1xcs6mc-0 ivrFkx']").nth(numb).scroll_into_view_if_needed()
                content = html.fromstring(page.content())
                list = content.xpath("//div[@class='Layout-sc-1xcs6mc-0 ivrFkx']")
                list.pop(0)
                el = list[numb]
                title = el.xpath(".//p[@class='CoreText-sc-1txzju1-0 MveHm']/text()")[1]

            elem = {
                'title': title,
                'author': el.xpath(".//a[@class='ScCoreLink-sc-16kq0mq-0 jRnnHH tw-link']/text()")[0],
                'category': el.xpath(".//a[@class='ScCoreLink-sc-16kq0mq-0 jRnnHH tw-link']/text()")[0],
                'viewers':
                    el.xpath(".//p[@class='CoreText-sc-1txzju1-0 MveHm']/text()")[0],
                'ref': link +
                       el.xpath(".//a[@class='ScCoreLink-sc-16kq0mq-0 jRnnHH tw-link']/@href")[0],
                'tags': el.xpath(".//div[@class='ScTruncateText-sc-i3kjgq-0 ickTbV']/span/text()")
            }
            parsed += [elem]
            print(elem)
            numb += 1

        print(parsed)
        JsonWork.save(lab8_suffix + "with_request.json", parsed)
        browser.close()