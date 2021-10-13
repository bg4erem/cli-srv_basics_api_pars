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
url = "https://lenta.ru"
response1 = requests.get("https://lenta.ru/") # Mail.Ru News
dom = html.fromstring(response1.text)

main_news = dom.xpath('//div[@class="b-yellow-box__wrap"]/div/a[not(@class="b-link-external")]')

for news in main_news:
    title = news.xpath('.//text()')
    title = str(title[0]).replace('\xa0',' ')
    link_short = news.xpath('.//@href')
    link = url+str(link_short[0])
    news_parser = requests.get(link)
    news_parser_dom = html.fromstring(news_parser.text)
    date_stamp = news_parser_dom.xpath('//div[@class="b-topic__info"]/time[@class="g-date"]/@datetime')
    date_stamp = date_stamp[0]
    source = "lenta.ru"

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
