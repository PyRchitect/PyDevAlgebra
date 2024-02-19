# https://github.com/public-apis/public-apis

import urllib.request
import urllib.parse
import ssl

import json

import sys

# Madrid
URL = 'https://api.tutiempo.net/json/?lan=en&apid=zwDX4azaz4X4Xqs&ll=40.4178,-3.7022'

headers = {
	'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64;rv:12.0) Gecko/20100101 Firefox/12.0'
}

def open_url(URL):

	try:
		connection = urllib.request.Request(URL,headers=headers)
		context = ssl._create_unverified_context()
		with urllib.request.urlopen(connection,context=context) as response:
			site = response.read().decode()
	except Exception as e:
		print(f"Dogodila se greska {e}")
	
	return json.loads(site)

def write_json(dict_json):

	filename = 'Madrid.json'
	filepath = sys.path[0]+'\\'+filename

	try:
		with open(filepath,'w') as fw:
			json.dump(dict_json,fw)
	except Exception as e:
		print(f"Dogodila se greska {e}")

def show_report(dict_json):
	print(dict_json)
	print(dict_json['locality'])
	city = dict_json['locality']['name']
	country = dict_json['locality']['country']
	print(f"Vremenska prognoza za {city}, {country}")

dict_json = open_url(URL)
# write_json(dict_json)
# show_report(dict_json)