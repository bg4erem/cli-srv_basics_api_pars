# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests

url = "https://api.hunter.io/v2/email-verifier"
email = "support@geekbrains.ru"
with open("homework_2_api-source", "r") as api_file:
    api_key = api_file.readline()
my_params = {"email": email, "api_key": api_key}

response = requests.get(url, params=my_params)

with open("homework_2_result", "w") as result_file:
    print(response.text, file=result_file)
    print(f"Request data has been saved to {result_file.name}")

if response.json().get("data").get("status") == "invalid":
    print(f"Email '{email}' is invalid")
elif response.json().get("data").get("status") == "accept_all" or "webmail":
    print(f"Email '{email}' is active and deliverable")
