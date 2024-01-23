def check(L):
	r=[10]
	for i,l in enumerate(L[:-1]):
		r.append((((l+r[i])%10 or 10)*2)%11)
	return (11-r[-1] if r[-1]!=1 else 0) == L[-1]
	
def main():
	v = input("\nUnesi OIB: ")	# primjer: 69435151530

	if len(v) != 11:
		raise ValueError("OIB mora imati 11 znamenki.")

	if not v.isnumeric():
		raise ValueError("Simboli moraju biti znamenke 0-9")

	print(f"OIB{' nije' if not check([int(x) for x in v]) else ''} validan.")

main()