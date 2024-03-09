from time import sleep
from sense_emu import SenseHat

sense = SenseHat()

def test_sense():
    temperature = sense.get_temperature()
    print(f"T iz senzora: {temperature:.2f}")

    temperature_from_humidity = sense.get_temperature_from_humidity()
    temperature_from_pressure = sense.get_temperature_from_pressure()
    print(f"T iz senzora vlage: {temperature_from_humidity:.2f}")
    print(f"T iz senzora tlaka: {temperature_from_pressure:.2f}")

    pressure = sense.get_pressure()
    print(f"Tlak: {pressure:.2f}")
    humidity = sense.get_humidity()
    print(f"Vlaga: {humidity:.2f}")

    mjerenje = f"T: {temperature:.2f}; P: {pressure:.2f}; H: {humidity:.2f}"
    print(mjerenje)

def read_data():
    return (
        sense.get_temperature(),
        sense.get_pressure(),
        sense.get_humidity())

# ispod -10-W, ispod +12-B, ispod  +25-G, ispod +35-Y, iznad +35-R
R = (255,0,0)
G = (0,255,0)
B = (0,0,255)
K = (0,0,0)
W = (255,255,255)
Y = (255,255,0)
C = (0,255,255)
M = (255,0,255)

def ispisi_stupce(stupac,boja):
    for red in range(8):
        sense.set_pixel(stupac,red,boja)

sense.clear()
ispisi_stupce(2,M)
ispisi_stupce(5,M)

"""
while True:
    T,P,H = read_data()
    if T<-10:
        sense.clear(W)
    elif T<12:
        sense.clear(B)
    elif T<25:
        sense.clear(Y)
    elif T<35:
        sense.clear(G)
    else:
        sense.clear(R)
    sleep(0.5)
"""

"""v2

while True:
    T,P,H = read_data()
    if T<-10:
        ispisi_stupce(0,W)
        ispisi_stupce(1,W)
    elif T<12:
        ispisi_stupce(0,B)
        ispisi_stupce(1,B)
    elif T<25:
        ispisi_stupce(0,Y)
        ispisi_stupce(1,Y)
    elif T<35:
        ispisi_stupce(0,G)
        ispisi_stupce(1,G)
    else:
        ispisi_stupce(0,R)
        ispisi_stupce(1,R)
    sleep(0.5)
"""

""" v3
"""
def clear_s(stupac):
    for red in range(8):
        sense.set_pixel(stupac,red,K)

def ispisi_sr(stupac,redak,boja):
    clear_s(stupac)
    pocetni_redak=7-redak
    for red in range(pocetni_redak):
        sense.set_pixel(stupac,redak)

ispisi_sr(0,5,Y)
ispisi_sr(1,1,W)
time.sleep(0.5)