# Realizado por: Brayan Steven Marín Quirós y Ronny Jiménez Bonilla
# Fecha de creación: 02/04/2019 10:00am
# Última modificación: 02/04/2019 11:20pm
# Versión: 3.7.2

#Importación de funciones

from funciones import *
from tkinter import *
from json import *
from requests import *

#Creación de la ventana
raiz = Tk()

#Propiedades de la ventana
raiz.title("Ventana principal")
raiz.iconbitmap("imagenes/icon.ico")
raiz.geometry("800x600")
raiz.resizable(0, 0)

#Creación frame
#miFrame = Frame()
#miFrame.pack()

#miFrame.config(width=800, height=600)

#Creación text area
txt_Area = Text(raiz, height=50, width=50)

#Crear scroll bar
scroll = Scrollbar(raiz)

txt_Area.pack(side=LEFT)
scroll.pack(side=RIGHT)

#Creación botón
btn_Share = Button(raiz, text="Share", command=funcionBotonBuscar).pack()

#Programa principal
raiz.mainloop()

#soy ronny
#aló
#picharmy

#Hola