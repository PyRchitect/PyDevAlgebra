import random as rn
import arg_testing as at

def test_len(N):
	def test_len_action(L):
		if len(L)==N:
			return True
		else:
			raise ValueError(f"Unos mora imati {N} znamenki.")
	return test_len_action

def test_num(L):
	if L.isnumeric():
		return True
	else:
		raise ValueError("Simboli moraju biti znamenke 0-9")

def calc_norma(L):
	L = [int(x) for x in L]
	r=[10]
	for i,l in enumerate(L[:-1]):
		r.append((((l+r[i])%10 or 10)*2)%11)
		# print(f"test: {r[-1]}")
	return (11-r[-1] if r[-1]!=1 else 0)

def OIB_test_norma(L):
	if calc_norma(L) == int(L[-1]):
		return True
	else:
		raise ValueError("nije validan.")

def calc_OIB():
	r = rn.choices(range(1,10),k=10)
	k = str(calc_norma(r+['0']))
	# +['0'] je samo testna jer norma računa do L[-1] pa da je pun broj
	# zato što se u originalnu listu puni samo prvih 10 znamenki broja
	# dolje se testna 0 zamjenjuje izračunatom kontrolnom znamenkom k
	return ''.join([str(x) for x in r+[k]])

def DOB_test_DMY(L):
	if int(L[:2]) not in range(1,32):
		raise ValueError("dan nije validan.")
	if int(L[2:4]) not in range(1,13):
		raise ValueError("mjesec nije validan.")
	if int(L[4:]) < 1900:
		raise ValueError("ma nisi rođen prije 1900.")
	if int(L[4:]) > 2024:
		raise ValueError("godina mora biti manja od trenutne.")
	if int(L[4:]) > 2006:
		raise ValueError("samo za starije od 18.")
	return True

def CI_test_first_digit(N):
	def CI_test_first_digit_action(L):
		if int(L[0])%N == 0:
			return True
		else:
			raise ValueError(f"Prva znamenka mora biti djeljiva s {N}.")
	return CI_test_first_digit_action

def CI_test_sum_digits(N):
	def test_sum_digits_action(L):
		if sum([int(x) for x in L]) == N:
			return True
		else:
			raise ValueError(f"Suma znamenki mora biti {N}.")
	return test_sum_digits_action

def main():
	naziv = ["OIB","DoB","ISKAZNICA"]
	format = ["#"*11,"DDMMYYYY","#"*4]
	testovi = []
	testovi.append([test_len(11),test_num,OIB_test_norma])
	testovi.append([test_len(8),test_num,DOB_test_DMY])
	testovi.append([test_len(4),test_num,CI_test_first_digit(2),CI_test_sum_digits(5)])
	print("FORMULAR EVALUATOR")
	print('- '*7)

	new_input = True
	while new_input:
		print("[0] - generiraj OIB")
		print("[1] - provjeri")
		
		odabir_test = False
		while odabir_test == False:
			try:
				odabir = int(input("Odabir [0/1] "))
				print("- "*7)
				assert odabir in [0,1]
				odabir_test = True
			except:
				print("Pogrešan unos!")
				odabir_test = False

		if odabir == 0:
			print(f"Generirani OIB: {calc_OIB()}")
		else:
			values = []
			for (n,f) in zip(naziv,format):
				values.append(input(f"Unesi {n} [{f}]: "))
			print("- "*7)
			for (n,t,v) in zip(naziv,testovi,values):
				print(f"{n}:",end=' ')
				try:
					L = at.input_tests(t)(v)
					# sve je prošlo OK, imamo unos u varijabli, dalje po želji
				except ValueError as VE:
					print(VE)
		
		new_input_test=False
		while new_input_test==False:
			try:
				print("- "*7)
				new_input_test = input("Novi unos? [Y/N] ")
				assert new_input_test.upper() in ['Y','N']
			except:				
				print("Pogrešan unos!")
				new_input_test=False				
	
		new_input = True if new_input_test.upper()=='Y' else False

main()