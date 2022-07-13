from cgi import print_directory
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
arduinoEstado = False

def json_validator(data):
    try:
        #print("mensaje mqtt: ", data)
        json.loads(data)
        return True
    except ValueError as error:
        print("invalid json")
        return False

def on_message(client, userdata, message):
    global horaTemp
    global temper
    global tiempo
    global activo
    horaTemp = str(message.payload.decode("utf-8"))
    print("mensaje mqtt: ", horaTemp)
    validaJson1 = json_validator(horaTemp)
    if validaJson1 == True:
        htJson = json.loads(horaTemp)
        #print("Mensaje dentro de la funcion ")
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
#time.sleep(20)

connection = mysql.connector.connect(host='localhost', port = '3306', database='secadora', user='cursoIoT', password='cursoIoT')
broker_address = "172.16.80.230"
tiempo = 0

client = mqtt.Client("P1")              #create new instance
client.on_message=on_message            #attach function to callback
client.connect(broker_address)          #conectar al broker
client.loop_start()                     #inicio de loop para recibir datos
client.subscribe("secadora/controles")

clientP= mqtt.Client("publicar")
clientP.on_publish = on_publish         #asignar funcion a callback
clientP.connect(broker_address, 1883)   #establecer conexion

#Ciclo para esperar a que arduino este iniciado y enviando json

while True:
    if activo == 1:
        print("precalentado")
        arduino.write('p'.encode('ascii'))
        time.sleep(2)
        inicio = arduino.readline().decode('ascii')
        print("edo1: ", inicio)
        if inicio != "":
            validaJson2 = json_validator(inicio)
            if validaJson2 == True:
                ardJson = json.loads(inicio)
                temperA = ardJson["temp"]
                #cargaA = ardJson["carg"]
                ret= clientP.publish("secadora/lectura/temperatura", temperA)
                time.sleep(1)

    if activo == 2:
        print("Recibiendo datos")
        arduino.write('i'.encode('ascii'))
        time.sleep(2)
        inicio = arduino.readline().decode('ascii')
        print("edo2: ", inicio)
        if inicio != "":
            validaJson2 = json_validator(inicio)
            if validaJson2 == True:
                ardJson = json.loads(inicio)
                temperA = ardJson["temp"]
                cargaA = ardJson["carg"]
                ret= clientP.publish("secadora/lectura/temperatura", temperA)
                ret= clientP.publish("secadora/lectura/carga", cargaA)
                time.sleep(1)

    if activo == 3:
        print("Paro de emergencia")
        arduino.write('e'.encode('ascii'))
        time.sleep(1)

    if activo == 4:
        print("Fin de ciclo")
        arduino.write('f'.encode('ascii'))
        time.sleep(1)
        break

    
"""
while True:
    print("Mensaje despues de la funcion ")
    time.sleep(1)
    
    #inicio = arduino.readline().decode('ascii')
    inicio = "x"
    if inicio != "":
        validaJson2 = json_validator(inicio)
        if validaJson2 == True:
            ardJson = json.loads(inicio)
            temperA = ardJson["temp"]
            cargaA = ardJson["carg"]
            print(str(temperA) + "x" + str(cargaA))
    time.sleep(1)
    if activo == 1:
        #arduino.write('i'.encode('ascii'))
        print("enviando a arduino")
        break
    
    if activo == 4:
        #arduino.write('i'.encode('ascii'))
        print("enviando a arduino")
        break

"""

"""
while True:
    cad = arduino.readline().decode('ascii')
    time.sleep(2)
    
    print(temper)
    print(tiempo)
    print(activo)
    print(cad)
    
    if cad != "" and activo == 2:

        validaJson = json_validator(cad)
        if validaJson == True:
            ardJson = json.loads(cad)
            temper = ardJson["temp"]
            carga = ardJson["carg"]
            print(temper)
            print(carga)

            
            ret= clientP.publish("secadora/lectura/temperatura", temper)
            ret= clientP.publish("secadora/lectura/carga", carga)
            insetarDatos(temper, carga, 0, 'naranjas')
"""