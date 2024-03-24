# unosimo kombinaciju boja koja nas "pušta" kroz vrata
# provjeravamo je u "bazi" podataka
# ukoliko je ispravna, sve gori zeleno
# ukoliko je neispravna, sve se zacrveni
# automatski reset nakon 5 sekundi

# 1,2,3,Back
# 4,5,6,Clear
# 7,8,9,Enter
# *,0,#,Nesto

# kako pomičemo po ekranu kursor tako ćemo registrirat poziciju

import time

from sense_emu import SenseHat
sense=SenseHat()
 
R=(255,0,0)
G=(0,255,0)
B=(0,0,255)
C=(0,255,255)
M=(255,0,255)
Y=(255,255,0)
Dg=(40,40,40)
Gr=(190,190,190)
O=(255,128,0)
P=(240,90,120)
X=(40,100,60)
W=(255,255,255)
K=(0,0,0)
Br=(165,42,42)
sense.clear()

mapirani_pin ={
	1:		(0,0),
	2:		(2,0),
	3:		(4,0),
	'back':	(6,0),

	4:		(0,2),
	5:		(2,2),
	6:		(4,2),
	'clear':(6,2),

	7:		(0,4),
	8:		(2,4),
	9:		(4,4),
	'enter':(6,4),

	'*':	(0,6),
	0:		(2,6),
	'#':	(4,6),
	'none':	(6,6)
	}


pinovi = [
	{
		'user':'Mate',
		'pin':[4,5,1,2]
		},
		{
		'user':'Stipe',
		'pin':[1,2,3,3]
		}
	]

uneseni_pin = [4,5,1,2]

def iscrtaj_poziciju(koordinate):
	sense.clear()
	sense.set_pixel(koordinate[0],koordinate[1],W)
	time.sleep(1)

def provjeri_kod(otipkani_pin):
	pin_pronadjen = False
	user = ''
	for pin_entry in pinovi:
		if pin_entry['pin']== otipkani_pin:
			print(f"Pustamo, dobar dan {pin_entry['user']}")
			pin_pronadjen = True
			user = pin_entry['user']
			break			
		else:
			pass
	return (pin_pronadjen,pin_entry['user'])
	

for pin_entry in pinovi:
	if pin_entry['pin'] == uneseni_pin:
		print(f"Puštamo, Dobar dan {pin_entry['user']}")
		break
	else:
		print("Ne puštamo.")

for key,item in mapirani_pin.items():
	sense.clear()
	sense.set_pixel(*item,R)

trenutni_broj = 1
koord = [0,0]
pin_broj = 0


while True:
	iscrtaj_poziciju(koord)
	for event in sense.stick.get_events():
		if event.action=='pressed':
			if event.direction=='up':
				smjer = 'up'
				if trenutni_broj > 3:
					trenutni_broj -=3
				if trenutni_broj == 0:
					trenutni_broj = 8
				koord[0] = mapirani_pin[trenutni_broj][0]
				koord[1] = mapirani_pin[trenutni_broj][1]
			elif event.direction=='down':
				smjer = 'down'
				if trenutni_broj == 8:
					trenutni_broj = 0
				elif trenutni_broj < 7 and trenutni_broj != 0:
					trenutni_broj +=3
				koord[0] = mapirani_pin[trenutni_broj][0]
				koord[1] = mapirani_pin[trenutni_broj][1]
			elif event.direction=='left':
				smjer = 'left'
				trenutni_broj-=1
				if trenutni_broj == -1:
					trenutni_broj = 9
				koord[0] = mapirani_pin[trenutni_broj][0]
				koord[1] = mapirani_pin[trenutni_broj][1]
			elif event.direction=='right':
				smjer = 'right'
				trenutni_broj+=1
				if trenutni_broj == 10:
					trenutni_broj = 0
				koord[0] = mapirani_pin[trenutni_broj][0]
				koord[1] = mapirani_pin[trenutni_broj][1]

			elif event.direction == 'middle':
				uneseni_pin[pin_broj] = trenutni_broj
				print(uneseni_pin)
				pin_broj += 1
				if pin_broj == 4:
					ispravan=provjeri_kod(uneseni_pin)
					pin_broj = 0
					if ispravan[0]:
						sense.show_message(ispravan[1],text_colour=X,back_colour=G)
					else:
						sense.clear(R)
					time.sleep(4)
					sense.clear()
					pin_broj=0