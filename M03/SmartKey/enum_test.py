from enum import Enum

class Poruke:
	P1 = "poruka 1"
	P2 = "poruka 2"
	P3 = "poruka 3"

print(Poruke.__dict__)
print(Poruke.__dict__["P1"])
print(Poruke.__dict__["P2"])