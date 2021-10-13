from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as Mongo_Duplicate_Err
import time

client = MongoClient('127.0.0.1', 27017)
db = client['emails']
mongo_db = db.emails

driver = webdriver.Chrome('./chromedriver')
driver.get('https://account.mail.ru/login')

time.sleep(2)
field = driver.find_element(By.XPATH, '//input[@placeholder="Account name"]')
field.send_keys('study.ai_172@mail.ru')
field.send_keys(Keys.ENTER)

time.sleep(2)

field = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
field.send_keys('NextPassword172???')
field.send_keys(Keys.ENTER)

time.sleep(2)
driver.get('https://e.mail.ru/inbox/')
time.sleep(3.5)

email_links = []

k = 0
last_link = str
while True:
    emails = driver.find_elements(By.XPATH, "//a[contains(@class, 'llc')]")
    element = emails[1]
    last_checker = emails[-1].get_attribute('href')
    if last_checker == last_link:
        break
    for email_link in emails:
        email_link = email_link.get_attribute('href')
        if email_link not in email_links:
            email_links.append(str(email_link))
        last_link = email_link
    element.send_keys(Keys.END)
    time.sleep(2.2)


print(f'Len of emails: {len(email_links)}')
pprint(email_links)

email_info = {} #from, date, subject, body

for el in email_links:
    if el is None:
        email_links.remove(el)

for link in email_links:
    driver.get(link)
    time.sleep(1.5)
    from_address = driver.find_element(By.XPATH, '//span[@class="letter-contact"]')
    from_address = from_address.get_attribute('title')
    date = driver.find_element(By.XPATH, '//div[@class="letter__date"]').text
    subject = driver.find_element(By.XPATH, '//h2[@class="thread__subject"]').text
    body = driver.find_element(By.XPATH, '//div[@class="letter-body"]').text

    email_info['from'] = from_address
    email_info['date'] = date
    email_info['subject'] = subject
    email_info['body'] = body

    try:
        mongo_db.insert_one({'_id':link,
                         'from':from_address,
                         'date':date,
                         'subject':subject,
                         'body':body})
        print(f"Added to DB: Email {subject} from {from_address} received {date}")
    except Mongo_Duplicate_Err:
        print(f"Error, already in DB: Email {subject} from {from_address} received {date}")
        continue
