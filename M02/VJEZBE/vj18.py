# svi primbrojevi u rasponu 1:100
import math

def eratosten(x):
	u_bound = int(math.sqrt(x)+1)
	for n in range(2,u_bound):
		if not x%n:
			return False
	return True

def main():
	l_min = 1
	l_max = 100
	P=[]
	for x in range(2,l_max):
		if eratosten(x):
			P.append(x)
	print(P)
		
main()