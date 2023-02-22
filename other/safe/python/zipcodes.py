import requests
import urllib.request as u
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_and_store_zipcodes():
	url = "https://www.georgia-demographics.com/zip_codes_by_population"
	r = requests.get(url)
	text = r.text

	s = "<a href=\"30573-demographics\">"
	zipCodes = text.split("-demographics")

	with open("../resources/zipcodes.txt", "w") as f:
		c = 0
		for z in zipCodes:
			if c > 0:
				print("here ", c, ": ", z[2:7])
				f.write(z[2:7]+"\n")
			c += 1


# param start_index = what index zipcode to start at | index 0
def getReps(start_index):
	with open("../resources/zipcodes.txt", "r") as f:
		GAzipcodes = f.readlines()
	with open("../resources/zip-to-lat-long.txt", "r") as f:
		zipcodesLatLong = f.readlines()
	
	start = time.time()
	for i in range(start_index, len(GAzipcodes), 1):
		time.sleep(2)
		for d in zipcodesLatLong:
			if str(GAzipcodes[i].strip()) in str(d[:5]):
				lat = d.split(",")[1].strip()
				lng = d.split(",")[2].strip()
				url = f"https://v3.openstates.org/people.geo?lng={lng}&lat={lat}&apikey=21aacfcb-f25e-4105-811e-e2f3bb069f4e&include=offices&include=links"
				headers = {'authority': 'api.geocod.io', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
				request = requests.get(url, headers=headers)
				print("status: ", request)
				try:
					json = request.text
					rep_identifier = "ocd-division/country:us/state:ga/sldl:"
					s = json.split(rep_identifier)[1]
					firstName = re.search(r'given_name\"\:\"(.*?)\"', s).group(1)
					lastName = re.search(r'family_name\"\:\"(.*?)\"', s).group(1)
					email = re.search(r'email\"\:\"(.*?)\"', s).group(1)
					img = re.search(r'image\"\:\"(.*?)\"', s).group(1)
					if (len(firstName) > 0 and len(lastName) > 0 and len(email) > 0 and len(img) > 0):
						with open("../resources/zip-to-repinfo.txt", "r") as f:
							lines = f.readlines()
							c = 0
							for line in lines:
								curr = str(i + 1) + " " + str(GAzipcodes[i]).strip() + " " + str(firstName.strip()) + " " + str(lastName.strip()) + " " + str(email.strip()) + " " + str(img.strip()) + "\n"
								if (curr.strip() == line.strip()):
									c += 1
									print("IDENTICAL")
							if (c == 0):
								print(f"{i + 1}) {GAzipcodes[i].strip()}")
								print("     writing...")
								with open("../resources/zip-to-repinfo.txt", "a") as f:
									curr = str(i + 1) + " " + str(GAzipcodes[i].strip()) + " " + str(firstName.strip()) + " " + str(lastName.strip()) + " " + str(email.strip()) + " " + str(img.strip()) + "\n"
									f.write(curr)
								print("     " + firstName)
								print("     " + lastName)
								print("     " + email)
								print("     " + img + "\n")
							elif (c > 1):
								print("WARNING: duplicate found in zip-to-repinfo.txt")
								exit()
					else:
						getReps(i)
				except:
					print("too many requests! exiting program...")
					exit()
	end = time.time()
	print("runtime: " + str((end-start)/60) + " minutes")
		
with open("../resources/zip-to-repinfo.txt", "r") as f:
	lines = f.readlines()
	# if zip-to-repinfo.txt is not empty
	if (len(lines) != 0):
		lastLine = lines[len(lines) - 1]
		print("starting at: ", int(lastLine[0:3].strip()))
		getReps(int(lastLine[0:3].strip()) - 1)
	else:
		print("starting at: 0")
		getReps(0)




	