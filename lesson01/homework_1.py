# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
from pprint import pprint
file = open("homework_1.json", "w")

username = "bg4erem"
url = f"https://api.github.com/users/{username}/repos"

response = requests.get(url)
pprint(response.json())
print(response.json(), file=file)
print(f'This JSON content saved to {file.name}')

file.close()
