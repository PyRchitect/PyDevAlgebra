#unosimo kombinaciju boja koja nas "pusta" kroz vrata
#provjeravamo je u "bazi" podataka
#ukoliko je ispravna, sve gori zeleno
#ukoliko je neispravna, sve se zacrveni
#automatski reset nakon 5s
 
# 1,2,3,back
# 4,5,6,clear
# 7,8,9,enter
# *,0,#,nesto
 
# 1-(0,0)
# 2-(2,0)
 
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
 
def iscrtaj_poziciju(koordinate):
    sense.clear()
    sense.set_pixel(koordinate[0],koordinate[1],W)
    time.sleep(1)
 
def provjeri_kod(otipkani_pin):
    pin_pronadjen=False
    user=''
    for pin_entry in pinovi:
        if pin_entry['pin']==otipkani_pin:
            print(f"Pustamo, Dobar dan {pin_entry['user']}")
            pin_pronadjen=True
            user=pin_entry['user']
            break
 
        else:
            pass
            #print('Ne pustamo')
    return (pin_pronadjen,user)
 
def pronadji_key_iz_value(coords):
    x=coords[0]
    y=coords[1]
    for key, value in mapirani_pin.items():
        if value[0]==x and value[1]==y:
            key_iz_dict=key
 
    return key_iz_dict
 
 
mapirani_pin={
    1:(0,0),
    2:(2,0),
    3:(4,0),
    'back':(6,0),
    4:(0,2),
    5:(2,2),
    6:(4,2),
    'clear':(6,2),
    7:(0,4),
    8:(2,4),
    9:(4,4),
    'enter':(6,4),
    'star':(0,6),
    0:(2,6),
    'hash':(4,6),
    'none':(6,6)
    }
 
pinovi=[
    {
        'user':'Mate',
        'pin':[4,5,1,2]
    },  
    {
        'user':'Stipe',
        'pin':[1,2,3,3]
    }
    ]
 
 
 
uneseni_pin=[-1,-1,-1,-1]
'''
for pin_entry in pinovi:
    if pin_entry['pin']==uneseni_pin:
        print(f"Pustamo, Dobar dan {pin_entry['user']}")
        break
    else:
        print('Ne pustamo')
'''
 
 
'''
for key,item in mapirani_pin.items():
    sense.clear()
    sense.set_pixel(item[0],item[1],W)
    time.sleep(0.5)
'''
 
trenutni_broj=1
koord=[0,0]
pin_broj=0
 
while True:
    iscrtaj_poziciju(koord)
    for event in sense.stick.get_events():
        if event.action=='pressed':
            if event.direction=='up' and koord[1]>0:
                koord[1]-=2
                print(koord)
                trenutni_broj=pronadji_key_iz_value(koord)
            elif event.direction=='down' and koord[1]<6:
                koord[1]+=2
                print(koord)
                trenutni_broj=pronadji_key_iz_value(koord)
            elif event.direction=='left' and koord[0]>0:
                koord[0]-=2
                print(koord)
                trenutni_broj=pronadji_key_iz_value(koord)
            elif event.direction=='right' and koord[0]<6:
                koord[0]+=2
                print(koord)
                trenutni_broj=pronadji_key_iz_value(koord)
            elif event.direction=='middle':
                trenutni_broj=pronadji_key_iz_value(koord)
                uneseni_pin[pin_broj]=trenutni_broj
                print(uneseni_pin)
                pin_broj+=1
                if pin_broj==4:
                    ispravan=provjeri_kod(uneseni_pin)
                    if ispravan[0]:
                        sense.clear(G)
                        sense.show_message(f'Dobar dan, {ispravan[1]}',text_colour=X,back_colour=G)
                    else:
                        sense.clear(R)
                    time.sleep(4)
                    sense.clear()
                    pin_broj=0