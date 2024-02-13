import urllib.request
import urllib.parse

URL_01 = 'https://www.algebra.hr'
URL_02 = 'https://izradaweb.hr'
URL_03 = 'https://www.york.ac.uk/teaching/cws/wws/webpage1.html'

headers = {
	'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64;rv:12.0) Gecko/20100101 Firefox/12.0'
}

def open_url(URL):

	try:
		connection = urllib.request.Request(URL,headers=headers)
		with urllib.request.urlopen(connection) as response:
			site = response.read().decode()		
	except Exception as e:
		print(f"Dogodila se greska {e}")

	# site = connection.read().decode()

	print(site)

# open_url(URL_01)
# open_url(URL_02)
# open_url(URL_03)

def search_url(upit):	
	encodirani_upit = urllib.parse.quote(upit)
	eu_utf8 = encodirani_upit.encode('utf-8')
	URL_UPIT = f'https://google.com/search?q={eu_utf8}'
	request = urllib.request.Request(URL_UPIT,headers=headers)
	try:
		with urllib.request.urlopen(request) as response:
			data = response.read().decode()
	except Exception as e:
		print(f"Dogodila se greska {e}")
	
	print(data)

# search_url('programiranje u pythonu')