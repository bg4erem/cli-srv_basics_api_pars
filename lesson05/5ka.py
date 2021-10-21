from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions as se

chrome_options = Options()
# chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.get('https://5ka.ru/special_offers/')

counter = 0
while True:
    try:
        # button = driver.find_element(By.CLASS_NAME, 'special-offers__more-btn')
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'special-offers__more-btn')))
        button.click()
        counter += 1
    except se.ElementNotInteractableException:
        break

print(counter)
