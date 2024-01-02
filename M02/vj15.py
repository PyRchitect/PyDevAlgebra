def modulo_test(x,t): return True if not x%t else False

def main():
	l_min = 1
	l_max = 30
	# print(f"> test list: {list(range(l_min,l_max+1))}")
	D = {3:[],6:[],9:[]}

	for x in range(l_min,l_max+1):
		if modulo_test(x,3):
			D[3].append(x)
			if modulo_test(x,2): D[6].append(x)
			if modulo_test(int(x/3),3): D[9].append(x)
	
	for k in D:	print(f"> dijeljivi s {k}: {D[k]}")

# main()

def main_test():
	x = 6
	if x in range(1,6):
		print('da')
	else:
		print('ne')

main_test()