# a = 5
# b = 0

def f1():
	try:
		c=a//b
	except ZeroDivisionError as ZDE:
		print(f"Greska: {ZDE}")
	except Exception as ERR:
		print(f"Greska: {ERR}")
	else:
		print("Nije bilo greske!")
	finally:
		print("Gotovo!")
		print(c)

def f2():
	broj=0
	while broj==0:
		try:
			broj=int(input('Unesi broj od 1 do 10: '))
			assert broj in range(1,11)
		except (AssertionError,ValueError) as e:
			broj=0
		finally:
			print('uvijek zavrtimo ovo')

# f1()
f2()