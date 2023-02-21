import requests

url = "https://obscure-beyond-79368.herokuapp.com/get_rep_info"

params = {
    "streetAddress": "200 River Vista Dr Atlanta Dr",
    "zipcode": "30339"
}

r = requests.get(url, params=params)

print(r.text)

#print(r.text)
