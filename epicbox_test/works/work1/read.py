import json

with open("config.json") as js:
    data = json.load(js)
    print(data)


