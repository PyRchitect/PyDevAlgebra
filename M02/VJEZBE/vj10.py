def polujeftini_enumerate_y(L):
	i=0
	for x in L:
		yield (i,x)
		i+=1

def polujeftini_enumerate_r(L):
	s = []
	i=0
	for x in L:
		s.append((i,x))
		i+=1
	return s

def yield_return_test():

	test = 'Ratar'
	print("\ntest return:")
	for (i,x) in polujeftini_enumerate_r(test):
		print(f"index: {i} oznaka:{x}")

	print("\ntest yield:")
	for (i,x) in polujeftini_enumerate_y(test):
		print(f"index: {i} oznaka:{x}")

# yield_return_test()

def test():		
	A = [1,2,3]
	B = A[:]
	print(A)
	print(B)
	print(B==A)
	print(B is A)

test()