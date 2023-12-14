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

def konverzije_IP(IPadresa,tip):
	sum=""
	for i in IPadresa.split("."):
		sum+=f"{int(i):{tip}}"+"."
	print(f"[{sum[:-1].upper()}]")

def test_IP():
	IP = "192.168.0.1"
	print(IP)
	konverzije_IP(IP,'x')
	konverzije_IP(IP,'b')

test_IP()