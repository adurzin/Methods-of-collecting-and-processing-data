from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep


driver = webdriver.Chrome(executable_path='./chromedriver.exe')

driver.get('https://www.mvideo.ru/')

driver.execute_script("window.scrollTo(0, 1800);")  # скролл на необходимую высоту

wait = WebDriverWait(driver, 10)
button = wait.until(ec.element_to_be_clickable((By.XPATH, "//div[1]/div/button[2]")))
button.click()

while True:
    try:
        element = driver.find_element(By.XPATH, '//mvid-shelf-group/*/div[2]/button[2]')
        element.click()
        sleep(1)
    except:
        break

items = driver.find_elements(By.XPATH, "//mvid-shelf-group//div[@class='product-mini-card__name ng-star-inserted']")


for element in items:
    name = element.find_element(By.CLASS_NAME, "title").text
    # price = element.find_element(By.XPATH, "///span[@class='price__main-value']").text
    print(name)
