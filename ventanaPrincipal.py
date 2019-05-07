# Realizado por: Brayan Steven Marín Quirós y Ronny Jiménez Bonilla
# Fecha de creación: 02/04/2019 10:00am
# Última modificación: 02/04/2019 11:20pm
# Versión: 3.7.2

# Importación de funciones

from json import *
from requests import *
from tkinter import *


# Definición de fuciones

def generarMatiz(id, frase, nombre):
    for fila in listaMatriz:
        if fila[0] == nombre:
            fila[1].append(frase)
            fila[2].append(id)
            return ""
    nuevoPersonaje = []
    nuevoPersonaje.append(nombre)
    nuevoPersonaje.append([frase])
    nuevoPersonaje.append([id])
    nuevoPersonaje.append("123")
    listaMatriz.append(nuevoPersonaje)


def verificarFrase(id):
    for fila in listaMatriz:
        if id in fila[2]:
            return True
    return False


def separarNombre(frase):
    largo = len(frase) - 1
    for i in range(largo, 0, -1):
        if frase[i] == "-" or frase[i] == "?" or frase[i] == "—":
            nombre = frase[i + 2:]
            return nombre

def mostrarFrases():
    txt_Area.config(state="normal")
    txt_Area.delete('1.0', END)

    for personaje in listaMatriz:
        txt_Area.insert(INSERT, str(personaje) + "\n")
        txt_Area.insert(INSERT, "\n ")

    txt_Area.config(state="disabled")

def funcionBotonBuscar():
    cantidad = txt_Buscar.get()

    try:
        cantidad = int(cantidad)
    except:
        return ""

    for cant in range(cantidad):

        r = request("GET", "http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote")
        json_body = r.json()

        id = json_body["id"]
        frase = json_body["starWarsQuote"]
        nombre = separarNombre(frase)
        frase = frase[:len(frase) - len(nombre)]

        if not verificarFrase(id):
            generarMatiz(id, frase, nombre)

    mostrarFrases()



def funcionBotonShare():
    print("")


# Variables globales
listaMatriz = []

# Creación de la ventana
root = Tk()

# Propiedades de la ventana
root.title("Ventana principal")
root.iconbitmap("imagenes/icon.ico")
root.resizable(0, 0)

# Creación frame
frame = Frame()
frame.pack()
frame.config(width=800, height=600)

# Creación del título
lbl_Titulo = Label(frame, text="Frases de Star Wars")
lbl_Titulo.grid(row=0, column=0, padx=10, pady=10, sticky="n")
lbl_Titulo.config(font="Helvetica")

# Creación text area

txt_Area = Text(frame, wrap=NONE)
txt_Area.grid(row=1, column=0, padx=10, pady=10)
txt_Area.config(state="disabled")

scrollVertical = Scrollbar(frame, command=txt_Area.yview())
scrollVertical.grid(row=1, column=1, sticky="ns")
txt_Area['yscrollcommand'] = scrollVertical.set

scrollHorizontal = Scrollbar(frame, orient=HORIZONTAL)
scrollHorizontal.grid(row=2, column=0, sticky="news")
txt_Area['xscrollcommand'] = scrollHorizontal.set

# Creación widgets

txt_Buscar = Entry(frame)  # x=691
txt_Buscar.grid(row=1, column=3, padx=10, pady=10, sticky="n")
txt_Buscar.config(justify="center")

btn_Share = Button(frame, text="Share", command=funcionBotonShare, width=36, height=1)
btn_Share.place(x=691, y=100)
btn_Share.config(font="Helvetica")

lbl_Apariciones = Label(frame, text="Personaje con más frases: ")
lbl_Apariciones.grid(row=1, column=2, padx=10, pady=10, sticky="s")
lbl_Apariciones.config(font="Helvetica")

btn_Buscar = Button(frame, text="Buscar", command=funcionBotonBuscar, width=20, height=1)
btn_Buscar.grid(row=1, column=2, sticky="n", padx=10, pady=10)
btn_Buscar.config(font="Helvetica")

# Programa principal
root.mainloop()