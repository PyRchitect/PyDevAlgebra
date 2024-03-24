'''
     x      x
   x
              x
	 G

	   A
'''
 
# x=R (njih izbjegavamo)
# bodovi=G (njih skupljamo)
# brzina se mijenja (ubrzavamo)
# auto je žute boje

from sense_emu import SenseHat
import time
import random
sense = SenseHat()
 
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

def iscrtaj_auto():
	sense.clear()
	for piksel in auto:
		sense.set_pixel(piksel[0],piksel[1],Y)
	for kamen in kamenje:
		sense.set_pixel(kamen[0],kamen[1],M)

auto = [[3,7]]  # može biti širi (hummer, kamion, ...) pa 2,3 piksela
korak = 0

kamenje = [[random.randint(0,7),0]] # više kamenja

iscrtaj_auto()

while True:
	for event in sense.stick.get_events():
		if event.action == 'pressed':

			if event.direction == 'left' and auto[0][0]>0:
				novi_x = auto[0][0] - 1
				auto[0][0] = novi_x
			elif event.direction == 'right' and auto[0][0]<7:
				novi_x =auto[0][0] + 1
				auto[0][0] = novi_x
			elif event.direction == 'middle':
				pass
		
		korak += 1
		if korak%10 == 0:
			for kamen in kamenje:
				kamen[1]+=1

			if kamenje and kamenje[0][1] == 8:
				kamenje.pop(0)

		print(auto)
		iscrtaj_auto()
		time.sleep(0.3)