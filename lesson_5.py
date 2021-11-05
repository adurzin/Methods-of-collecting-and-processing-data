from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('127.0.0.1', 27017)

db = client['mvideo']
products = db.products

driver = webdriver.Chrome(executable_path='./chromedriver.exe')

driver.get('https://www.mvideo.ru/')

driver.execute_script("window.scrollTo(0, 1800);")  # скролл на необходимую высоту

wait = WebDriverWait(driver, 10)
button = wait.until(ec.element_to_be_clickable((By.XPATH, "//div[1]/div/button[2]")))
button.click()

while True:
    try:
        button = wait.until(ec.element_to_be_clickable((By.XPATH, '//mvid-shelf-group/*/div[2]/button[2]')))
        button.click()
    except:
        break

elements = driver.find_elements(By.XPATH, "//mvid-shelf-group/mvid-carousel/div[1]/div/mvid-product-cards-group/div")

product = {}

for el in elements:
    try:
        name = el.find_element(By.CLASS_NAME, 'title').text
        link = el.find_element(By.TAG_NAME, 'a').get_attribute('href')
        product['_id'] = link[:10:-1]
        product['name'] = name
        product['link'] = link
    except:
        pass

    try:
        price = el.find_element(By.CLASS_NAME, 'price__main-value').text
        product['price'] = price

        try:
            db.products.insert_one(product)
        except DuplicateKeyError:
            print("Продукт уже существует в базе")
        product = {}

    except:
        pass

driver.quit()
