def varijanta_1():
	broj = 1
	while broj != 0:
		unos = int(input("Unesi broj: "))
		broj = unos
	print('ovo ne zelim ispisati')

def varijanta_2():
	while True:
		unos = int(input("Unesi broj: "))
		if unos == 0:
			break
		print("Ispisujemo dok je razlicito od nule")

# varijanta_1()
# varijanta_2()