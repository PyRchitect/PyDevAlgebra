def main():
	if int(input("\nINICIJALIZACIJA? [0:NE, 1:DA] ")):
		d = {}	# osnovna struktura podataka
		i = 0	# brojač za naslove rubrika
		b = []	# brojač predmeta po rubrikama
		r_flag = True		# da li nova rubrika? da/ne
		while r_flag:		# dok korisnik traži novu rubriku
			i+=1			# povećaj brojač rubrika za 1
			print(f"\n{i}. RUBRIKA:")
			r = input("> Unesi naziv rubrike [format:naziv]: ")
			t = float(input("> Unesi težinski udio [format:0.##]: "))
			j = 0			# brojač za naslove predmeta
			n = []			# lista naziva predmeta
			g = []			# lista ocjena predmeta
			print("> Unos predmeta:")
			p_flag = True	# da li novi predmet? da/ne
			while p_flag:	# dok korisnik traži novi predmet
				j+=1		# povećaj brojač predmeta za 1
				print(f"> {j}. PREDMET:")
				n.append(input("> > Unesi naziv predmeta [format:naziv]: "))
				g.append(int(input("> > Unesi ocjenu predmeta [format:1-5]: ")))
				p_flag = int(input("> > Novi predmet ? [0:NE, 1:DA] "))
			b.append(j)		# dodaj broj predmeta za tu rubriku
			d[r] = [t,{x:y for (x,y) in zip(n,g)}]	# dodaj u strukturu
			r_flag = int(input("\n> Nova rubrika ? [0:NE, 1:DA] "))
	else:
		d = {
			'a': [0.3, {'mat': 5, 'hrv': 4}],
			'b': [0.2, {'eng': 5, 'lat': 5}],
			'c': [0.2, {'bio': 4, 'kem': 3, 'fiz': 5}],
			'd': [0.2, {'geo': 4, 'pov': 3}],
			'e': [0.1, {'gla': 5, 'lik': 4, 'tzk': 5}]
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
		print("> PREDMETI:")
		for (x,y) in v[1].items():			# ispiši predmete za rubriku
			print(f"> > {x}: {y}")			# format naziv: ocjena

	print("\nPROSJECI:")
	print(f"> obični prosjek: {sum(h)/sum(b):.2f}")	# zbroji prosjeke/broj rubrika
	print(f"> težinski prosjek: {sum([(x/y)*z for (x,y,z) in zip(h,b,t)]):.2f}")

main()

# OSNOVNA STRUKTURA:
# svjedodžba(dict) =
# {
#	naziv1(str):[	težina(float),
#					predmeti(dict): {	ime1(str): ocjena(int),
#										ime2(str): ocjena(int),
#										ime3(str): ocjena(int),
#										...
#									}
#				],
#	naziv2(str):[	težina(float),
#					predmeti(dict): {	ime4(str): ocjena(int),
#										ime5(str): ocjena(int),
#										ime6(str): ocjena(int),
#										...
#									}
#				],
#	...
# }

# TO DO :: ERROR HANDLING
# > provjera krivih unosa
# > ne smije prazno polje
# > tezine float 0<=t<=1, u zbroju = 1
# > ocjene int 1<=g<=5
# > predmeti bi trebali biti različiti
# TO DO :: SCALING
# > bolje init za sve pa ocjene po učeniku
# > unos ostalih podataka za učenika