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

def test_first_digit(N):
	def test_first_digit_action(L):
		if int(L[0]) == N:
			return True
		else:
			raise ValueError(f"Prva znamenka mora biti {N}.")
	return test_first_digit_action

def test_sum_digits(N):
	def test_sum_digits_action(L):
		if sum([int(x) for x in L]) == N:
			return True
		else:
			raise ValueError(f"Suma znamenki mora biti {N}.")
	return test_sum_digits_action

def argtest(input_tests):
	def onDecorator(func):
		if not __debug__:
			return func
		else:
			def onCall(*pargs):
				for parg in pargs:
					for test in input_tests:
						if not test(parg):
							raise
				return func(*pargs)
			return onCall
	return onDecorator

def input_tests(tests):
	@argtest(tests)
	def input_sequence(v):	
		print("Svi testovi uspješni.")
		# napravi nešto dalje s unosom npr. spremi
		# za potrebe testiranja samo printa i vraća
		print(f"TEST PRINT: {v}")
		return v
	return input_sequence
	
def main():
	naziv = "synthetic"
	format = "####"
	print(f"{naziv} EVALUATOR")
	print('- '*7)

	new_input = True
	while new_input:
		v = input(f"Unesi {naziv} [{format}]: ")	# L = 1022
		try:
			t = [test_len(4),test_num,test_first_digit(1),test_sum_digits(5)]
			L = input_tests(t)(v)
			# sve je prošlo OK, imamo unos u varijabli, dalje po želji
		except ValueError as VE:
			print(VE)
		
		new_input_test=False
		while new_input_test==False:
			new_input_test = input("\nNovi unos? [Y/N] ")
			if not new_input_test.upper() in ['Y','N']:
				print("Pogrešan unos!")
				new_input_test=False
			else:
				new_input = True if new_input_test.upper()=='Y' else False
				new_input_test=True
	
main()