import requests
import json

url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()
json_object = json.dumps(data, indent=4)
with open("sample.json", "w") as outfile:
    outfile.write(json_object)