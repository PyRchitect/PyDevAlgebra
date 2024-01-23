import random as rn

def div_maker(N):
	def div_action(x):
		return True if x%N==0 else False
	return div_action

def main():
	lb = 1
	ub = 100
	ln = 10
	L = rn.choices(range(lb,ub),k=ln)

	def djeljivost(d):
		div_test = div_maker(d)
		print(f"\nDjeljivost s {d}:")
		[print(f"{x} {'je' if div_test(x) else 'nije'} djeljiv s {d}") for x in L]
	
	d_list = [2,4,5,7]
	[djeljivost(x) for x in d_list]

main()