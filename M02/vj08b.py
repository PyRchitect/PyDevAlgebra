def main():
	if int(input("\nINICIJALIZACIJA? [0:NE, 1:DA] ")):
		d = {}	# osnovna struktura podataka
		i = 0	# brojač za naslove rubrika
		b = []	# brojač zadataka po rubrikama
		r_flag = True		# da li nova rubrika? da/ne
		while r_flag:		# dok korisnik traži novu rubriku
			i+=1			# povećaj brojač rubrika za 1
			print(f"\n{i}. RUBRIKA:")
			r = input("> Unesi naziv rubrike [format:naziv]: ")
			t = float(input("> Unesi težinski udio [format:0.##]: "))
			j = 0			# brojač za naslove zadataka
			n = []			# lista naziva zadataka
			g = []			# lista ocjena zadataka
			print("> Unos vrste zadatka:")
			p_flag = True	# da li novi zadatak? da/ne
			while p_flag:	# dok korisnik traži novi zadatak
				j+=1		# povećaj brojač zadataka za 1
				print(f"> {j}. ZADATAK:")
				n.append(input("> > Unesi naziv zadatka [format:naziv]: "))
				g.append(int(input("> > Unesi ocjenu zadatka [format:1-5]: ")))
				p_flag = int(input("> > Novi zadatak ? [0:NE, 1:DA] "))
			b.append(j)		# dodaj broj zadataka za tu rubriku
			d[r] = [t,{x:y for (x,y) in zip(n,g)}]	# dodaj u strukturu
			r_flag = int(input("\n> Nova rubrika ? [0:NE, 1:DA] "))
	else:
		d = {
			'a': [0.3, {'kontrolni': 5, 'ispitivanje': 5}],
			'b': [0.2, {'seminar': 5, 'zavrsni': 5}],
			'c': [0.2, {'domaci': 3, 'vjezbe': 3, 'lab': 2}],
			'd': [0.2, {'dolasci': 2, 'javljanje': 2, 'nesto':3}],
			'e': [0.1, {'zalaganje': 1, 'interes': 1, 'pomoc': 2}]
			}
		b = [len(v[1]) for v in d.values()]

	# izračun prosjeka
	h = []	# prosjek ocjena po rubrikama
	t = []	# helper: težine po rubrikama
	for i,v in enumerate(d.values()):
		s = 0	# zbrajač ocjena za rubriku
		for x in v[1].values():
			s += x			# zbroji ocjenu iz rubrike
		h.append(s)			# dodaj sumu ocjena za rubriku
		t.append(v[0])		# dodaj težinu za rubriku za kasnije
	
	print("\nISPIS REZULTATA")
	for i,(r,v) in enumerate(d.items()):
		print(f"\nRUBRIKA {r}: {100*v[0]:.2f}%")	# rubrika: težina%
		print(f"> prosjek: {h[i]/b[i]:.2f}")		# prosjek za rubriku
		print("> ZADACI:")
		for (x,y) in v[1].items():			# ispiši zadatke za rubriku
			print(f"> > {x}: {y}")			# format naziv: ocjena

	print("\nPROSJECI:")
	print(f"> obični prosjek: {sum(h)/sum(b):.2f}")	# zbroji prosjeke/broj rubrika
	print(f"> težinski prosjek: {sum([(x/y)*z for (x,y,z) in zip(h,b,t)]):.2f}")

main()

# OSNOVNA STRUKTURA:
# svjedodžba(dict) =
# {
#	naziv1(str):[	težina(float),
#					zadaci(dict):	{	tip1(str): ocjena(int),
#										tip2(str): ocjena(int),
#										tip3(str): ocjena(int),
#										...
#									}
#				],
#	naziv2(str):[	težina(float),
#					zadaci(dict):	{	tip4(str): ocjena(int),
#										tip5(str): ocjena(int),
#										tip6(str): ocjena(int),
#										...
#									}
#				],
#	...
# }

# TO DO :: ERROR HANDLING