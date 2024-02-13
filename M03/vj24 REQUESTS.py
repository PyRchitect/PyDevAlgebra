import requests

# https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

URL_01 = 'https://www.algebra.hr'
URL_02 = 'https://izradaweb.hr'
URL_03 = 'https://www.york.ac.uk/teaching/cws/wws/webpage1.html'

def get_site_status_code(URL):
	response = requests.get(URL)
	print(response.status_code)

def get_site(URL):
	response = requests.get(URL)
	print(response.content)

def get_site_headers(URL):
	response = requests.get(URL)
	print(response.headers)

def get_site_text(URL):
	response = requests.get(URL)
	print(response.text)

# get_site_status_code(URL_01)
# get_site(URL_01)
# get_site_headers(URL_01)
get_site_text(URL_01)