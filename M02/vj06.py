# ulaz je int broj (type je int) od 0 do 15 - 15 -> 1111 0 -> 0000
# pretvaramo u binarni ALI type ostaje int !!!
# MI cemo napisati program koji ce napraviti tu konverziju

def konverzije_baza(broj,baza):
	digits = []
	while broj > 0:
		digits.insert(0,broj%baza)
		broj = broj//baza
	return digits

def test_baze():
	broj = 8 # za testiranje
	baza = 2 # za testiranje
	print("\n> konverzija baza - test:")
	print(f"dec: {broj}")
	result = konverzije_baza(broj,baza)
	print(f"baza {baza}: {result}")

	result_str = '0b'+''.join([str(i) for i in result])
	print("\n> konvertiraj natrag - test:")
	print(f"result (baza 2): {result_str}")
	print(f"result (baza 10): {int(result_str,2)}")

test_baze()