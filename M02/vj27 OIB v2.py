def test_norma(L):
	L = [int(x) for x in L]
	r=[10]
	for i,l in enumerate(L[:-1]):
		r.append((((l+r[i])%10 or 10)*2)%11)
		# print(f"test: {r[-1]}")
	if (11-r[-1] if r[-1]!=1 else 0) == L[-1]:
		return True
	else:
		raise ValueError("OIB nije validan.")

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

def argtest(*input_tests):
	def onDecorator(func):
		if not __debug__:
			return func
		else:
			def onCall(*pargs):
				for test in input_tests:
					if not test(pargs[0]):
						raise
				return func(*pargs)
			return onCall
	return onDecorator

@argtest([test_len(11),test_num,test_norma])
def input_sequence(v):
	print("Svi testovi uspješni.")
	return v
	
def main():
	naziv = "OIB"
	print(f"{naziv} EVALUATOR")
	print('- '*11)

	new_input = True
	while new_input:
		v = input(f"Unesi {naziv}: ")	# L = 69435151530
		try:
			L = input_sequence(v)
			print(L)
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