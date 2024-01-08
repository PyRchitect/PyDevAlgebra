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