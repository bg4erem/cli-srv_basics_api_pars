from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['products']
mongo_products = db.products

rate = 80

search_result = mongo_products.find({'rate': {'$gt': rate}}, {'desc': 0, '_id': 0})

for product in search_result:
    pprint(product)
