from sense_emu import SenseHat
import time
sense=SenseHat()
 
R=(255,0,0)
G=(0,255,0)
B=(0,0,255)
K=(0,0,0)
sense.clear()
 
def iscrtaj_tijelo():
    sense.clear()
    for piksel in pozicija:
        sense.set_pixel(piksel[0],piksel[1],R)
 
pozicija=[[0,0],[1,0],[2,0]]
korak=0
 
iscrtaj_tijelo()
 
 
 
 
 
while True:
    for event in sense.stick.get_events():
        if event.action=='pressed':
            korak+=1
            if event.direction=='up':
                novi_x=pozicija[len(pozicija)-1][0]
                novi_y=pozicija[len(pozicija)-1][1]
                novi_y-=1
                if novi_y==-1:
                    novi_y=7
                nova_pozicija=[novi_x, novi_y]
                pozicija.append(nova_pozicija)
 
 
            elif event.direction=='down':
                pozicija[1]+=1
                #sense.show_letter('D')
            elif event.direction=='left':
                pozicija[0]-=1
                #sense.show_letter('L')
            elif event.direction=='right':
                pozicija[0]+=1
                #sense.show_letter('R')
            elif event.direction=='middle':
                pass
            #sense.clear()
            #sense.set_pixel(pozicija[0],pozicija[1],R)
            if korak%5!=0:
                pozicija.pop(0)
            print(pozicija)
            iscrtaj_tijelo()
            time.sleep(0.3)