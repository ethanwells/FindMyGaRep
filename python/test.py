import requests as r

url = "https://www.zipdatamaps.com/00601"

response = r.get(url)
json = response.text
print(json)
