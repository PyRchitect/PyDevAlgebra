def H(n,s,a,d):

	if n>0:
		H(n-1,s,d,a)	# FLIP a,d
		print(f"{n} : {s} -> {d}")
		H(n-1,a,s,d)	# FLIP a,s

H(int(input("n : ")),'A','B','C')