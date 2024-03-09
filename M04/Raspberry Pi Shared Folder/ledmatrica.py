import time
from sense_emu import SenseHat
sense = SenseHat()
sense.show_message('Pozdrav svima!')

plavo = (0,0,255)
# sense.show_message("I'm blue dabudidabudam",text_colour=plavo)

pozadina_zelena = (0,255,0)
# sense.show_message(
#'Malo igre',
#text_colour=plavo,
#back_colour=pozadina_zelena,
#scroll_speed=0.05)

sense.show_letter(
'P',
text_colour=plavo,
back_colour=pozadina_zelena)

time.sleep(0.5)
sense.set_pixel(0,2,[255,0,0])
time.sleep(0.5)
sense.clear()
sense.set_pixel(0,2,[255,0,0])
time.sleep(0.5)
sense.clear(plavo)

R = (255,0,0)
G = (0,255,0)
B = (0,0,255)
K = (0,0,0)
W = (255,255,255)
Y = (255,255,0)
C = (0,255,255)
M = (255,0,255)

zastava = [
    G,G,G,G,G,G,G,G,
    R,R,R,R,R,R,R,R,
    R,R,R,R,R,R,R,R,
    W,W,W,W,W,W,W,W,
    W,W,W,W,W,W,W,W,
    B,B,B,B,B,B,B,B,
    B,B,B,B,B,B,B,B,
    G,G,G,G,G,G,G,G
    ]

sense.clear()
sense.show_letter('P')

sense.set_rotation(90)

kutevi = [0,90,180,270,0,90,180,270,0]

for kut in kutevi:
    sense.set_rotation(kut)
    time.sleep(0.5)