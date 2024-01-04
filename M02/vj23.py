x=''
l=[]

def broj_ocjena_count(ocjene):
	return [ocjene.count(i+1) for i in range(5)]

while x.upper() not in ['E','X']:
	print("\nMENI")
	print("> u/U - unos u listu")
	print("> i/I - ispis analize")
	print("> c/C - brisanje liste")
	print("> x/X, e/E - izlaz")
	# ostalo - krivi unos i zavrtiti iznova
	x = input("\nUnesi opciju: ")

	if x.upper() == 'U':
		try:
			n = int(input("Unos:"))
		except:
			print("Unos mora biti broj.")
		else:
			if n not in range(1,5+1):
				print("Unesi ocjenu od 1 do 5.")
			else:
				l.append(n)
	elif x.upper() == 'I':
		if l:
			print(f"Ispis: {l}")
			print(f"> min: {min(l)}")
			print(f"> avg: {sum(l)/len(l):.2f}")
			print(f"> max: {max(l)}")
			print(f"> len: {len(l)}")
			print("> histogram:")
			[print(f"> > {i+1}: {x}") for i,x in enumerate(broj_ocjena_count(l))]
		else:
			print("Lista prazna.")
	elif x.upper() == 'C':
		l.clear()
		print(f"Brisanje.")
	elif x.upper() in ['E','X']:
		print("Izlaz.")
	else:
		print("Krivi unos opcije.")