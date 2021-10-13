from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get('https://gb.ru/login')

assert 'GeekBrains' in driver.title

# elem = driver.find_element_by_id("user_email")
elem = driver.find_element(By.ID, "user_email")
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element(By.ID, "user_password")
elem.send_keys('Password172')

elem.send_keys(Keys.ENTER)

time.sleep(3)

profile = driver.find_element(By.XPATH, "//a[contains(@href,'/users/')]")
link_profile = profile.get_attribute('href')
driver.get(link_profile)

time.sleep(3)
button = driver.find_element(By.CLASS_NAME, 'text-sm')
driver.get(button.get_attribute('href'))



# driver.close()