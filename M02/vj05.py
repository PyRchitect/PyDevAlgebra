def konverzije_brojeva():
	sbr1 = '17'
	sbr2 = '5'

	szbr = sbr1 + sbr2
	print(szbr)
	print()

	br1 = int(sbr1)
	br2 = int(sbr2)

	zbr = br1 + br2
	print(zbr)
	print()

	br1 = float(sbr1)
	br2 = float(sbr2)

	zbr = br1 + br2
	print(zbr)
	print("Zbroj je " + str(zbr))
	print()

	strue = 'True'
	sfalse = 'False'

	btrue = bool(strue)
	bfalse = bool(sfalse)

	print(type(br1))
	print(type(br2))

	print(type(sbr1))
	print(type(sbr2))

	print(type(strue))
	print(type(sfalse))

	print(btrue)
	print(bfalse)

	print(type(btrue))
	print(type(bfalse))

	rTrue = "whatever"
	rfalse = ""

	print(bool(rTrue))
	print(bool(rfalse))

	print(type(rTrue))
	print(type(rfalse))

	asciibroj = 65
	asciiznak = chr(asciibroj)
	print(asciibroj,asciiznak)
	asciibrojizznaka = ord(asciiznak)
	print(asciiznak,asciibrojizznaka)

	dbr = 17

	bbr = bin(dbr)
	print(dbr,bbr)
	print(type(bbr))
	print(f"{dbr:b}")

	obr = oct(dbr)
	print(dbr,obr)
	print(type(obr))
	print(f"{dbr:o}")

	hbr = hex(dbr)
	print(dbr,hbr)
	print(type(hbr))
	print(f"{dbr:x}")

def konverzije_IP(IPadresa,padding,tip):
	return ".".join([f"{int(i):0>{padding}{tip}}" for i in IPadresa.split(".")])

def konverzije_IP_backup(IPadresa,padding,tip):
	sum=""
	for i in IPadresa.split("."):
		sum+=f"{int(i):0>{padding}{tip}}"+"."
	return sum[:-1].upper()

def test_IP():
	IP = "192.168.0.1"	# za testiranje
	print("\n> IP konverzija - test:")
	print(f"dec: {IP}")
	print(f"hex: {konverzije_IP(IP,2,'x')}")
	print(f"bin: {konverzije_IP(IP,8,'b')}")

# ulaz je int broj (type je int) od 0 do 15 - 15 -> 1111 0 -> 0000
# pretvaramo u binarni ALI type ostaje int !!!
# MI cemo napisati program koji ce napraviti tu konverziju

def konverzije_baza(broj,baza):
	digits = []
	while broj > 0:
		digits.append(broj%baza)
		broj = broj//baza
	digits.reverse()
	return digits

def test_baze():
	broj = 8 # za testiranje
	baza = 2 # za testiranje
	print("\n> konverzija baza - test:")
	print(f"dec: {broj}")
	print(f"baza {baza}: {konverzije_baza(broj,baza)}")

test_IP()
test_baze()