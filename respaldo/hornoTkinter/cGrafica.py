from logging import root
from matplotlib import lines
import serial
import time
import collections
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from tkinter import *
from threading import Thread

pwmValue = 0
global temp

def getData():
    time.sleep(1.0)
    ser.reset_input_buffer()
    while(isRun):
        global isReceiving
        global value
        global valueTemp
        print(imprimir)
        #valueTemp = (serialConnection.readline().strip())
        valueTemp = ser.readline().decode('utf-8').rstrip()
        cad = valueTemp
        print("cad" + cad)
        pos=cad.index(":")
        label=cad[:pos]
        value=cad[pos+1:]

        print("valueTemp = " + str(value))
        if imprimir == True:
            #value = float(ser.readline().decode('utf-8').rstrip())
            value = value
        else:
            value = 0
        isReceiving = True

def askQuit():
    global isRun
    isRun = False
    thread.join()
    ser.write(('0\n').encode())
    ser.close()
    root.quit()
    root.destroy()

def plotData(self, Samples, lines):
    global value
    data.append(value)
    lines.set_data(range(Samples), data)
    pwm.set("RPM: " + str(value))
    temp.set("Temperatura: " + str(valueTemp))

def motorControl(int):
    global pwmValue
    global imprimir
    imprimir = True
    pwmValue = str(slider.get())
    pwm.set("RPMX: " + pwmValue)
    #if pwmValue == 100:
        #isRun = True

isReceiving = False
isRun = True
imprimir = False
value = 0.0
valueTemp = 0
ser = serial.Serial('COM14', 9600)

thread = Thread(target = getData)
thread.start()

while isReceiving != True:
    #print("iniciando")
    time.sleep(0.1)

samples = 100
data = collections.deque([0] * samples, maxlen = samples)
sampleTime = 100

xmin = 0
xmax = samples
ymin = 0
ymax = 200

fig = plt.figure(facecolor = '0.94')
ax = plt.axes(xlim = (xmin, xmax), ylim = (ymin, ymax))
plt.title("grafica")
ax.set_xlabel("Muestras")
ax.set_xlabel("Peso en gramos")

lines = ax.plot([], [])[0]

root = Tk()
root.protocol('WM_DELETE_WINDOW', askQuit)

canvas = FigureCanvasTkAgg(fig, master = root)
canvas._tkcanvas.grid(row = 0)

frame = Frame(root, width = 400, height = 200)
frame.grid(row = 0, column = 1, padx = 10, pady = 5)
frame.grid_propagate(False)

pwm = StringVar(root, "PWM")
temp = StringVar(frame, "TEMP")

labelPwm = Label(frame, textvariable = pwm)
labelPwm.grid(row = 0, column = 0, padx = 20, pady = 20)

slider = Scale(frame, from_= 0, to = 255, orient = HORIZONTAL, command = motorControl, length = 200)
slider.grid(row = 1, padx = 20, pady = 20)

labelTemp = Label(frame, textvariable = temp)
labelTemp.grid(row = 2, column = 0, padx = 20, pady = 20)

anim = animation.FuncAnimation(fig, plotData, fargs = (samples, lines), interval = sampleTime)

root.geometry('1100x600')
root.mainloop()