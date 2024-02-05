class Osoba:
    def __init__(self, ime, oib, email, telefon, adresa):
        self.ime = ime
        self.oib = oib
        self.email = email
        self.telefon = telefon
        self.adresa = adresa

    def ispis(self):
        print()
        print(self.ime)
        print(self.oib)
        print(self.email)
        print(self.telefon)
        print(self.adresa)

class Djelatnik(Osoba):
    def __init__(self, ime, prezime, oib, email, telefon, adresa, radno_mjesto):
        super().__init__(ime, oib, email, telefon, adresa)
        self.prezime = prezime
        self.radno_mjesto = radno_mjesto

    def ispis(self):
        print()
        print(self.ime)
        print(self.prezime)
        print(self.oib)
        print(self.email)
        print(self.telefon)
        print(self.adresa)
        print(self.radno_mjesto)
        print()

class Kupac(Osoba):
    def __init__(self, naziv, oib, email, telefon, sjediste, djelatnost):
        super().__init__(naziv, oib, email, telefon, sjediste)
        self.djelatnost = djelatnost

    def ispis(self):
        super().ispis()
        print(self.djelatnost)
        print()

kupci = []
while True:
    naziv = input('Unesite naziv Kupca ')
    oib = input('Unesite oib Kupca ')
    email = input('Unesite email Kupca ')
    telefon = input('Unesite telefon Kupca ')
    sjediste = input('Unesite sjediste Kupca ')
    djelatnost = input('Unesite djelatnost Kupca ')

    kupci.append(Kupac(naziv, oib, email, telefon, sjediste, djelatnost))

    if input('Zelite li dodati novog Kupca u program? (d/n) ') != 'd':
        break

for kupac in kupci:
    kupac.ispis()
    
print()

djelatnici = []
while True:
    ime = input('Unesite ime Djelatnika ')
    prezime = input('Unesite prezime Djelatnika ')
    oib = input('Unesite oib Djelatnika ')
    email = input('Unesite email Djelatnika ')
    telefon = input('Unesite telefon Djelatnika ')
    adresa = input('Unesite adresu Djelatnika ')
    radno_mjesto = input('Unesite naziv radnog mjesta Djelatnika ')

    djelatnici.append(Djelatnik(ime, prezime, oib, email, telefon, adresa, radno_mjesto))

    if input('Zelite li dodati novog Djelatnika u program? (d/n) ') != 'd':
        break

for djelatnik in djelatnici:
    djelatnik.ispis()