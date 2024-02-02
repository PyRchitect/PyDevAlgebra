def auto():

	from enum import Enum

	class Motor():

		class STANJE(Enum):
			UGASEN = 0
			UPALJEN = 1

			@staticmethod
			def dopusteno():
				return [x.value for x in Motor.STANJE]

		def __init__(self,
			   volumen=None,
			   snaga=None,
			   tip=None,
			   stanje = STANJE.UGASEN):

			self.volumen = volumen
			self.snaga = snaga
			self.tip = tip

			self.stanje = stanje

		def __promijeni_stanje_motora(self,novo_stanje):
			if novo_stanje.value not in Motor.STANJE.dopusteno():
				raise ValueError("nepoznato stanje motora")
			self.stanje = Motor.STANJE(novo_stanje)

		def upali_motor(self):
			self.__promijeni_stanje_motora(Motor.STANJE.UPALJEN)

		def ugasi_motor(self):
			self.__promijeni_stanje_motora(Motor.STANJE.UGASEN)

		def __str__(self):
			return ("\nMOTOR - OPIS:" +
				f"\n> volumen: {self.volumen}" +
				f"\n> snaga: {self.snaga}" +
				f"\n> tip: {self.tip}")

		def status(self):
			return (f"MOTOR - STATUS: {self.stanje}")

	class Getriba():

		class TIPOVI(Enum):
			AUTOMATIC = 0
			MANUAL = 1

			@staticmethod
			def dopusteno():
				return [x.value for x in Getriba.TIPOVI]

		class STANJE(Enum):
			PARK = -2
			RIKVERC = -1
			NEUTRAL = 0
			PRVA = 1
			DRUGA = 2
			TRECA = 3
			CETVRTA = 4
			PETA = 5
			SESTA = 6

			@staticmethod
			def dopusteno():
				return [x.value for x in Getriba.STANJE]

		def __init__(self,
			   tip=None,
			   stanje=STANJE.PARK):

			if tip.value not in Getriba.TIPOVI.dopusteno():
				raise ValueError("nepoznat tip getribe")
			self.tip = tip

			self.__stanje = stanje

		def __promijeni_stanje_brzine(self,novo_stanje):
			if novo_stanje.value not in Getriba.STANJE.dopusteno():
				raise ValueError("nepostojeca brzina")
			self.__stanje = Getriba.STANJE(novo_stanje)

		def __b_min(self):
			return Getriba.STANJE.PRVA

		def __b_max(self):
			return Getriba.STANJE.SESTA
		
		def __auto_u_brzini(self):
			return self.__stanje.value in range(self.__b_min().value,self.__b_max().value)

		def ubaci_u_brzinu(self):
			if self.__auto_u_brzini():
				raise ValueError("auto je vec u brzini")
			self.__promijeni_stanje_brzine(Getriba.STANJE.PRVA)

		def smanji_brzinu(self):
			if self.__stanje == self.__b_min():
				raise ValueError("brzina vec najniza")
			elif not self.__auto_u_brzini():
				raise ValueError("auto nije u brzini")
			self.__promijeni_stanje_brzine(Getriba.STANJE(self.__stanje.value-1))

		def povecaj_brzinu(self):
			if self.__stanje == self.__b_max():
				raise ValueError("brzina vec najvisa")
			elif not self.__auto_u_brzini():
				raise ValueError("auto nije u brzini")
			self.__promijeni_stanje_brzine(Getriba.STANJE(self.__stanje.value+1))

		def ubaci_u_ler(self):
			self.__promijeni_stanje_brzine(Getriba.STANJE.NEUTRAL)

		def ubaci_u_rikverc(self):
			if self.__auto_u_brzini():
				raise ValueError("auto u brzini, prvo ubaci u ler")
			self.__promijeni_stanje_brzine(Getriba.STANJE.RIKVERC)

		def ubaci_u_park(self):
			if self.__auto_u_brzini():
				raise ValueError("auto u brzini, prvo ubaci u ler")
			self.__promijeni_stanje_brzine(Getriba.STANJE.PARK)

		def __str__(self):
			return ("\nGETRIBA - OPIS:" +
				f"\n> tip: {self.tip}")

		def status(self):
			return (f"GETRIBA - STATUS: {self.__stanje}")

	class Zmigavci():

		class STANJE(Enum):
			NIJEDAN = 0
			LIJEVI = 1
			DESNI = 2
			SVA_CETIRI = 3

			@staticmethod
			def dopusteno():
				return [x.value for x in Zmigavci.STANJE]

		def __init__(self,
			   stanje = STANJE.NIJEDAN):

			self.__stanje = stanje

		def __promijeni_stanje_zmigavca(self,novo_stanje):
			if novo_stanje.value not in Zmigavci.STANJE.dopusteno():
				raise ValueError("nepoznato stanje zmigavaca")
			self.__stanje = Zmigavci.STANJE(novo_stanje)

		def upali_lijevi_zmigavac(self):
			self.__promijeni_stanje_zmigavca(Zmigavci.STANJE.LIJEVI)

		def upali_desni_zmigavac(self):
			self.__promijeni_stanje_zmigavca(Zmigavci.STANJE.DESNI)

		def upali_sva_cetiri_zmigavca(self):
			self.__promijeni_stanje_zmigavca(Zmigavci.STANJE.SVA_CETIRI)

		def ugasi_zmigavce(self):
			self.__promijeni_stanje_zmigavca(Zmigavci.STANJE.NIJEDAN)

		def __str__(self):
			return ("\nZMIGAVCI - OPIS:" +
				f"\n> nema parametara")

		def status(self):
			return (f"ZMIGAVCI - STATUS: {self.__stanje}")

	class Automobil():

		def __init__(self,
			   marka=None,
			   model=None,
			   m_volumen=None,
			   m_tip=None,
			   m_snaga=None,
			   g_tip=None):

			self.marka = marka
			self.model = model

			self.motor = Motor(m_volumen,m_snaga,m_tip)
			self.getriba = Getriba(g_tip)
			self.zmigavci = Zmigavci()

		def __str__(self):
			return ("\nOPIS:" +
				f"\n> marka: {self.marka}" +
				f"\n> model: {self.model}" +
				f"{self.motor}" +
				f"{self.getriba}")

		def status(self):
			return ("\nSTATUS:" +
				f"\n> motor: {self.motor.status()}" +
				f"\n> getriba: {self.getriba.status()}" +
				f"\n> zmigavci: {self.zmigavci.status()}")

	auto = Automobil('Audi','A6','2.0','TDI','195 KS',Getriba.TIPOVI.AUTOMATIC)

	print(auto)

	print(auto.status())

	auto.motor.upali_motor()
	auto.getriba.ubaci_u_brzinu()
	auto.getriba.povecaj_brzinu()
	auto.zmigavci.upali_desni_zmigavac()

	print(auto.status())

	auto.zmigavci.ugasi_zmigavce()
	auto.getriba.povecaj_brzinu()
	auto.getriba.smanji_brzinu()
	auto.getriba.povecaj_brzinu()

	print(auto.status())

	auto.zmigavci.upali_lijevi_zmigavac()
	auto.zmigavci.ugasi_zmigavce()
	auto.getriba.ubaci_u_ler()
	auto.getriba.ubaci_u_rikverc()

	print(auto.status())

	auto.getriba.ubaci_u_park()
	auto.motor.ugasi_motor()
	auto.zmigavci.upali_sva_cetiri_zmigavca()
	auto.zmigavci.ugasi_zmigavce()

	print(auto.status())

if __name__ == '__main__':
	auto()