# Realizado por: Brayan Steven Marín Quirós y Ronny Jiménez Bonilla
# Fecha de creación: 02/05/2019 10:00am
# Última modificación: 13/05/2019 10:30pm
# Versión: 3.7.2

# Importación de funciones
from socket import gethostbyname, create_connection, error
from tkinter.messagebox import showinfo, showerror
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from xml.etree import ElementTree
from email import encoders
from tkinter import ttk
from requests import *
from tkinter import *
import tkinter as tk
import smtplib
import time
import os

# Variables globales
archivoBackUp = "backUp.xml"
directorio = []
dicc = {}
mayorCantidadFrases = 0
listaMatriz = []  # Lista que contiene las frases buscadas
listaFrasesSeleccionadas = []  # Lista que contiene las frases seleccionadas
frasesCorreo = []  # Lista que contiene las que serán enviadas por correo


# Definición de funciones
def graba(nomArchGrabar, raiz):
    """
    Función: Graba el nombre del archivo.
    Entradas: nomArchGrabar(str) Nombre que se le pondrá al archivo, raiz(obj) Raiz que tiene la información del xml
    Salidas: NA
    """
    try:
        archivo = open(nomArchGrabar, 'w')
        archivo.write(ElementTree.tostring(raiz, encoding='utf-8').decode('utf-8'))
        archivo.close()
    except:
        print("\nError al grabar el archivo: \n", nomArchGrabar)


def generarMatriz(id, frase, nombre, codigoAplicacion="", correo=False):
    """
    Función: Genera la matriz principal
    Entradas: id(int) Id de la frase, frase(str) Frase dada, nombre(str) Nombre del personaje,
     codigoAplicacion(str)Codigo de cada personaje, correo(bool) Bandera que indica si creará una matriz para enviar por
     correo o si es una matriz para imprimir en pantalla
    Salidas: Crea la matriz y retorna ""
    """
    if not correo:
        for fila in listaMatriz:
            if fila[0] == nombre:
                fila[1].append(frase)
                fila[2].append(id)
                return ""
    else:
        for fila in frasesCorreo:
            if fila[0] == nombre:
                fila[1].append(frase)
                fila[2].append(id)
                return ""

    nuevoPersonaje = []
    nuevoPersonaje.append(nombre)
    nuevoPersonaje.append([frase])
    nuevoPersonaje.append([id])
    if codigoAplicacion == "":
        codigoAplicacion = generarCodigoAplicacion(nombre)
    nuevoPersonaje.append(codigoAplicacion)

    # Agrega toda la información del personaje a la matriz
    if not correo:
        listaMatriz.append(nuevoPersonaje)
    else:
        frasesCorreo.append(nuevoPersonaje)

    return ""


def generarCodigoContador(num):
    """
    Función: Genera el código que contiene el contador de los personajes
    Entradas: num(int) Número que lleva el contador de personajes
    Salidas: retorna codigo
    """
    if num <= 9:
        codigo = "00" + str(num)
    elif num <= 99:
        codigo = "0" + str(num)
    elif num >= 100:
        codigo = str(num)

    return codigo


def generarCodigoAplicacion(nombre):
    """
    Función: Genera el código de cada personaje
    Entradas: nombre(str) Nombre del personaje
    Salidas: retorna codigo
    """
    ultimaLetra = len(nombre) - 1
    serial = generarCodigoContador(len(listaMatriz) + 1)
    codigo = "#" + nombre[0] + serial + "-" + nombre[ultimaLetra].upper()
    return codigo


def obtenerPersonajeMasFrases(pMayorCantidadFrases):
    """
    Función: Obtiene el personaje con más frases
    Entradas: pMayorCantidadFrases(int) variable que almacena la mayor cantidad de frases encontrada en el diccionario
    Salidas:
    """
    codigosPersonaje = list(dicc.keys())
    mayorCantidadFrases = pMayorCantidadFrases
    for codigo in codigosPersonaje:
        cantidadFrases = dicc[codigo]
        if cantidadFrases >= mayorCantidadFrases:
            mayorCantidadFrases = cantidadFrases
            for dato in listaMatriz:
                if codigo == dato[3]:
                    nombrePersonaje = dato[0]
                    break
    return nombrePersonaje


def comprobarConexion():
    """
    Función: Comprueba si hay conexión a Internet
    Entradas: NA
    Salidas: retorna True si se puede establecer la conexión, sino retorna false
    """
    try:
        gethostbyname("google.com")
        conexion = create_connection(("google.com", 80), 1)
        conexion.close()
        return True
    except error:
        return False


def generarNombreArchivo():
    """
    Función: Genera el nombre del archivo según la fecha y hora actual
    Entradas: NA
    Salidas: retorna nombreArchivo
    """
    nombreArchivo = time.strftime("%d-%m-%Y-%H-%M-%S")
    nombreArchivo = "\share-" + nombreArchivo + ".xml"
    return nombreArchivo


def generarDiccionario(nombre):
    """
    Función: Genera el diccionario con el código de los personajes y la cantidad de llamadas del API
    Entradas: nombre(str) Nombre del personaje
    Salidas: retorna dicc
    """
    for dato in listaMatriz:
        if dato[0] == nombre:
            codigoPersonaje = dato[3]
            try:
                cantidadFrases = dicc[codigoPersonaje]
            except:
                cantidadFrases = 0
            cantidadFrases += 1
            dicc[codigoPersonaje] = cantidadFrases
            return dicc


def verificarFrase(id):
    """
    Función: Verifica que la frase no esté guardada
    Entradas: id(int) Id de la frase
    Salidas: retorna True si la frase está, sino retorna False
    """
    for fila in listaMatriz:
        if id in fila[2]:
            return True
    return False


def separarNombre(frase):
    """
    Función: Separa el nombre del personaje de la frase
    Entradas: frase(str) Frase enviada por el API
    Salidas: retorna el nombre del personaje
    """
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
            elif nombre == "Padmé Amidala":
                nombre = "Padme Amidala"
            elif nombre == "Chirrut Îmwe":
                nombre = "Chirrut Imwe"

            return nombre
    return "Error"


def obtenerFrase(frase, nombre):
    """
    Función: Obtiene la frase del aPI
    Entradas: frase(str) Frase enviada por el API, nombre(str) Nombre del personaje
    Salidas: retorna la fraseFinal
    """
    if not nombre == "Riyo Chuchi":  # Es la excepción porque incluye el episodio
        frase = frase[:(len(frase) - len(nombre)) - 3]
    else:
        frase = frase[:(len(frase) - len(nombre)) - 38]

    fraseFinal = ""
    for caracter in frase:
        if caracter == "’":
            caracter = "'"
        elif caracter == "…":
            caracter = "..."
        elif caracter == "—":
            caracter = "-"
        fraseFinal += caracter

    return fraseFinal


def separarFrasesSeleccionadas(frase):
    """
    Función: Separa las frases seleccionadas en el listbox para obtener una lista con la frase y el personaje
    Entradas: frase(str) Frase obtenida del listbox
    Salidas: Agrega la frase y el personaje a listaFrasesSeleccionadas respectivamente y retorna ""
    """
    frase = frase[22:]
    listaDividir = frase.split(" Personaje: ")
    listaFrasesSeleccionadas.append(listaDividir)
    return ""


def generarListaEnviarCorreo():
    """
    Función: Genera la lista para enviar por correo
    Entradas: NA
    Salidas: Genera la matriz que creará el archivo XML para enviar por correo y retorna ""
    """
    for fraseSelecionada in listaFrasesSeleccionadas:
        personaje = fraseSelecionada[1]
        for fila in listaMatriz:
            if fila[0] == personaje:
                fraseSeleccion = fraseSelecionada[0]
                for frase in fila[1]:
                    if fraseSeleccion == frase:
                        id = fila[1].index(frase)
                        id = fila[2][id]
                        generarMatriz(id, frase, personaje, fila[3], correo=True)
    return ""


def mostrarDesarrolladores():
    """
    Función: Muestra una ventana emergente con la información de los desarrolladores.
    Entradas: NA
    Salidas: Retorna ""
    """
    showinfo("Desarrolladores", "Realizado por Ronny Jiménez Bonilla y Brayan Marín Quirós.")
    return ""


def abrirManualUsuario():
    """
    Función: Muestra el manual de usuario de la aplicación.
    Entradas: NA
    Salidas: Retorna ""
    """
    os.popen("Manual_usuario\manual_de_usuario_frases.pdf")
    return ""
