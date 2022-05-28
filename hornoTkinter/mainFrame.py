from tkinter import Entry, Frame,Label,Button,Checkbutton,Scale,StringVar,IntVar, Canvas
from tkinter.constants import DISABLED
import serial
import time
import threading
##########
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from threading import Thread
##########

arduino = serial.Serial("COM8",9600,timeout=1.0)

class MainFrame(Frame):

    ############
    global getData
    def getData():
        time.sleep(1.0)
        #serialConnection.reset_input_buffer() #resetea el buffer

        while(isRun):
            global isReceiving
            global value
            value1 = arduino.readline().decode('ascii').strip()
            pos=value1.index(":")
            label=value1[:pos]
            value=float(value1[pos+1:])
            isReceiving = True

    def plotData(self, Samples, lines):
        global value
        data.append(value)
        lines.set_data(range(Samples), data)

    ############
    def __init__(self, master=None):
        super().__init__(master, width=520, height=670)                
        self.master = master    
        self.master.protocol('WM_DELETE_WINDOW',self.askQuit)
        self.pack()
        self.hilo1 = threading.Thread(target=self.getSensorValues,daemon=True)
        #global arduino
        self.arduino = serial.Serial("COM7",9600,timeout=1.0)
        time.sleep(1)
        self.value_pot = StringVar()
        self.value_dis = StringVar()
        self.value_mot = StringVar()
        self.value_mot2 = StringVar()
        self.value_led = IntVar()
        self.create_widgets()
        self.isRun=True
        self.hilo1.start()

    def askQuit(self):
        self.isRun=False
        self.arduino.write('mot:0'.encode('ascii'))
        time.sleep(1.1)
        self.arduino.write('led:0'.encode('ascii'))
        self.arduino.close()
        self.hilo1.join(0.1)
        self.master.quit()
        self.master.destroy()
        print("*** finalizando...")

    def getSensorValues(self):

        print("Lectura")
        
        while self.isRun:
            cad =arduino.readline().decode('ascii').strip()
            print(cad)
            if cad:
                print(cad)         
                pos=cad.index(":")
                label=cad[:pos]
                value=cad[pos+1:]
                #if label == 'dis':
                self.value_dis.set(value)
                #if label == 'pot':
                self.value_pot.set(label)
        

        
    def fGrafica(self):
        isReceiving = False
        global isRun
        isRun = True
        value = 0.0

        
        thread = Thread(target = getData)
        thread.start()

        while isReceiving != True:
            print("iniciando recpecion de datos")
            time.sleep(2.1)

        samples = 100
        data = collectione.deque([0] * samples, maxlen = samples)
        sampleTime = 100

        xmin = 0
        xmax = samples
        ymin = 0
        ymax = 200

        global fig
        fig = plt.figure(facecolor='0.94')
        ax = plt.axes(xlim = (xmin, xmax), ylim = (ymin, ymax))
        plt.title("grafica")
        ax.set_xlabel("muestras")
        ax.set_ylabel("valor")

        lines = ax.plot([], [])[0]
        Canvas = FigureCanvasTkAgg(fig, master=self)
        Canvas._tkcanvas.grid(row = 0)

    def fEnviaMot(self):
        cad = self.value_mot.get() + ":" +self.value_mot2.get()
        self.arduino.write(cad.encode('ascii'))
        print(cad)

        
    def create_widgets(self):
        Label(self,text="Temperatura actual: ").place(x=30,y=20)
        #Label(self,width=6,textvariable=self.value_pot).place(x=180,y=20)
        Entry(self,width=8,textvariable=self.value_pot,justify='center',state='disabled').place(x=180,y=20)
        Label(self,text="Peso actual: ").place(x=30,y=50)
        #Label(self,width=6,textvariable=self.value_dis).place(x=180,y=50)
        Entry(self,width=8,textvariable=self.value_dis,justify='center',state='disabled').place(x=180,y=50)
        #Checkbutton(self, text="Encender/Apagar Led", variable=self.value_led,
        #onvalue=1, offvalue=0,command=self.fEnviaLed).place(x=30, y=90)                 
        Label(self,text="Temperatura: ").place(x=30,y=132)
        Scale(self, from_=0, to=180,orient='horizontal',tickinterval=20,
        length=220,variable=self.value_mot).place(x=110,y=115)
        Label(self,text="Tiempo: ").place(x=30,y=192)
        Scale(self, from_=20, to=100,orient='horizontal',tickinterval=20,
        length=220,variable=self.value_mot2).place(x=110,y=175)
        Button(self,text="Iniciar", command=self.fEnviaMot).place(x=360,y=160)
        Button(self,text="Graficar", command=self.fGrafica).place(x=360,y=190)
        #canvas = Canvas(root, bg='red')