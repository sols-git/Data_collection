# Написать программу, которая собирает входящие письма из своего или
# тестового почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
mongo_base = client['mail']
collection = mongo_base.collection
driver = webdriver.Chrome('/Users/sergeysolovyev/Синхро/python/Crawling/venv/lesson_7/chromedriver')
driver.get('https://m.mail.ru/login')
assert "Вход — Почта Mail.Ru" in driver.title
elem = driver.find_element_by_name('Login')
elem.send_keys('study.ai_172@mail.ru')
elem = driver.find_element_by_name('Password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)
last_mail = driver.find_element_by_xpath("//a[@class='messageline__link']").get_attribute('href')
driver.get(last_mail)
end_mails = 0
while end_mails == 0:
    item = {}
    item['from'] = str(driver.find_elements_by_class_name("readmsg__text-container__inner-line")[0].text)[4:]
    item['date'] = str(driver.find_elements_by_class_name("readmsg__text-container__inner-line")[1].text).split('\n')[0]
    item['theme'] = str(driver.find_element_by_class_name("readmsg__theme-box__line").text)
    item['body'] = str(driver.find_element_by_id("readmsg__body").text)
    try:
        collection.insert_one(item)
    except Exception as e:
        print(e)
    next_mail = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH,"//div[@class='readmsg__horizontal-block__right-block']//a"))
        )
    next_mail = next_mail.get_attribute('href')
    try:
        driver.get(next_mail)
    except exceptions.NoSuchElementException:
        print('End of the mail list')
        end_mails = 1
        break

driver.quit()
