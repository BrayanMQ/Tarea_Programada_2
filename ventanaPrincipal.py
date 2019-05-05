# Realizado por: Brayan Steven Marín Quirós y Ronny Jiménez Bonilla
# Fecha de creación: 02/04/2019 10:00am
# Última modificación: 02/04/2019 11:20pm
# Versión: 3.7.2

#Importación de funciones

from funciones import *
from tkinter import *


#Creación de la ventana
root = Tk()

#Propiedades de la ventana
root.title("Ventana principal")
root.iconbitmap("imagenes/icon.ico")
root.resizable(0, 0)

#Creación frame
frame = Frame()
frame.pack()
frame.config(width=800, height=600)

#Creación del título
lbl_Titulo = Label(frame, text="Frases de Star Wars")
lbl_Titulo.grid(row=0, column=0, padx=10, pady=10, sticky="n")
lbl_Titulo.config(font="Helvetica")


#Creación text area
txt_Area = Text(frame)
txt_Area.grid(row=1, column=0, padx=10, pady=10)
txt_Area.config(state="disabled")

scrollVertical = Scrollbar(frame, command=txt_Area.yview())
scrollVertical.grid(row=1, column=1, sticky="nsew")
txt_Area['yscrollcommand'] = scrollVertical.set


#Creación widgets

btn_Buscar = Button(frame, text="Buscar", command=funcionBotonBuscar, width=20, height=1)
btn_Buscar.grid(row=1, column=2, sticky="n", padx=10, pady=10)
btn_Buscar.config(font="Helvetica")

txt_Buscar = Entry(frame)       #x=691
txt_Buscar.grid(row=1, column=3, padx=10, pady=10, sticky="n")
txt_Buscar.config(justify="center")

btn_Share = Button(frame, text="Share", command=funcionBotonShare,  width=36, height=1)
btn_Share.place(x=691, y=100)
btn_Share.config(font="Helvetica")

lbl_Apariciones = Label(frame, text="Personaje con más frases: ")
lbl_Apariciones.grid(row=1, column=2, padx=10, pady=10, sticky="s")
lbl_Apariciones.config(font="Helvetica")



#Programa principal
root.mainloop()
