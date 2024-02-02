import sys

def generalno():

	class NazivKlase:

		def __str__(self):
			return f"Moja klasa je {self.__class__} clean !"

		def __repr__(self):
			return "Moja klasa je " + str(self.__class__) + " raw !"

	objekt1 = NazivKlase()
	objekt2 = NazivKlase()

	print()
	print(f"{objekt1!s}")
	print(f"{objekt2!s}")
	print()
	print(f"{objekt1!r}")
	print(f"{objekt2!r}")
	print()
	print(f"{objekt1!a}")
	print(f"{objekt2!a}")
	print()
	sys.stdout.write(repr(objekt1))
	sys.stdout.write(repr(objekt2))

def TV():

	class TelevizijskiAparat():
		dijagonala=55
		sirina=124
		visina=79
		proizvodjac="Grundig"

	print(f"klasa: {TelevizijskiAparat.dijagonala }")

	moj_tv = TelevizijskiAparat()
	moj_tv.dijagonala = 66
	print(f"instanca prva: {moj_tv.dijagonala }")

	moj_tv_2 = TelevizijskiAparat()
	moj_tv_2.dijagonala = 77
	print(f"instanca druga: {moj_tv_2.dijagonala }")

def osobe():

	class Osoba():

		titula = {"g":"gospodin","gđa":"gospođa"}

		def __init__(self,ime=None,visina=None):
			self.ime = ime
			self.visina = visina

		def __str__(self):
			return f"ime: {self.ime}, visina: {self.visina}"

	lista_cekanja = []
	lista_cekanja.append(Osoba("Mate",180))
	lista_cekanja.append(Osoba("Stipe",190))

def meta():

	class ReadOnly:

		def __get__(self,instance,owner):
			print("> fetch ...")
			return instance._name

		def __set__(self,instance,value):
			print("> change ...")
			# instance._name = value
			raise AttributeError("Cannot set!")

		def __delete__(self,instance):
			print('> remove ...')
			del instance._name

	class Person:
		def __init__(self,attr):
			self._attr = attr
		# assign descriptor to attr
		attr = ReadOnly()

	netko = Person("Ime")
	netko.attr = "Drugo Ime"

def racun():

	class Racun():
		def __init__(self,racun):
			self.racun = racun
		def __str__(self) -> 'str':
			return f"RACUN!"
	class Racundzija():
		def __init__(self,racun):
			self.racun=racun		
		def racun(self,racun:'Racun') -> 'Racun':
			return racun
		def __str__(self) -> 'str':
			return f"Racun = {racun.racun}"	
	racun = Racun("neki racun")
	racundzija = Racundzija(racun)
	print(racundzija)

# generalno()
# TV()
# osobe()
# meta()
racun()