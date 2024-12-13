import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from Lab6.login_const import login, password
from Lab3.main import MongoWork

mongo = MongoWork()
coll_name = 'mail_ru_with_spider'


def get_random_sleep():
    return random.uniform(0.4, 0.7)


def get_mails_by_selenium():
    edge_options = webdriver.EdgeOptions()
    driver = webdriver.Edge(options=edge_options)
    driver.get("https://e.mail.ru/inbox/")

    # input email
    input = driver.find_element(By.NAME, "username")
    submit = driver.find_element(By.XPATH, "//button[@class='base-0-2-79 primary-0-2-93 auto-0-2-105']")
    time.sleep(get_random_sleep())
    input.send_keys(login)
    time.sleep(get_random_sleep())
    submit.click()

    time.sleep(get_random_sleep())

    # choose another method
    submit = driver.find_element(By.XPATH, "//button[@class='base-0-2-79 fluid-0-2-86 auto-0-2-105']")
    submit.click()

    time.sleep(get_random_sleep())

    # input password
    input = driver.find_element(By.NAME, "password")
    submit = driver.find_element(By.XPATH, "//button[@class='base-0-2-79 primary-0-2-93 auto-0-2-105']")
    time.sleep(get_random_sleep())
    input.send_keys(password)
    time.sleep(get_random_sleep())
    submit.click()

    # wait to load page
    #time.sleep(10)
    #WebDriverWait(driver, 11).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "html")))
    WebDriverWait(driver, 11).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "html")))
    time.sleep(1)

    numb = 0
    mail_list_len = len(driver.find_elements(By.XPATH, "//div[@class='ReactVirtualized__Grid__innerScrollContainer']/a"))
    while numb < mail_list_len:
        # try proceed and wait
        mail = driver.find_elements(By.XPATH, "//div[@class='ReactVirtualized__Grid__innerScrollContainer']/a")[numb]
        time.sleep(get_random_sleep())
        mail.click()
        try:
            WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, "//h2[@class='thread-subject']")))
        except:
            driver.back()
            continue

        # get elements
        title = driver.find_element(By.XPATH, "//h2[@class='thread-subject']")
        author = driver.find_element(By.XPATH, "//span[@class='letter-contact']")
        email = driver.find_element(By.XPATH, "//span[@class='letter-contact']")
        date = driver.find_element(By.XPATH, "//div[@class='letter__date']")
        text = driver.find_element(By.XPATH, "//div[@class='js-helper js-readmsg-msg']/div/div/div")
        downloads = driver.find_elements(By.XPATH, "//a[@class='attach-list__controls-element-download']")
        if downloads:
            downloads[0].click()

        elem = {
                'title': title.text,
                'author': author.text,
                'email': email.get_attribute('title'),
                'date': date.text,
                'text': text.text
                }

        mongo.add(elem, ['title', 'author', 'email', 'date'], coll_name)
        time.sleep(get_random_sleep())
        driver.back()
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "html")))
        time.sleep(1)
        numb += 1

    pass


