from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as Mongo_Duplicate_Err


client = MongoClient('127.0.0.1', 27017)
db = client['news']
mongo_db = db.news

header = {'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

news_item = {} # title, link, datetime, source

response1 = requests.get("https://news.mail.ru/") # Mail.Ru News
dom = html.fromstring(response1.text)

news_main_photo = dom.xpath("//span[contains(@class, 'photo__title_new')]") # main news with photo

for news in news_main_photo:
    title = news.xpath(".//text()")
    link = news.xpath("./../../@href")
    newsparser = requests.get(link[0])
    dom_newsparser = html.fromstring(newsparser.text)
    datestamp = dom_newsparser.xpath("//span/@datetime")
    source = dom_newsparser.xpath('//span[@class="note"]/a/span[@class="link__text"]/text()')

    news_item['title'] = title[0]
    news_item['link'] = link[0]
    news_item['datetime'] = datestamp[0]
    news_item['source'] = source[0]

    try:
        mongo_db.insert_one({'_id':link[0],
                         'title':title[0],
                         'link':link[0],
                         'datetime':datestamp[0],
                         'source':source[0]})
        print(f"Added to DB: {title}")
    except Mongo_Duplicate_Err:
        print(f"Already in DB: {title}")
        continue

news_main = dom.xpath("//li") # main news with no photo

for news in news_main:
    title = news.xpath(".//a/text() | .//a/span/text()")
    link = news.xpath(".//a/@href")
    newsparser = requests.get(link[0])
    dom_newsparser = html.fromstring(newsparser.text)
    datestamp = dom_newsparser.xpath("//span/@datetime")
    source = dom_newsparser.xpath('//span[@class="note"]/a/span[@class="link__text"]/text()')

    news_item['title'] = title[0]
    news_item['link'] = link[0]
    news_item['datetime'] = datestamp[0]
    news_item['source'] = source[0]

    try:
        mongo_db.insert_one({'_id':link[0],
                         'title':title[0],
                         'link':link[0],
                         'datetime':datestamp[0],
                         'source':source[0]})
        print(f"Added to DB: {title}")
    except Mongo_Duplicate_Err:
        print(f"Already in DB: {title}")
        continue

news1_sub_main = dom.xpath("//a[contains(@class, 'newsitem__title')]") # main news from topic blocks

for news in news1_sub_main:
    title = news.xpath(".//span/text()")
    link = news.xpath("./@href")
    newsparser = requests.get(link[0])
    dom_newsparser = html.fromstring(newsparser.text)
    datestamp = dom_newsparser.xpath("//span/@datetime")
    source = dom_newsparser.xpath('//span[@class="note"]/a/span[@class="link__text"]/text()')

    news_item['title'] = title[0]
    news_item['link'] = link[0]
    news_item['datetime'] = datestamp[0]
    news_item['source'] = source[0]

    try:
        mongo_db.insert_one({'_id':link[0],
                         'title':title[0],
                         'link':link[0],
                         'datetime':datestamp[0],
                         'source':source[0]})
        print(f"Added to DB: {title}")
    except Mongo_Duplicate_Err:
        print(f"Already in DB: {title}")
        continue
