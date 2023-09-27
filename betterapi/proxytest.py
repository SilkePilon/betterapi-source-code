import requests

headers = {
    'Content-Type': 'application/json',
}

create = {
    'cmd': 'sessions.create',
    'session' : "MAIN",
    'maxTimeout': 60000,
}

json_data = {
    'cmd': 'request.get',
    'session': "MAIN",
    'url': 'https://you.com/api/streamingSearch?q=hi&page=1&count=10&safeSearch=Moderate&onShoppingPage=false&mkt=&responseFilter=WebPages,Translations,TimeZone,Computation,RelatedSearches&domain=youchat&queryTraceId=54ad0387-3523-4d96-8267-c1f67c55010a&chat=%5B%7B%22question%22%3A%22there%22%2C%22answer%22%3A%22I%27m%20sorry%2C%20I%27m%20not%20sure%20what%20you%20are%20asking%20about%20%5C%22there%5C%22.%20Can%20you%20please%20provide%20more%20context%20or%20clarify%20your%20question%3F%22%7D%2C%7B%22question%22%3A%22there%22%2C%22answer%22%3A%22I%27m%20sorry%2C%20it%27s%20not%20clear%20what%20your%20question%20is%20related%20to%20the%20term%20%5C%22there%5C%22.%20Could%20you%20please%20provide%20more%20context%20or%20clarify%20your%20question%3F%22%7D%5D&chatId=68a4ab10-520e-4d58-b152-eb97f1a29978',
    'maxTimeout': 60000,
}


# session = requests.post('http://192.168.2.151:8191/v1', headers=headers, json=create).json()
# print(session)
response = requests.post('http://192.168.2.151:8191/v1', headers=headers, json=json_data).json()

print(response['solution']['response'])

