import paho.mqtt.client as mqtt #import the client1
import time
import serial
import mysql.connector
import json
############

horaTemp = ""
temper = 0
tiempo = 0
activo = 0

def on_message(client, userdata, message):
    global horaTemp
    global temper
    global tiempo
    global activo
    horaTemp = str(message.payload.decode("utf-8"))
    htJson = json.loads(horaTemp)
    print("Mensaje dentro de la funcion " , horaTemp)
    temper = htJson["temp"]
    tiempo = htJson["tiem"]
    activo = htJson["acti"]

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def insetarDatos(tem, pes, vel, tip):
    try:
        query = "insert into muestras (temperatura, peso, velocidad, hora, fecha, tipoProducto) values (" + str(tem) + ", " + str(pes) + ", " + str(vel) + ", NOW(), NOW(), '" + tip + "');"
        print(query)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))

arduino = serial.Serial("/dev/ttyACM0", 115200, timeout=1.0)
connection = mysql.connector.connect(host='localhost', port = '3306', database='secadora', user='cursoIoT', password='cursoIoT')
broker_address="172.16.80.230"
tiempo = 0

client = mqtt.Client("P1") #create new instance
clientP= mqtt.Client("publicar")
client.on_message=on_message #attach function to callback
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop

client.subscribe("secadora/controles")

#time.sleep(4) # wait
while True:
    print("Mensaje despues de la funcion " , horaTemp)
    time.sleep(1)
    if horaTemp != "":
        break
    
#client.loop_stop() #stop the loop

#print("Publishing message to topic","house/bulbs/bulb1")
#client.publish("house/bulbs/bulb1","ON")

clientP.on_publish = on_publish                          #assign function to callback
clientP.connect(broker_address, 1883)                                 #establish connection

while True:
    cad = arduino.readline().decode('ascii')
    time.sleep(2)
    
    print(temper)
    print(tiempo)
    print(activo)
    print(cad)
    
    if cad != "" and activo == 1:
        pos = cad.index(":")
        temSecadora = cad[:pos]
        carSecadora = cad[pos+1:]
        print(temSecadora)
        print(carSecadora)
    

        ret= clientP.publish("secadora/lectura/temperatura",temSecadora)
        ret= clientP.publish("secadora/lectura/carga",carSecadora)

        insetarDatos(temSecadora, carSecadora, 0, 'naranjas')
    

#ret= clientP.publish("house/bulbs/bulb1","OFF")