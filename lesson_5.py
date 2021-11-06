from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException


client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
products = db.products

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.get('https://www.mvideo.ru/')

driver.execute_script("window.scrollTo(0, 1900);")  # скролл на необходимую высоту

wait = WebDriverWait(driver, 5)
button = wait.until(ec.element_to_be_clickable((By.XPATH, "//div[1]/div/button[2]")))
button.click()

while True:
    try:
        button = wait.until(ec.element_to_be_clickable((By.XPATH, '//mvid-shelf-group/*/div[2]/button[2]')))
        button.click()
    except (ElementNotInteractableException, TimeoutException):
        break

elements = driver.find_elements(By.XPATH, "//mvid-shelf-group/mvid-carousel/div[1]//div[@class='title']")

product = {}

print(len(elements))
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                         " Chrome/95.0.4638.69 Safari/537.36"}

for el in elements:
    link = el.find_element(By.TAG_NAME, 'a').get_attribute('href')
    print([link])
    driver.execute_script(f'''window.open("{link}", "_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    wait.until(ec.element_to_be_clickable((By.XPATH, "//mvideoru-cart-button/button | //mvid-mprime-button//button")))
    name = driver.find_element(By.XPATH, "//h1[@class='title']").text
    print(name)
    price = driver.find_element(By.XPATH, "//span[@class='price__main-value'][1]").text
    print(price)
    product = {'link': link,
               'name': name,
               'price': price,
               '_id': link[10::-1]
               }
    try:
        db.products.insert_one(product)
    except DuplicateKeyError:
        print("Этот продукт уже есть в базе данных")
    product = {}
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

driver.quit()
