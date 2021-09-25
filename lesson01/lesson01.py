import requests
from pprint import pprint

city = 'yakutsk'
my_params = {
    'q': city,
    'appid': 'e5e4cd692a72b0b66ea0a6b80255d1c3'
}

url = "http://api.openweathermap.org/data/2.5/weather"

response = requests.get(url, params=my_params)
j_data: object = response.json()
# pprint(j_data)
pprint(f'В городе {j_data.get("name")} температура {round(j_data.get("main").get("temp") - 273.15, 2)} градусов')