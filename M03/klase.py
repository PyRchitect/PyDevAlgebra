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

	for x in lista_cekanja:
		print(x)

	# print()
	# x = Osoba()
	# print(Osoba.__dict__)	
	# print(x.__dict__)
	# print()
	# x.__dict__.update({'tezina':80})
	# print(Osoba.__dict__)
	# print(x.__dict__)
	# print()
	Osoba.__dict__['ziv']=1
	#print(Osoba.__dict__)
	#print(x.__dict__)


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

def auto():

	class Automobil():

		MOTOR = {
			0: 'ugasen',
			1: 'upaljen'}

		ZMIGAVCI = {
			0: 'nijedan',
			1: 'lijevi',
			2: 'desni',
			3: 'sva 4'}
		
		BRZINE = {
			-2: 'P',
			-1: 'R',
			-0: 'N',
			1: 'prva',
			2: 'druga',
			3: 'treca',
			4: 'cetvrta',
			5: 'peta',
			6: 'sesta'}

		def __init__(self,
			   marka=None,
			   model=None,
			   snaga=None,
			   vrsta_goriva=None,
			   mjenjac_brzina=None):
			
			self.marka = marka
			self.model = model
			self.snaga = snaga
			self.vrsta_goriva = vrsta_goriva
			self.mjenjac_brzina = mjenjac_brzina			

			self.stanje_motor = 0
			self.stanje_zmigavac = 0
			self.stanje_brzine = 0
		
		def __promijeni_stanje_motora(self,stanje):
			self.stanje_motor = Automobil.MOTOR[stanje]
		
		def upali_motor(self):
			self.__promijeni_stanje_motora(self,0)
		
		def ugasi_motor(self):
			self.__promijeni_stanje_motora(self,1)
		
		def __promijeni_stanje_zmigavca(self,stanje):
			self.stanje_zmigavac = Automobil.ZMIGAVCI[stanje]
		
		def upali_lijevi_zmigavac(self):
			self.__promijeni_stanje_zmigavca(self,1)
		
		def upali_desni_zmigavac(self):
			self.__promijeni_stanje_zmigavca(self,2)
		
		def upali_sva_cetiri_zmigavca(self):
			self.__promijeni_stanje_zmigavca(self,3)
		
		def ugasi_zmigavce(self):
			self.__promijeni_stanje_zmigavca(self,0)
		
		def __promijeni_stanje_brzine(self,stanje):
			self.stanje_brzine = Automobil.BRZINE[stanje]
		
		def smanji_brzinu(self):
			if self.stanje_brzine>0:
				self.__promijeni_stanje_brzine(self,self.stanje_brzine-1)
		
		def povecaj_brzinu(self):
			if self.stanje_brzine>0:
				self.__promijeni_stanje_brzine(self,self.stanje_brzine+1)
		
		def ubaci_u_ler(self):
			self.__promijeni_stanje_brzine(self,0)
		
		def ubaci_u_rikverc(self):
			self.__promijeni_stanje_brzine(self,-1)
		
		def ubaci_u_park(self):
			self.__promijeni_stanje_brzine(self,-2)

# generalno()
# TV()
osobe()
# meta()