# Realizado por: Brayan Steven Marín Quirós y Ronny Jiménez Bonilla
# Fecha de creación: 02/04/2019 10:00am
# Última modificación: 02/04/2019 11:20pm
# Versión: 3.7.2

# Importación de funciones

from socket import gethostbyname, create_connection, error

import pickle
from json import *
from requests import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
import time


#Variables globales
archivoBackUp = "BackUp.xml"
listaMatriz = []
dicc = {}
mayorCantidadFrases = 0

# Definición de fuciones

def comprobarConexion():
    try:
        gethostbyname("google.com")
        conexion = create_connection(("google.com", 80), 1)
        conexion.close()
        return True
    except error:
        return False

def graba(nomArchGrabar, lista):
    """
    Función: Graba el nombre del archivo.
    Entradas: nomArchGrabar(str) Nombre que se le pondrá al archivo, lista(list) Lista que se guardará
    Salidas: NA
    """
    try:
        f = open(nomArchGrabar, "wb")
        pickle.dump(lista, f)
        f.close()
    except:
        print("\nError al grabar el archivo: \n", nomArchGrabar)


def lee(nomArchLeer):
    """
    Función: Lee el archivo "canciones"
    Entradas: nomArchLeer(string) Es el nombre del archivo
    Salidas: Retorna lista
    """
    lista = []
    try:
        f = open(nomArchLeer, "rb")
        lista = pickle.load(f)
        f.close()
    except:
        print(
            "\nError al leer el archivo: " + nomArchLeer + ". Cuando se guarde una nueva persona, el archivo se creará"
                                                           " automáticamente.")
    return lista


def obtenerNombreArchivo():

    fecha = time.strftime("%d-%m-%Y-%I-%M-%S")
    fecha = fecha + ".xml"
    return fecha

def obtenerPersonajeMasFrases(diccPersonajes, listaMatriz, pMayorCantidadFrases):
    codigosPersonaje = list(diccPersonajes.keys())
    mayorCantidadFrases = pMayorCantidadFrases
    for codigo in codigosPersonaje:
        cantidadFrases = diccPersonajes[codigo]
        if cantidadFrases > mayorCantidadFrases:
            mayorCantidadFrases = cantidadFrases
            for dato in listaMatriz:
                if codigo == dato[3]:
                    nombrePersonaje = dato[0]
                    break
    print(nombrePersonaje)
    return nombrePersonaje

def generarDiccionario(listaMatriz):
    for datos in listaMatriz:
        codigoPersonaje = datos[3]
        cantidadFrases = len(datos[2])
        dicc[codigoPersonaje] = cantidadFrases

    print(dicc)
    return dicc

def generarCodigoAplicacion(nombre):
    ultimaLetra = len(nombre)-1
    serial = generarCodigoContador(len(listaMatriz)+1)
    codigo = "#" + nombre[0] + serial + "-" + nombre[ultimaLetra].upper()
    return codigo

def generarMatriz(id, frase, nombre):

    for fila in listaMatriz:
        if fila[0] == nombre:
            fila[1].append(frase)
            fila[2].append(id)
            return ""

    nuevoPersonaje = []
    nuevoPersonaje.append(nombre)
    nuevoPersonaje.append([frase])
    nuevoPersonaje.append([id])
    codigoAplicacion = generarCodigoAplicacion(nombre)
    nuevoPersonaje.append(codigoAplicacion)



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
            if nombre == "on Jinn":
                nombre = "Qui-Gon Jinn"
            elif nombre == "PO":
                nombre = "C-3PO"
            elif nombre == "an Kenobi":
                nombre = "Obi-Wan Kenobi"
            elif nombre == "SO":
                nombre = "K-2SO"
            elif nombre == "Riyo Chuchi (Season One, Episode 15, Trespass)":
                nombre = "Riyo Chuchi"

            return nombre
    return "Error"

def mostrarFrases():
    txt_Area.config(state="normal")
    txt_Area.delete('1.0', END)

    for personaje in listaMatriz:
        if len(personaje[1]) == 1:
            frase = personaje[1][0]
            txt_Area.insert(INSERT, "Código " + personaje[3] + " Frase: " + frase + ". Personaje: "
                            + personaje[0] + "\n")
            txt_Area.insert(INSERT, "\n")
        else:
            for frase in personaje[1]:
                txt_Area.insert(INSERT, "Código " + personaje[3] + " Frase: " + frase + ". Personaje: "
                                + personaje[0] + "\n")
                txt_Area.insert(INSERT, "\n")


    txt_Area.config(state="disabled")

def generarCodigoContador(num):

    if num <= 9:
        codigo = "00" + str(num)
    elif num <= 99:
        codigo = "0" + str(num)
    elif num >= 100:
        codigo = str(num)

    return codigo

def obtenerFrase(frase, nombre):
    if not nombre == "Riyo Chuchi": #Es la excepción porque incluye el episodio
        frase = frase[:(len(frase) - len(nombre)) - 3]
    else:
        frase = frase[:(len(frase) - len(nombre)) - 38]

    return frase

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font="Helvetica")
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def funcionBotonBuscar():
    cantidad = txt_Buscar.get()

    try:
        cantidad = int(cantidad)

        if cantidad > 50:
            return popupmsg("Error")
    except:
        return ""

    for cant in range(cantidad):

        r = request("GET", "http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote")
        json_body = r.json()

        id = json_body["id"]
        frase = json_body["starWarsQuote"]
        nombre = separarNombre(frase)
        frase = obtenerFrase(frase, nombre)

        if not verificarFrase(id):
            generarMatriz(id, frase, nombre)

    mostrarFrases()
    diccPersonajes = generarDiccionario(listaMatriz)

    personaje = obtenerPersonajeMasFrases(diccPersonajes, listaMatriz, mayorCantidadFrases)
    lbl_Apariciones.config(text="Personaje con más frases: " + personaje)


def funcionBotonShare():
    if comprobarConexion():
        enviarCorreo()
    else:
        popupmsg("No hay conexión a Internet.")

def enviarCorreo():
    print("")

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

scrollVertical = Scrollbar(frame, orient=VERTICAL, command=txt_Area.yview)
scrollVertical.grid(row=1, column=1, sticky='nsew')
txt_Area['yscrollcommand'] = scrollVertical.set

scrollHorizontal = Scrollbar(frame, orient=HORIZONTAL, command=txt_Area.xview)
scrollHorizontal.grid(row=2, column=0, sticky='nsew')
txt_Area['xscrollcommand'] = scrollHorizontal.set

# Creación widgets

txt_Buscar = Entry(frame)  # x=691
txt_Buscar.grid(row=1, column=3, padx=10, pady=10, sticky="n")
txt_Buscar.config(justify="center")

btn_Share = Button(frame, text="Share", command=funcionBotonShare, width=36, height=1)
btn_Share.place(x=691, y=100)
btn_Share.config(font="Helvetica")

lbl_Apariciones = Label(frame, text="Personaje con más frases: ")
lbl_Apariciones.place(x=691, y=425)
lbl_Apariciones.config(font="Helvetica")

btn_Buscar = Button(frame, text="Buscar", command=funcionBotonBuscar, width=20, height=1)
btn_Buscar.grid(row=1, column=2, sticky="n", padx=10, pady=10)
btn_Buscar.config(font="Helvetica")

# Programa principal
root.mainloop()
