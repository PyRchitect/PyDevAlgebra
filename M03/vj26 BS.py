import requests
from bs4 import BeautifulSoup

URL = 'https://www.algebra.hr'
URL_COVID = 'https://www.worldometers.info/coronavirus'

def parse_url_01():

	stranica = BeautifulSoup(requests.get(URL).content,'html.parser')

	svi_paragrafi=stranica.find_all('p')
	print(svi_paragrafi[1])

	svi_linkovi_a = stranica.find_all('a')
	print(svi_linkovi_a)

def parse_url_02():

	covid_stranica = BeautifulSoup(requests.get(URL_COVID).content,'html.parser')
	
	svi_podaci = covid_stranica.find_all('div',id='maincounter-wrap')
	# print(svi_podaci)

	coronavirus_cases = svi_podaci[0]
	print(coronavirus_cases)

	naslov = coronavirus_cases.find('h1').get_text()
	print(naslov)

# parse_url_01()
parse_url_02()