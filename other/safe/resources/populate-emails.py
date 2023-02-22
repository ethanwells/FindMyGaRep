# Ethan Wells

import requests
import re
import csv

# This program iterates through each row in "district-to-repInfo.csv"
# and dynamically populates all emails.
# Note: this program relies on the fact that the name and district number
#       of each representative are manually entered
# Note: due to special edge-case formatting on openstates website,
#       the email for these reps were inputted manually:
#       Reynaldo "Rey" Martinez
#       Pedro "Pete" Marin
#       Miriam Paris
#       Dar'shun Kendrick

html = requests.get("https://openstates.org/ga/legislators/?chamber=lower").text
objects = html.split("<li><a href=\"/person")[1:-1]
persons = []
for o in objects:
	person = re.search(r'/(.*?)</a></li>', o).group(1)
	persons.append(person)

c = 0
lines = list(csv.reader(open('district-to-repInfo.csv')))
with open("district-to-repInfo.csv") as f:
	datareader = csv.reader(f)
	for i, row in enumerate(datareader):
		print(i)
		name = row[0]
		# set email
		for person in persons:
			if name in person:
				link = "https://openstates.org/person/" + person.split("\">")[0].strip()
				r = requests.get(link)
				print(r)
				email = re.search(r'<a href="mailto:(.*?)">', r.text).group(1)
				lines[i][4] = email

		
writer = csv.writer(open('district-to-repInfo.csv', 'w'))
writer.writerows(lines)
print(c)







