# Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)
mongo_base = client['mvideo']
hits = mongo_base.hits
driver = webdriver.Chrome('/Users/sergeysolovyev/Синхро/python/Crawling/venv/lesson_7/chromedriver')
driver.get('https://www.mvideo.ru/')
assert "М.Видео" in driver.title

for i in range(1, 4):
    button_next = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//div[9]//div[1]//div[2]//div[1]//div[1]//div[1]//div[2]//a[{i}]")))
    driver.execute_script("$(arguments).click();", button_next)
    carousel = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='c-product-tile-picture__holder']//a"))
    )
    for li in range(4, 10):
        info = carousel[li].get_attribute('data-product-info')
        print(type(info), info)
        try:
            hits.insert_one(json.loads(carousel[li].get_attribute('data-product-info')))
        except Exception as e:
            print(e)

driver.quit()
