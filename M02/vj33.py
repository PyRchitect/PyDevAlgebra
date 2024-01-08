lista = [0,1,2]

def promjeniNaIndexu(broj):
	zamjena = 5
	if len(lista)>=broj+1:
		lista[broj]=zamjena

def dodajUListu(broj):
	lista.append(broj)

print(lista)
promjeniNaIndexu(1)
print(lista)
dodajUListu(6)
print(lista)