#interface para mover brazo Robot
#Autor: Victor Romero Bautista
#Mexico

#importar librerias 
import tkinter
from tkinter import *
from time import sleep
import tkinter.messagebox
import serial

#ser = serial.Serial('COM3', 9600, timeout = 1)
#ser.flush()
sleep(1)


#board.digital[pinS1].mode = SERVO
#board.digital[pinS2].mode = SERVO
#board.digital[pinS3].mode = SERVO
#board.digital[pinS4].mode = SERVO


#Funciones para mover articulaciones del brazo Robot

def servo1(posiciones1):
    print(posiciones1)
    pos1 = angulo1.get()
    pos1Str = 'x' + str(pos1)
    #ser.write(pos1Str.encode())


def servo2(posiciones2):
    print(posiciones2)
    pos2 = angulo2.get()
    pos2Str = 'y' + str(pos2)
    #ser.write(pos2Str.encode())

def servo3(posiciones3):
    print(posiciones3)
    #escritura de angulo en Servomotor
    #board.digital[pinS3].write(posiciones3)

#abrir Gripper
def abrir():
    print("abrir")
    #board.digital[pinS4].write(90)

#Cerrar Gripper
def cerrar():
    print("cerrar")
    #board.digital[pinS4].write(0)

#informacion
def info():
    tkinter.messagebox.showinfo("Informacion",
                            "Modo de uso: \nDesplazar cada perilla para mover las articulaciones del brazo robot \nPara abrir y cerrar el gripper, precione los respectivos botones")

##############################################3
##############################################

root = Tk()
root.title("Control de Brazo Robot")
root.minsize(320,300)


#Widgets ###################################
###########################################
#logo
#img = PhotoImage(file="lg.gif")
#widget = Label(root, image=img)
#widget.grid(column=1, row=1)

#etiqueta 1
var = StringVar()
etiqueta = Label(root, textvariable=var, relief=FLAT, pady=5)
var.set("Control de servomotores  \n Arduino <> Python")
etiqueta.grid(column=2, row=1)

#etiqueta apoyo
var2 = StringVar()
etiquetaAp = Label(root,textvariable=var2)
var2.set(" ")
etiquetaAp.grid(column=2,row=7)

#etiqueta apoyo2
var3 = StringVar()
etiquetaAy = Label(root,textvariable=var3)
var3.set(" ")
etiquetaAy.grid(column=2,row=5)

#Barra de posicion base
angulo1 = Scale(root,
                command = servo1,
                from_=0,
                to = 180,
                orient = HORIZONTAL,
                length = 300,
                troughcolor = 'gray',
                width=30,
                cursor='arrow',
                label = 'Posicion Base')
angulo1.grid(column=2, row=2)

#Barra de posicion brazo
angulo2 = Scale(root,
                command = servo2,
                from_=0,
                to = 180,
                orient = HORIZONTAL,
                length = 300,
                troughcolor = 'gray',
                width=30,
                cursor='dot',
                label = 'Posicion Brazo')
angulo2.grid(column=2, row=3)

#Barra de posicion antebrazo
angulo3 = Scale(root,
                command = servo3,
                from_=70,
                to = 179,
                orient = HORIZONTAL,
                length = 300,
                troughcolor = 'gray',
                width=30,
                cursor='dot',
                label = 'Posicion Antebrazo')
angulo3.grid(column=2, row=4)

##Gripper

#Abrir
#BoA = Button(root,
#                text="Abrir Gripper",
#               command=abrir,
#               relief=RAISED,
#                activebackground='green',
#                bd=3,
#                height=2,
#                width=17)
#BoA.grid(column=2, row=6)

#Cerrar
#BoC = Button(root,
#                text="Cerrar Gripper",
#                command=cerrar,
#               relief=RAISED,
#                activebackground='red',
#                bd=3,
#                height=2,
#                width=17)
#BoC.grid(column=2, row=8)

#boton informacion
#Binf = Button(root,
#                text="Modo de uso",
#                relief=GROOVE,
#                command=info)
#Binf.grid(column=1,row=2)

#etiqueta apoyo2
var4 = StringVar()
etiquetaAy = Label(root,textvariable=var4)
var4.set(" ")
etiquetaAy.grid(column=1,row=2)

root.mainloop()