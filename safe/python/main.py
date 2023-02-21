
from geocodio import GeocodioClient
import json as json
import re
import csv

# my api key
client = GeocodioClient("4076d8e183288236d678e34f8377fd22f77e343")

# params
street = ""
city = ""
zipcode = ""

# formatted address
address = f"{street} {city} {zipcode}"

# get state lower-chamber house district-number
parsed = str(client.parse(address))
formatted_address = str(re.search(r'\'formatted_address\'\: \'(.*?)\'', parsed).group(1).strip())
house_district_profile = str(client.geocode(formatted_address, fields=["stateleg-next"])).replace("\'", "\"")
house_district = re.search(r'State House District (.*?)\"', house_district_profile).group(1).strip()

# get rep info
with open("../resources/district-to-repInfo.csv", "r") as f:
	datareader = csv.reader(f)
	for i, row in enumerate(datareader):
		district = int(row[2].strip())
		if district == int(house_district):
			name = row[0]
			party = row[1]
			email = row[4]
			print(f"rep name: {name}")
			print(f"rep party: {party}")
			print(f"rep email: {email}")






