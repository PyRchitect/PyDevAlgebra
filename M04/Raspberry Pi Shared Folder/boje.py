from sense_emu import SenseHat
import time
import random
 
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
 
sense.clear(Dg)
 
stanje=[R,R,G,G,B,B,C,C,M,M,Y,Y,P,P,X,X]
random.shuffle(stanje)
print(stanje)
 
prikaz=[]
skriveno=[]
for _ in range(64):
    prikaz.append(Dg)
    skriveno.append(Dg)
 
sense.set_pixels(skriveno)
#time.sleep(3)
for indeks, boja in enumerate(stanje):
    skriveno[(indeks//4)*16+2*(indeks%4)+0]=boja
    skriveno[(indeks//4)*16+2*(indeks%4)+1]=boja
    skriveno[(indeks//4)*16+2*(indeks%4)+8]=boja
    skriveno[(indeks//4)*16+2*(indeks%4)+9]=boja
 
#sense.set_pixels(skriveno)
sense.set_pixels(prikaz)
 
 
pozicija=[0,0]
sense.set_pixel(pozicija[0],pozicija[1],W)
 
while True:
    for event in sense.stick.get_events():
        if event.action=='pressed':
 
            if event.direction=='up' and pozicija[1]>0:
                pozicija[1]-=2
                #sense.show_letter('U')
            elif event.direction=='down' and pozicija[1]<6:
                pozicija[1]+=2
                #sense.show_letter('D')
            elif event.direction=='left' and pozicija[0]>0:
                pozicija[0]-=2
                #sense.show_letter('L')
            elif event.direction=='right' and pozicija[0]<6:
                pozicija[0]+=2
                #sense.show_letter('R')
            elif event.direction=='middle':
                sense.set_pixel(pozicija[0], pozicija[1], stanje[indeks_boje])
                sense.set_pixel(pozicija[0]+1, pozicija[1], stanje[indeks_boje])
                sense.set_pixel(pozicija[0], pozicija[1]+1, stanje[indeks_boje])
                sense.set_pixel(pozicija[0]+1, pozicija[1]+1, stanje[indeks_boje])
                time.sleep(3)
                #sense.show_letter('M')
            sense.set_pixels(prikaz)
            sense.set_pixel(pozicija[0],pozicija[1],W)
            #print(pozicija[0],pozicija[1],pozicija[0]//2,pozicija[1]//2,pozicija[0]//2+pozicija[1]*2)
            indeks_boje=pozicija[0]//2+pozicija[1]*2
            print(stanje[indeks_boje])
 
 
            '''
            prikaz[(indeks//4)*16+2*(indeks%4)+0]=stanje[indeks_boje]
            prikaz[(indeks//4)*16+2*(indeks%4)+1]=stanje[indeks_boje]
            prikaz[(indeks//4)*16+2*(indeks%4)+8]=stanje[indeks_boje]
            prikaz[(indeks//4)*16+2*(indeks%4)+9]=stanje[indeks_boje]
            time.sleep(4)
            prikaz[(indeks//4)*16+2*(indeks%4)+0]=Dg
            prikaz[(indeks//4)*16+2*(indeks%4)+1]=Dg
            prikaz[(indeks//4)*16+2*(indeks%4)+8]=Dg
            prikaz[(indeks//4)*16+2*(indeks%4)+9]=Dg
            '''
            time.sleep(0.3)
 
'''            
https://pastebin.com/wcDMmhmB
'''