import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

url = 'https://roscontrol.com'
search_request = "яйца"
params = {"keyword": search_request, "page": 1}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

# pprint(products_list)

while True:
    response = requests.get(url + '/testlab/search', params=params, headers=headers)

    soup = bs(response.text, "html.parser")
    if not soup.find("a", attrs={"class":"page-num page-item last"}):
        break
    products_list = soup.find_all("a", attrs={
        "class": "block-product-catalog__item js-activate-rate util-hover-shadow clear"})
    products = []

    for product in products_list:
        product_database = {}
        product_name = product.find("div", attrs={"class":"product__item-link"}).text
        product_img = product.find("img").get("src")
        try:
            product_rate = int(product.find("div", attrs={"class":"rating-value"}).text)
        except AttributeError:
            product_rate = 0
        product_desc = product.find("div", attrs="product__item-text").text

        product_database['name'] = product_name
        product_database['img'] = product_img
        product_database['rate'] = product_rate
        product_database['description'] = product_desc

        products.append(product_database)
    params['page'] += 1

pprint(products)