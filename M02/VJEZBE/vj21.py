def while_continue():

	broj = 1
	while broj < 6:
		if broj == 4:
			broj += 1
			continue
		print(broj)
		broj += 1
	print()

def while_combined():
	broj = 0
	while broj < 5:
		broj += 1
		if broj == 4:
			continue
		print(broj)

def broj_iter_1():

	b = list(range(6))
	b_iter = b.__iter__()

	b0 = b_iter.__next__()
	print(b0)
	b1 = b_iter.__next__()
	print(b1)
	b2 = b_iter.__next__()
	print(b2)
	b3 = b_iter.__next__()
	print(b3)
	b4 = b_iter.__next__()
	print(b4)
	b5 = b_iter.__next__()
	print(b5)
	b6 = b_iter.__next__()
	print(b6)

def broj_iter_2():	

	b = list(range(6))
	b_iter = b.__iter__()

	b0 = next(b_iter)
	print(b0)
	b1 = next(b_iter)
	print(b1)
	b2 = next(b_iter)
	print(b2)
	b3 = next(b_iter)
	print(b3)
	b4 = next(b_iter)
	print(b4)
	b5 = next(b_iter)
	print(b5)
	b6 = next(b_iter)
	print(b6)

def parni_brojevi(start,end):
	ulaz = start
	while True:
		ulaz+=1
		if ulaz%2==0:
			continue
		if ulaz == end:
			break
		print(ulaz)

parni_brojevi(3,13)