import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as Mongo_Duplicate_Err

client = MongoClient('127.0.0.1', 27017)
db = client['products']
mongo_storage_products = db.products

url = 'https://roscontrol.com'
search_request = "мясо"
params = {"keyword": search_request, "page": 1}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

# pprint(products_list)

while True:
    response = requests.get(url + '/testlab/search', params=params, headers=headers)

    soup = bs(response.text, "html.parser")
    if not soup.find("a", attrs={"class": "page-num page-item last"}):
        break
    products_list = soup.find_all("a", attrs={
        "class": "block-product-catalog__item js-activate-rate util-hover-shadow clear"})
    products = []

    for product in products_list:
        product_database = {}
        product_name = product.find("div", attrs={"class": "product__item-link"}).text
        product_img = product.find("img").get("src")
        try:
            product_rate = int(product.find("div", attrs={"class": "rating-value"}).text)
        except AttributeError:
            product_rate = None
        product_desc = str(product.find_all("div", attrs="product__item-text"))

        product_database['name'] = product_name
        product_database['img'] = product_img
        product_database['rate'] = product_rate
        product_database['description'] = product_desc

        products.append(product_database)

        try:
            mongo_storage_products.insert_one({"_id":product_img,
                                               "name":product_name,
                                               "rate":product_rate,
                                               "img":product_img,
                                               "desc":product_desc})
            print(f'Added to DB: {product_name}')
        except Mongo_Duplicate_Err:
            print(f'DB Error: Product {product_name} already exists!')
            pass



    params['page'] += 1

# pprint(products)
