# unos u:
# C - Celzijus
# F - Farenheit
# K - Kelvin

def KC(temp,type='K'):
	if type.upper() == 'K':
		return (temp - 273.15,'C')
	elif type.upper() == 'C':
		return (temp + 273.15,'K')
	else:
		raise ValueError

def CF(temp,type='C'):
	if type.upper() == 'C':
		return (temp*1.8 + 32,'F')
	elif type.upper() == 'F':
		return (temp/1.8 - 32,'C')
	else:
		raise ValueError

def FK(temp,type='F'):
	if type.upper() == 'F':
		return KC(CF(temp,type='F')[0],type='C')
	elif type.upper() == 'K':
		return CF(KC(temp,type='K')[0],type='C')
	else:
		raise ValueError

def main():
	funkcije = {'F':[CF,FK],'C':[KC,CF],'K':[KC,FK]}
	new_input = True
	while new_input:
		data = input("Unesi temperaturu [#.##] [C|F|K]: ").split(' ')
		
		#l = funkcije[data[1]]
		for f in funkcije[data[1]]:
			r = f(float(data[0]),data[1])
			print(f"> temperatura [{r[1]}]: {r[0]:.2f}")
		
		input_test = False
		while not input_test:		
			input_test = input("Ponovo? [Y/N] ")
			if not input_test in ["y","Y","n","N"]:
				print("Pogresan unos!")
			else:
				input_test=True		
		if input_test in ["n","N"]:
			new_input = False

main()