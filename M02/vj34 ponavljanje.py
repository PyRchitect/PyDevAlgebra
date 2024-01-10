import random as rn
import datetime as dt

def lotto_generator(size,max_num):
	for x in rn.sample(range(1,max_num+1),k=size):
		yield x

def lotto_play(size,max_num,dopunski=True):
	print(f"LOTTO {size}/{max_num}")

	L=[]
	for i,b in enumerate(lotto_generator(size+1,max_num)): # +1 dopunski
		if i==0:
			print(f"Prvi broj je ... {b}")
		elif i<size:
			print(f"Slijedeci broj je ... {b}")
		elif i==size and dopunski:			
			print(f"I dopunski broj je ... {b}")
		L.append(b)

	print(f"\nRezultati kola {dt.date.today().strftime('%d.%m.%Y.')}")
	print(f"Izvučeni brojevi: {sorted(L[:-1])}")
	if dopunski:
		print(f"Dopunski broj je: {L[-1]}")
	print("- "*7)

def main():
	print("LOTTO BONANZA")
	print('- '*7)

	while True:
		print("[0] - izlaz")
		print("[1] - 7/39")
		print("[2] - 6/45")
		print("[3] - 5/50+2/12")
		
		odabir_test = False
		while odabir_test == False:
			try:
				odabir = int(input("Odabir [0/1/2/3] "))
				print("- "*7)
				assert odabir in range(4)
				odabir_test = True
			except:
				print("Pogrešan unos!")
				odabir_test = False	

		if odabir == 0:
			print("Hvala i doviđenja.")
			break
		
		print("Dopunski broj?")

		dopunski_test = False
		while dopunski_test == False:
			try:
				d = input("Odabir [Y/N] ")
				print("- "*7)
				assert d.upper() in ['Y','N']
				d = True if d.upper()=='Y' else False
				dopunski_test = True
			except:
				print("Pogrešan unos!")
				dopunski_test = False
		
		if odabir == 1:
			lotto_play(7,39,dopunski=d)
		elif odabir == 2:
			lotto_play(6,45,dopunski=d)
		elif odabir == 3:
			print("EUROJACKPOT")
			print("- "*7)
			lotto_play(5,50,dopunski=d)
			lotto_play(2,12,dopunski=d)

main()