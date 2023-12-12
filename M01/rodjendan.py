import datetime as dt

class i:
    def __init__(self,naziv,adresa, tel, mail, preferenca=0):
        self.naziv = naziv
        self.adresa = adresa
        self.tel = tel
        self.mail = mail 
        self.preferenca = preferenca
    
    def posalji_upit(self,naslov,tekst):
        import smtplib

        sender = 'from@example.com'
        message = f"""From: {sender}
                    To: {self.mail}
                    Subject: {naslov}
                    {tekst}"""

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, self.mail, message)         
            print("Successfully sent email")
        except:
            pass

class l:
    def __init__(self,ime, tel, adresa):
        self.adresa = adresa
        self.ime = ime
        self.tel = tel

class p:
    def __init__(self,datum,termin,trajanje,lokacija,slavljenik):
        self.datum = datum
        self.termin = termin
        self.trajanje = trajanje
        self.lokacija = lokacija
        self.slavljenik = slavljenik
    
    def sastavi(self):
        # overloadati print za write to file
        # pretpostavka npr. PDF forma s praznim kucicama

        # pozivamo vas na proslavu rođendana ...
        print(f"SLAVLJENIK: {self.slavljenik}")
        # na dan ...
        print(f"DATUM: {self.datum}")
        print(f"TERMIN: {self.termin}")
        print(f"TERMIN: {self.trajanje}")
        print(f"LOKACIJA: {self.lokacija}")

    def dostavi(self,adresa):
        pass

def organizacija_rodjendana():

    slavljenik = input("> unesi slavljenika/cu: ")

    moguce_trajanje = list(range(1,4))

    print("> unesi željeno trajanje proslave:")
    while True:
        trajanje = int(input("> trajanje (1h/2h/3h): "))
        if trajanje in moguce_trajanje:
            break
        else:
            print("Greska!")

    print("> unesi u kojem rasponu datuma:")
    datum_od = input("> > od kojeg datuma: ")
    datum_do = input("> > do kojeg datuma: ")
    datum = date_between_two_dates(datum_od,datum_do)

    radno_vrijeme = list(range(8,16))
    termini = []
    print("> unesi željene termine (pretpostavka fiksno za svaki datum):")
    while True:
        termin = int(input("> dodaj termin (#h, 0 = izlaz): "))
        if termin in radno_vrijeme[:-trajanje]:
            termini.append(termin)
        elif termini == 0:
            break
        else:
            print("Greska!")

    igraonice = [i(...), i(...), ...]   # ili ucitati iz nekog popisa
    ljudi = [l(...), l(...), ...]       # ili ucitati iz nekog kalendara

    termin_odabrano = odredi_termin(datum,termini,trajanje)
    # pretpostavka uzmimo prvi raspoloživi termin (ili promijenit u preferirano):
    termin = termin_odabrano[0][0]

    lokacije = odredi_lokaciju(termin,igraonice)

    if len(lokacije)>1:
        uzmi_preferiranu(lokacije)
    else:
        lokacija = lokacije[0]

    pozivnica=sastavi_pozivnicu(datum, termin, lokacija, slavljenik)

    zovi_ljude(ljudi,pozivnica)

    # dogovori_tortu()

    odi_na_proslavu(datum, termin, lokacija)

def date_between_two_dates(datum_od,datum_do):
    current_date = datum_od

    while current_date <= datum_do:
        current_date.append(current_date)
        current_date += dt.timedelta(days=1)
    
    return current_date

def filter_vikend(datum_od,datum_do):

    for dan in date_between_two_dates(datum_od,datum_do):
        if dan.datetime.weekday()>=5:
            yield dan

def odredi_termin(datum_od,datum_do,trazeni_termini,trajanje=1):
    termini = trazeni_termini or [x for x in range(8,16-trajanje+1)]
    raspolozivi = [[],[]]

    for dan in filter_vikend(datum_od,datum_do):
        prvi_termin_flag = False
        for termin in termini(dan):
            if not zauzetost(dan,termin):
                # ako je prvi termin taj dan, dodaj datum u [0]
                if prvi_termin_flag == False:
                    raspolozivi[0].append(dan)
                    prvi_termin_flag = True
                # dodaj termin u [1]
                raspolozivi[1].append(termin)

    return raspolozivi                

def zauzetost(dan,termin):
    zauzet_da_ne = True
    # otvori kalendar, cross-referenciraj, ...
    return zauzet_da_ne

def odredi_lokaciju(datum,termin,igraonice):
    naslov = "Proslava dječjeg rođendana"

    termin_format = ""
    for datum in termin[0]: # pretraga po datumima
        termin_format += f"{datum}: | "
        for sat in termin[1]:
            termin_format += f"{sat} |"
        termin_format += f"\n"
   
    tekst = f"Poštovani, jeste li raspoloživi u slijedećim terminima?\n{termin_format}\nUnaprijed hvala, ..."
    raspolozivi = []
    for lok in igraonice:
        odgovor = lok.posalji_upit(naslov,tekst)
        # pretpostavimo API s automatskim odgovaranjem
        if odgovor: raspolozivi.append(lok)
    return raspolozivi

def uzmi_preferiranu(igraonice):

    preferirana = igraonice[0]

    for lok in igraonice:
        if lok.preferenca > preferirana.preferenca:
            preferirana = lok.preferenca    

    return preferirana

def sastavi_pozivnicu(datum,termin,lokacija,trajanje,slavljenik):
    pozivnica = p(datum,termin,lokacija,trajanje,slavljenik)

    return pozivnica.sastavi()

def zovi_ljude(ljudi,pozivnica):

    for x in ljudi:
        pozivnica.dostavi(x.adresa)

        # ... dostavi pozivnicu

def odi_na_proslavu(datum, termin, lokacija):
    pass


organizacija_rodjendana()