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
from xml.etree import ElementTree

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

def graba(nomArchGrabar, raiz):
    """
    Función: Graba el nombre del archivo.
    Entradas: nomArchGrabar(str) Nombre que se le pondrá al archivo, raiz()
    Salidas: NA
    """
    try:
        archivo = open(nomArchGrabar, 'a')
        archivo.write(ElementTree.tostring(raiz, encoding='utf-8').decode('utf-8'))
        archivo.close()
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

    fecha = time.strftime("%d-%m-%Y-%H-%M-%S")
    fecha = fecha + ".xml"
    return fecha

def obtenerPersonajeMasFrases(pMayorCantidadFrases):
    codigosPersonaje = list(dicc.keys())
    mayorCantidadFrases = pMayorCantidadFrases
    for codigo in codigosPersonaje:
        cantidadFrases = dicc[codigo]
        if cantidadFrases > mayorCantidadFrases:
            mayorCantidadFrases = cantidadFrases
            for dato in listaMatriz:
                if codigo == dato[3]:
                    nombrePersonaje = dato[0]
                    break
    print(nombrePersonaje)
    return nombrePersonaje

def generarDiccionario(nombre):
    for dato in listaMatriz:
        if dato[0] == nombre:
            codigoPersonaje = dato[3]
            try:
                cantidadFrases = dicc[codigoPersonaje]
            except:
                cantidadFrases = 0
            cantidadFrases += 1
            dicc[codigoPersonaje] = cantidadFrases
            #print(dicc)
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
    listbox_Frases.config(state="normal")
    listbox_Frases.delete(0, END) #Refrescar
    contador = 0
    for personaje in listaMatriz:
        for frase in personaje[1]:
            contador += 1
            listbox_Frases.insert(contador, "Código " + personaje[3] + " Frase: " + frase + ". Personaje: "
                                  + personaje[0] + "\n")
            contador += 1
            listbox_Frases.insert(contador, "\n")

    listbox_Frases.config(state="disabled")

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

        if cantidad > 50 or cantidad < 1:
            return popupmsg("La cantidad de frases debe ser menor o igual a 50 y mayor o igual a 1.")
    except:
        return popupmsg("La cantidad debe ser un número entero.")

    for cant in range(cantidad):

        r = request("GET", "http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote")
        json_body = r.json()

        id = json_body["id"]
        frase = json_body["starWarsQuote"]
        nombre = separarNombre(frase)
        frase = obtenerFrase(frase, nombre)
        if not verificarFrase(id):
            generarMatriz(id, frase, nombre)
        else:
            print("personaje: " + nombre + " frase repetida " + frase)

        generarDiccionario(nombre)

    print(dicc)
    mostrarFrases()

    personaje = obtenerPersonajeMasFrases(mayorCantidadFrases)
    lbl_Apariciones.config(text="Personaje con más frases: " + personaje)


def funcionBotonShare():
    if comprobarConexion():
        generarXML()
    else:
        popupmsg("No hay conexión a Internet.")

def enviarCorreo():
    print("")

def generarXML():
    raiz = ElementTree.Element('personajes')
    for personajeMatriz in listaMatriz:

        # Crear estructura del XML
        personaje = ElementTree.SubElement(raiz, 'personaje')
        autor = ElementTree.SubElement(personaje, 'autor')

        for frasePersonaje in personajeMatriz[1]:
            for id in personajeMatriz[2]:
                frase = ElementTree.SubElement(personaje, 'frase')
                texto = ElementTree.SubElement(frase, 'texto')
                idFrase = ElementTree.SubElement(frase, 'id')

                texto.text = frasePersonaje
                idFrase.text = str(id)

        codigo = ElementTree.SubElement(personaje, 'codigo')

        autor.text = personajeMatriz[0]
        codigo.text = personajeMatriz[3]

    graba("backUp.xml", raiz)

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

# Creación label del título
lbl_Titulo = Label(frame, text="Frases de Star Wars")
lbl_Titulo.grid(row=0, column=0, padx=10, pady=10, sticky="n")
lbl_Titulo.config(font="Helvetica")

# Creación listbox
listbox_Frases = Listbox(frame, height=25, width=105)
listbox_Frases.grid(row=1, column=0, padx=10, pady=10)
listbox_Frases.config(state="disabled")

#Creación scroll bar vertical del listbox
scrollVertical = Scrollbar(frame, orient=VERTICAL, command=listbox_Frases.yview)
scrollVertical.grid(row=1, column=1, sticky='nsew')
listbox_Frases['yscrollcommand'] = scrollVertical.set

#Creación scroll bar horizontal del listbox
scrollHorizontal = Scrollbar(frame, orient=HORIZONTAL, command=listbox_Frases.xview)
scrollHorizontal.grid(row=2, column=0, sticky='nsew')
listbox_Frases['xscrollcommand'] = scrollHorizontal.set

#Creación Entry buscar
txt_Buscar = Entry(frame)  # x=681
txt_Buscar.grid(row=1, column=3, padx=10, pady=10, sticky="n")
txt_Buscar.config(justify="center")


#Creación botón share
btn_Share = Button(frame, text="Share", command=funcionBotonShare, width=36, height=1)
btn_Share.place(x=681, y=100)
btn_Share.config(font="Helvetica")

#Creación label apariciones
lbl_Apariciones = Label(frame, text="Personaje con más frases: ")
lbl_Apariciones.place(x=681, y=425)
lbl_Apariciones.config(font="Helvetica")


#Creación botón buscar
btn_Buscar = Button(frame, text="Buscar", command=funcionBotonBuscar, width=20, height=1)
btn_Buscar.grid(row=1, column=2, sticky="n", padx=10, pady=10)
btn_Buscar.config(font="Helvetica")

# Programa principal
root.mainloop()
