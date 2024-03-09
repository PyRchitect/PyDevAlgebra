from sense_emu import SenseHat
import time
sense=SenseHat()
 
#ziroskop=sense.get_orientation()
#roll, pitch, yaw = ziroskop.values()
 
roll, pitch, yaw = sense.get_orientation().values()
 
roll=round(roll, 2)
pitch=round(pitch, 2)
yaw=round(yaw, 2)
 
mjerenje=f'Roll: {roll}; Pitch: {pitch}; Yaw: {yaw}'
#sense.show_message(mjerenje)
print(mjerenje)
 
accelerometer=sense.get_accelerometer_raw().values()
print(accelerometer)
 
sense.show_letter('P')
while True:
    x, y, z = sense.get_accelerometer_raw().values()
    x=round(x,0)
    y=round(y,0)
    if x==-1:
        sense.set_rotation(180)
    elif y==1:
        sense.set_rotation(90)
    elif y==-1:
        sense.set_rotation(270)
    else:
        sense.set_rotation(0)