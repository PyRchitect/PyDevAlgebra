from sense_emu import SenseHat
import time
sense=SenseHat()
 
def read_data():
    temperature=round(sense.get_temperature(),1)
    #print(temperature)
    pressure=round(sense.get_pressure(),1)
    #print(pressure)
    humidity=round(sense.get_humidity(),1)
    #print(humidity)
 
    mjerenje=f'Temp: {temperature}; Press: {pressure}; Humid: {humidity}'
    #sense.show_message(mjerenje)
    print(mjerenje)
    return (temperature, pressure, humidity)
 
 
# ispod -10-W, ispod +12-B, ispod +25-G, ispod +35-Y, iznad 35-R
R=(255,0,0)
G=(0,255,0)
B=(0,0,255)
K=(0,0,0)
W=(255,255,255)
Y=(255,255,0)
C=(0,255,255)
M=(255,0,255)
 
""" v1 citavi ekran
"""
def ispisi_stupac(stupac,boja):
    #sense.clear()
    #stupac=2
    #boja=M
    for red in range(8):
        sense.set_pixel(stupac,red,boja)
    #time.sleep(5)
 
sense.clear()
ispisi_stupac(2,M)
ispisi_stupac(5,M)
time.sleep(5)
 
"""
while True:
    T,P,H=read_data()
    if T<-10:
        sense.clear(W)
    elif T<12:
        sense.clear(B)
    elif T<25:
        sense.clear(G)
    elif T<35:
        sense.clear(Y)
    else:
        sense.clear(R)
    time.sleep(0.5)
"""
 
"""v2
"""
"""
while True:
    T,P,H=read_data()
    if T<-10:
        ispisi_stupac(0,W)
        ispisi_stupac(1,W)
    elif T<12:
        ispisi_stupac(0,B)
        ispisi_stupac(1,B)
    elif T<25:
        ispisi_stupac(0,G)
        ispisi_stupac(1,G)
    elif T<35:
        ispisi_stupac(0,Y)
        ispisi_stupac(1,Y)
    else:
        ispisi_stupac(0,R)
        ispisi_stupac(1,R)
    time.sleep(0.5)
"""
 
 
"""v3
Pokusavamo linearno prikazati temperature od -30 do 105°C
Jedan red led na samom dnu (2 ledice uvijek gore)
 
105
    00
89
    11
72
    22
55
    33
38
    44
21
    55
4
    66
-13
    77
-30
"""
def clear_s(stupac):
    for red in range(8):
        sense.set_pixel(stupac, red, K)
 
def ispisi_sr(stupac, redak, boja):
    clear_s(stupac)
    pocetni_redak=7-redak
    for red in range(pocetni_redak,8):
        sense.set_pixel(stupac, red, boja)
 
 
 
#sense.clear()
#ispisi_sr(0,0,Y)
#ispisi_sr(1,5,Y)
#time.sleep(0.5)
 
 
while True:
    T,P,H=read_data()
    if T<-13:
        ispisi_sr(0,0,W)
    elif T<4:
        ispisi_sr(0,1,B)
    elif T<21:
        ispisi_sr(0,2,G)
    elif T<38:
        ispisi_sr(0,3,Y)
    elif T<55:
        ispisi_sr(0,4,R)
    elif T<72:
        ispisi_sr(0,5,R)
    elif T<89:
        ispisi_sr(0,6,R)
    else:
        ispisi_sr(0,7,M)
    time.sleep(0.5)
 