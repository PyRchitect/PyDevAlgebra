ime = 'Mate'
prezime = "Matic"
#krivo = "Ovo je krivo'

english = "He's 20 years old"
navodnici = 'Ovo je "PANDA"'

print("Hello world!")
print(ime,prezime)
print(ime,prezime,sep='*****')
print(ime,prezime,end='')

print('He\'s a "golden" employee.')

putanja = 'C:\\Users'
print(putanja)
print("\"\'\ttest\\")

godina_rodenja = 1960
print(godina_rodenja)

def func(pargs,kargs):
	"""
	docstring test
	"""
	print(f"hello world!\npargs:{pargs}\nkargs:{kargs}")

help(func)

a = 3
b = 3
o = 2*(a+b)
p = a*b

brojnik = 6
nazivnik = 4

print(brojnik/nazivnik)
print(brojnik//nazivnik)
print(brojnik%nazivnik)