import requests
from bs4 import BeautifulSoup

import sys

def get_ocjena(tag):
	for (naziv,broj_zvjezdica) in opis_ocjena.items():
		if naziv in tag["class"]:
			return broj_zvjezdica

opis_ocjena = {
	"One":"*",
	"Two":"* *",
	"Three":"* * *",
	"Four":"* * * *",
	"Five":"* * * * *"
}

cijena_selector = '.price_color'
naslov_selector = '.product_pod h3 a'
ocjena_selector = '.star-rating'

sirovi_podaci = requests.get("http://books.toscrape.com").content
sadrzaj = BeautifulSoup(sirovi_podaci,"html.parser")

cijene = sadrzaj.select(cijena_selector)
naslovi = sadrzaj.select(naslov_selector)
ocjene = sadrzaj.select(ocjena_selector)

# for n in naslovi:
# 	print(n['title'])
filepath = sys.path[0] + '\\' + 'books.csv'
with open(filepath,"w",encoding='utf-8') as fw:
	for (cijena,naslov,ocjena) in zip(cijene,naslovi,ocjene):
		fw.write(f"{naslov['title']};{cijena.string};{get_ocjena(ocjena)}\n")