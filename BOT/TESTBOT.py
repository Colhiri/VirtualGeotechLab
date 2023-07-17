import requests

url = "https://api.telegram.org/bot{token}/{method}".format(
    token="5817177597:AAFldPHKS5vSco58icQU56ALbgiQAqyrxT4",
    # method="setWebhook",
    # method="getWebhookinfo",
    # method = "deleteWebhook"
)

data = {"url": "https://functions.yandexcloud.net/d4e8tjpk50un36kkl17a"}

r = requests.post(url, data=data)
print(r.json())
