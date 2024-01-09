import arg_testing as at

def test_DMY(L):
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

def main():
	naziv = "DoB"
	format = "DDMMYYYY"
	print(f"{naziv} EVALUATOR")
	print('- '*7)

	new_input = True
	while new_input:
		v = input(f"Unesi {naziv} [{format}]: ")	# L = 01012020
		try:
			t = [test_len(8),test_num,test_DMY]
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