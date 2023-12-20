import itertools as it
import numpy as np

multiplier = 8

def print_ocjene(ocjene):
	print("\n> ISPIS OCJENA:")
	print("- "*multiplier)
	[print(f"{i+1}. ocjena: {x}") for i,x in enumerate(ocjene)]

	print("\n> BROJ OCJENA COUNT:")
	print("- "*multiplier)
	[print(f"({i+1}) broj ocjena: {x}") for i,x in enumerate(broj_ocjena_count(ocjene))]

	print("\n> BROJ OCJENA ITER:")
	print("- "*multiplier)
	[print(f"({i+1}) broj ocjena: {x}") for i,x in enumerate(broj_ocjena_iter(ocjene))]

	print("\n> BROJ OCJENA NUMPY:")
	print("- "*multiplier)
	[print(f"({i+1}) broj ocjena: {x}") for i,x in enumerate(broj_ocjena_numpy(ocjene))]
	
	print("\n> PROSJEK OCJENA:")
	print("- "*multiplier)
	print(f"{sum(ocjene)/len(ocjene):.2f}")

def assign_ocjene(msg,chk):
	try:
		value = int(input(msg))
	except ValueError:
		print("Greska pri unosu!")
		value = False
	if not value in chk:
		print("Ocjena mora biti 1-5!")
		value = False
	return value

def broj_ocjena_count(ocjene):
	hist = []
	for i in range(5):
		hist.append(ocjene.count(i+1))
	return hist

def broj_ocjena_iter(ocjene):
	hist = [0]*5
	for k,g in it.groupby(sorted(ocjene)):
		hist[k-1]=len(list(g))
	return hist

def broj_ocjena_numpy(ocjene):
	x,b = np.histogram(ocjene,bins=[1,2,3,4,5])
	for v,n in it.zip_longest(b,x,fillvalue=0):
		yield n	# može se iskoristiti i v pa ne treba enumerate

def main_ocjene():
	num = 6
	chk = [x for x in range(1,6)]
	ocjene = []

	print("\n> UNOS OCJENA:")
	print("- "*multiplier)

	for x in range(num):
		input_flag = False
		while not input_flag:
			value = assign_ocjene(f"> unesi {x+1}. ocjenu:",chk)
			if value:
				input_flag = True
		ocjene.append(value)

	print_ocjene(ocjene)

main_ocjene()