"""
Secadora Industrial de Alimentos
David García Pacheco
Alfonso Monterrosas Fuentes
Salomón Tapia Aguilar
Universidad Tecnológica de Izúcar de Matamoros

Control del sistema
Recibe los datos de los sensores mediante un json
Al inicio recibe un json con valores en cero, indicando que el programa en arduino esta inicializado y listo para recibir ordenes
Una vez que recibe las ordenes de inicio en el json se envian los valores de temperatura, pero y revoluciones por minuto del ventilador
{"temp":0, "carg":0, "rpm":0}
temp = temperatura del sistema, promedio de los dos sensores
carg = peso del sensor de carga, recibe la perdida de peso de las muestras
rmp = revoluciones por minuto del ventilador
Los valores de las variables son enviados a Node-Red mediante MQTT
clientP.publish("secadora/lectura/temperatura", temperA)
clientP.publish("secadora/lectura/carga", cargaA)
clientP.publish("secadora/lectura/rpm", rpmA)

El control recibe un json proveniente de Node-Red para que controle el sistema y las ordenes indicadas son enviadas a Arduino
{"temp":0, "tiem":0, "acti":2}
temp = temperatura para inicio del proceso, normalmente 70°C
tiem = tiempo del proceso de secado, de 4 a 6 horas dependiendo del tipo de muestra
acti = actividad a realizar, se han definido 4:
        1. Precalentando el horno
        2. Recibiendo datos del horno
        3. Paro de emergencia
        4. Fin de ciclo
"""

from cgi import print_directory         #importar librerias necesarias para el funcionamiento del sistema
import paho.mqtt.client as mqtt         #mqtt
import time                             #retardos
import serial                           #comunicacion serial
import mysql.connector                  #mysql
import json                             #metodos para json

horaTemp = ""                           #definicion de variables globales
temper = 0
tiempo = 0
activo = 0
arduinoEstado = False

def json_validator(data):               #validacion de cadenas tipo json
    try:                                #cadenas recibidas de node-red y arduino
        json.loads(data)                #son validadas en estructura
        return True
    except ValueError as error:
        print("invalid json")
        return False

def on_message(client, userdata, message):  #funcion que recibe los mensajes por mqtt desde node-red
    global horaTemp                         #se establecen las variables como "globales"
    global temper                           #ya que se utilizaran en todo el programa
    global tiempo
    global activo
    horaTemp = str(message.payload.decode("utf-8"))     #recepcion de la cadena desde node-red
    print("mensaje mqtt: ", horaTemp)
    validaJson1 = json_validator(horaTemp)              #se valida que la cadena tenga estructura json
    if validaJson1 == True:                             #de ser correcta la estrutura
        htJson = json.loads(horaTemp)                   #se asigna la cadena a un objeto json
        #print("Mensaje dentro de la funcion ")
        temper = htJson["temp"]                         #se obtienen los valores de las variables del
        tiempo = htJson["tiem"]                         #json y se asignan a sus respectivas 
        activo = htJson["acti"]                         #variables globales

def on_publish(client,userdata,result):                 #creacopm de la función para callback
    print("data published \n")
    pass

def insetarDatos(tem, pes, vel, tip):
    try:
        query = "insert into muestras (temperatura, peso, velocidad, hora, fecha, tipoProducto) values (" + str(tem) + ", " + str(pes) + ", " + str(vel) + ", NOW(), NOW(), '" + tip + "');"
        #print(query)
        cursor = connection.cursor()        #creación del objeto tipo conector
        cursor.execute(query)               #ejecución de la consulta para 
        connection.commit()                 #insertar los valores provenientes
        cursor.close()                      #de los sensores vía arduino
    except mysql.connector.Error as error:
        print("Error en la inserción de datos: {}".format(error))



arduino = serial.Serial("/dev/ttyACM0", 115200, timeout = 1.0)  #creacion del objeto tipo serial para establecer la conexión con arduino
#time.sleep(20)

connection = mysql.connector.connect(host = 'localhost', port = '3306', database = 'secadora', user = 'cursoIoT', password = 'cursoIoT')
#conexión a la base de datos
broker_address = "192.168.0.15"    #direccion IP donde se encuentra el servidor mqtt
#tiempo = 0

client = mqtt.Client("P1")              #creación de nueva instancia mqtt
client.on_message=on_message            #adjuntar función al callback
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
                ret = clientP.publish("secadora/lectura/temperatura", temperA)
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
                ret = clientP.publish("secadora/lectura/temperatura", temperA)
                ret = clientP.publish("secadora/lectura/carga", cargaA)
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