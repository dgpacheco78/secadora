import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import mysql.connector #####
from mysql.connector import Error #####
from mysql.connector import errorcode #####
from random import randrange

serialPort = 'COM14'
beudRate = 9600
Samples = 20
sampleTime = 100
data = collections.deque([0] * Samples, maxlen = Samples)

try:
    serialConnection = serial.Serial(serialPort, beudRate)
except:
    print('puerto no disponible')

def getSerialData(self, Samples, serialConection, lines, lineValueText, lineLabel):
    #value = float(serialConnection.readline().strip())
    value = randrange(10)
    print(value)
    data.append(value)
    lineValueText.set_text(lineLabel + ' = ' + str(round(value,2)))
    lines.set_data(range(Samples), data)
    
def grafica():
    xmin = 0
    xmax = Samples
    ymin = 0
    ymax = 50

    fig = plt.figure(figsize = (13,6))
    ax = plt.axes(xlim = (xmin, xmax), ylim = (ymin, ymax))
    plt.title("Sensor en tiempo real")
    ax.set_xlabel("Muestra")
    ax.set_ylabel("Temperatura")

    lineLabel = 'Temperatura'
    lines = ax.plot([], [], label = lineLabel)[0]
    lineValueText = ax.text(0.85, 0.95, '', transform = ax.transAxes)
    anim = animation.FuncAnimation(fig, getSerialData, fargs = (Samples, serialConnection, lines, lineValueText, lineLabel), interval = sampleTime)
    plt.show()
    serialConnection.close()

#grafica()