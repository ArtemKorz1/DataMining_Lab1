import time

from playwright.sync_api import Playwright, sync_playwright

from Lab6.main import get_random_sleep
from Lab6.login_const import login, password
from Lab3.main import MongoWork

mongo = MongoWork()
coll_name = 'mail_ru_with_playwright'

def get_mails_by_playwright():
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto('https://e.mail.ru/inbox/')

        # input email
        page.wait_for_load_state()
        input = page.locator("//input[@name='username']")
        submit = page.locator("//button[@class='base-0-2-79 primary-0-2-93 auto-0-2-105']")
        time.sleep(get_random_sleep())
        input.type(login, delay=0.2)
        time.sleep(get_random_sleep())
        submit.click()

        time.sleep(get_random_sleep())

        # choose another method
        submit = page.locator("//button[@class='base-0-2-79 fluid-0-2-86 auto-0-2-105']")
        submit.click()

        time.sleep(get_random_sleep())

        # input password
        input = page.locator("//input[@name='password']")
        submit = page.locator("//button[@class='base-0-2-79 primary-0-2-93 auto-0-2-105']")
        time.sleep(get_random_sleep())
        input.type(password, delay=0.2)
        time.sleep(get_random_sleep())
        submit.click()

        # wait to load page
        page.locator("//div[@class='ReactVirtualized__Grid__innerScrollContainer']").wait_for()
        time.sleep(1)

        numb = 0
        mail_list = page.locator("//div[@class='ReactVirtualized__Grid__innerScrollContainer']/a")
        while True:
            mail_list = page.locator("//div[@class='ReactVirtualized__Grid__innerScrollContainer']/a")
            time.sleep(get_random_sleep())
            mail_list.nth(numb).click()

            page.locator("//h2[@class='thread-subject']").wait_for()

            # get elements
            title = page.locator("//h2[@class='thread-subject']").nth(0)
            author = page.locator("//span[@class='letter-contact']").nth(0)
            email = page.locator("//span[@class='letter-contact']").nth(0)
            date = page.locator("//div[@class='letter__date']").nth(0)
            text = page.locator("//div[@class='js-helper js-readmsg-msg']/div/div/div").nth(0)

            elem = {
                'title': title.inner_text(),
                'author': author.inner_text(),
                'email': email.get_attribute('title'),
                'date': date.inner_text(),
                'text': text.inner_text()
            }

            mongo.add(elem, ['title', 'author', 'email', 'date'], coll_name)

            if mail_list.nth(numb) == mail_list.last:
                break

            time.sleep(get_random_sleep())
            page.go_back()
            page.locator("//div[@class='ReactVirtualized__Grid__innerScrollContainer']").wait_for()
            time.sleep(1)
            numb += 1

        browser.close()