from sense_emu import SenseHat
import time
sense = SenseHat()

R = (255,0,0)
G = (0,255,0)
B = (0,0,255)
K = (0,0,0)

sense.clear()

def iscrtaj_tijelo():
	sense.clear()
	for piksel in pozicija:
		sense.set_pixel(piksel[0],piksel[1],R)

pozicija = [[0,0],[1,0],[2,0]]
korak = 0

iscrtaj_tijelo()

while True:
	for event in sense.stick.get_events():
		if event.action == 'pressed':
			korak+=1
			novi_x = pozicija[len(pozicija)-1][0]
			novi_y = pozicija[len(pozicija)-1][1]

			if event.direction == 'up':
				novi_y -=1
				if novi_y == -1:
					novi_y = 7
			elif event.direction == 'down':
				novi_y +=1
				if novi_y == 8:
					novi_y = 0
			elif event.direction == 'left':
				novi_x -=1
				if novi_x == -1:
					novi_x = 7
			elif event.direction == 'right':
				novi_x +=1
				if novi_x == 8:
					novi_x = 0

			nova_pozicija = [novi_x,novi_y]
			pozicija.append(nova_pozicija)
		
		
		if korak%5!=0:
			pozicija.pop(0)
		print(pozicija)
		iscrtaj_tijelo()
		time.sleep(0.3)