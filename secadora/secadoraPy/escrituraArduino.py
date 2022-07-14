import time
import serial

import json
############
arduino = serial.Serial("/dev/ttyACM0", 115200, timeout=1.0)
time.sleep(20)
arduino.write('i'.encode('ascii'))
print("fin  ")
