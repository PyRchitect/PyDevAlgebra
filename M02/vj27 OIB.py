def check(L):
	r=[10]
	for i,l in enumerate(L[:-1]):
		r.append((((l+r[i])%10 or 10)*2)%11)
		# print(f"test: {r[-1]}")
	return (11-r[-1] if r[-1]!=1 else 0) == L[-1]

def input_basic(v):
	if len(v)!=11:
		raise ValueError("OIB mora imati 11 znamenki.")
	try:
		return [int(x) for x in v]
	except:
		raise ValueError("Simboli moraju biti znamenke 0-9")
	
def main():
	print("OIB EVALUATOR")
	print('- '*11)
	new_input = True
	while new_input:
		v=input("Unesi OIB: ")	# L = 69435151530
		try:
			L = input_basic(v)
			print(f"OIB{' nije' if not check(L) else ''} validan.")
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