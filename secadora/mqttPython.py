#Importar clases
from ast import Str
from time import sleep
import paho.mqtt.client as paho
import serial


#declaracion de objetos y variables
broker="172.16.80.230"
port=1883
arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1.0)
sleep(0.5)

#definicion de funciones
def on_publish(client,userdata,result):
    print("data published \n")
    pass

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")
  
def on_message(client, userdata, message):
    print(Str(message.payload))

client1= paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback

client1.on_connect= on_connect                      #attach function to callback
client1.on_message= on_message 
client1.connect(broker,port)                                 #establish connection

client1.loop_start()  
client1.subscribe("python/test")

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print("exiting")
    client1.disconnect()
    client1.loop_stop()

"""
while True:
    cad = arduino.readline().decode('ascii').strip()
    sleep(1)
    print(cad)
    ret= client1.publish("codigoIoT/python",cad)
"""


