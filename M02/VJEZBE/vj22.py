x=''
input_value=''

while x.upper() not in ['E','X']:
	print("\nMENI")
	print("> u/U - unos")
	print("> i/I - ispis")
	print("> x/X ili e/E- izlaz")
	# ostalo - krivi unos i zavrtiti iznova
	x = input("Unesi opciju:")

	if x.upper() == 'U':
		input_value = input("Unos:")
	elif x.upper() == 'I':
		print(f"Ispis: {input_value}")
	elif x.upper() in ['E','X']:
		print("Izlaz.")
	else:
		print("Krivi unos.")