from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as Mongo_Duplicate_Err
import datetime

today_date = datetime.datetime.now().date()

client = MongoClient('127.0.0.1', 27017)
db = client['news']
mongo_db = db.news

header = {'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

news_item = {} # title, link, datetime, source
url = "https://yandex.ru/news/"
response1 = requests.get(url) # Mail.Ru News
dom = html.fromstring(response1.text)

main_news = dom.xpath('//article')

for news in main_news:
    title = news.xpath('.//h2/text()')
    title = str(title[0]).replace('\xa0',' ')
    link = news.xpath('.//div/a/@href')
    link = str(link[0])
    date_stamp = news.xpath('.//span[@class="mg-card-source__time"]/text()')[0]
    date_stamp = str(today_date)+"T"+date_stamp+":00+09:00"
    source = str(news.xpath('.//a[@aria-label]/text()')[0])

    # news_item["title"] = title
    # news_item["link"] = link
    # news_item["datetime"] = date_stamp
    # news_item["source"] = source
    #
    # pprint(news_item)

    try:
        mongo_db.insert_one({'_id':link,
                             'title':title,
                             'link':link,
                             'datetime':date_stamp,
                             'source':source})
        print(f"Added to DB: {title}")
    except Mongo_Duplicate_Err:
        print(f"Already in DB: {title}")
