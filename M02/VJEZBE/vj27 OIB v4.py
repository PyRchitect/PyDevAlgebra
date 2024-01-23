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

def test_norma(L):
	if calc_norma(L) == int(L[-1]):
		return True
	else:
		raise ValueError("OIB nije validan.")

def calc_OIB():
	r = rn.choices(range(1,10),k=10)
	k = str(calc_norma(r+['0']))
	# +['0'] je samo testna jer norma računa do L[-1] pa da je pun broj
	# zato što se u originalnu listu puni samo prvih 10 znamenki broja
	# dolje se testna 0 zamjenjuje izračunatom kontrolnom znamenkom k
	return ''.join([str(x) for x in r+[k]])

def main():
	naziv = "OIB"
	format = "#"*11
	print(f"{naziv} EVALUATOR")
	print('- '*7)

	new_input = True
	while new_input:
		print("[0] - generiraj")
		print("[1] - provjeri")
		
		odabir_test = False
		while odabir_test == False:
			try:
				odabir = int(input("Odabir [0/1] "))
				assert odabir in [0,1]
				odabir_test = True
			except:
				print("Pogrešan unos!")
				odabir_test = False

		if odabir == 0:
			print(f"\nGenerirani OIB: {calc_OIB()}")
		else:			
			v = input(f"\nUnesi {naziv} [{format}]: ")	# primjer: 69435151530
			try:
				t = [test_len(11),test_num,test_norma]
				L = at.input_tests(t)(v)
				# sve je prošlo OK, imamo unos u varijabli, dalje po želji
			except ValueError as VE:
				print(VE)
		
		new_input_test=False
		while new_input_test==False:
			try:
				new_input_test = input("\nNovi unos? [Y/N] ")
				assert new_input_test.upper() in ['Y','N']
			except:				
				print("Pogrešan unos!")
				new_input_test=False				
	
		new_input = True if new_input_test.upper()=='Y' else False

main()