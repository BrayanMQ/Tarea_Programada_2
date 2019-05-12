# Realizado por: Brayan Steven Marín Quirós y Ronny Jiménez Bonilla
# Fecha de creación: 02/04/2019 10:00am
# Última modificación: 02/04/2019 11:20pm
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

#Variables globales
archivoBackUp = "backUp.xml"
archivoCorreo = ""
dicc = {}
mayorCantidadFrases = 0
listaMatriz = []
listaFrasesSeleccionadas = []
frasesCorreo = []

# Definición de fuciones
def cargarBackUp(raiz):
    for personaje in raiz:
        autor = personaje.find("autor").text
        codigoApp = personaje.find("codigo").text
        cantApariciones = personaje.find("cantApariciones").text
        dicc[codigoApp] = int(cantApariciones)
        for frases in personaje.findall("frase"):
            frase = frases.find("texto").text
            idFrase = frases.find("id").text
            generarMatriz(idFrase, frase, autor, codigoApp)
            #generarDiccionario(autor)

    print(dicc)
    mostrarFrases()

    personaje = obtenerPersonajeMasFrases(mayorCantidadFrases)
    lbl_Apariciones.config(text="Personaje con más frases: " + personaje)
    return ""


def graba(nomArchGrabar, raiz):
    """
    Función: Graba el nombre del archivo.
    Entradas: nomArchGrabar(str) Nombre que se le pondrá al archivo, raiz()
    Salidas: NA
    """
    try:
        archivo = open(nomArchGrabar, 'wt')
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

    try:
        tree = ElementTree.parse(nomArchLeer)
        raiz = tree.getroot()
        cargarBackUp(raiz)
        showinfo("Back up", "Se cargó con éxito el back up.")
    except:
        showinfo("Back up", "No se ha encontrado un archivo back up.")


def mostrarFrases():
    listbox_Frases.config(state="normal")
    listbox_Frases.delete(0, END) #Refrescar
    contador = 0
    for personaje in listaMatriz:
        for frase in personaje[1]:
            contador += 1
            listbox_Frases.insert(contador, "Código " + personaje[3] + " Frase: " + frase + " Personaje: "
                                  + personaje[0])
    listbox_Frases.config(state="disabled")


def comprobarConexion():
    try:
        gethostbyname("google.com")
        conexion = create_connection(("google.com", 80), 1)
        conexion.close()
        return True
    except error:
        return False


def generarNombreArchivo():

    nombreArchivo = time.strftime("%d-%m-%Y-%H-%M-%S")
    nombreArchivo = nombreArchivo + ".xml"
    return nombreArchivo


def obtenerPersonajeMasFrases(pMayorCantidadFrases):
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

def generarCodigoContador(num):

    if num <= 9:
        codigo = "00" + str(num)
    elif num <= 99:
        codigo = "0" + str(num)
    elif num >= 100:
        codigo = str(num)

    return codigo

def generarCodigoAplicacion(nombre):
    ultimaLetra = len(nombre)-1
    serial = generarCodigoContador(len(listaMatriz)+1)
    codigo = "#" + nombre[0] + serial + "-" + nombre[ultimaLetra].upper()
    return codigo

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
            elif nombre == "Padmé Amidala":
                nombre = "Padme Amidala"
            elif nombre == "Chirrut Îmwe":
                nombre = "Chirrut Imwe"

            return nombre
    return "Error"

def generarMatriz(id, frase, nombre, codigoAplicacion="", correo=False):
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

def obtenerFrase(frase, nombre):
    if not nombre == "Riyo Chuchi": #Es la excepción porque incluye el episodio
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

def generarXML(pLista):
    raiz = ElementTree.Element('personajes')
    for personajeMatriz in pLista:
        # Crear estructura del XML
        personaje = ElementTree.SubElement(raiz, 'personaje')
        autor = ElementTree.SubElement(personaje, 'autor')
        contador = 0

        for frasePersonaje in personajeMatriz[1]:

            frase = ElementTree.SubElement(personaje, 'frase')
            texto = ElementTree.SubElement(frase, 'texto')
            idFrase = ElementTree.SubElement(frase, 'id')

            texto.text = frasePersonaje
            idFrase.text = str(personajeMatriz[2][contador])
            contador += 1
        codigo = ElementTree.SubElement(personaje, 'codigo')
        cantApariciones = ElementTree.SubElement(personaje, 'cantApariciones')
        autor.text = personajeMatriz[0]
        codigo.text = personajeMatriz[3]
        cantApariciones.text = str(dicc[personajeMatriz[3]])

    archivoCorreo = generarNombreArchivo()
    graba(archivoCorreo, raiz)

def enviarCorreo(remitente, contrasenna, destinatarios, asunto, cuerpo, nombreArchivo):

    # Iniciamos los parámetros del script
    ruta_adjunto = nombreArchivo  # Lugar donde se encuentra el archivo
    nombre_adjunto = nombreArchivo   # Nombre del archivo que se enviará


    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()

    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = destinatarios
    mensaje['Subject'] = asunto

    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_adjunto, 'rb')

    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload(archivo_adjunto.read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)

    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)

    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    try:
        sesion_smtp.login(remitente, contrasenna)
    except:
        showerror("Error", "No se pudo iniciar sesión.")
        return ""
    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    try:
        sesion_smtp.sendmail(remitente, destinatarios, texto)
        showinfo("Éxito", "Se ha enviado el correo con éxito")
    except:
        showerror("Error", "No se pudo enviar el mensaje.")

    # Cerramos la conexión
    sesion_smtp.quit()

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Información")
    label = ttk.Label(popup, text=msg, font="Helvetica")
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()

def pantallaNuevoCorreo(correo, contrasenna):

    ventanaCorreoNuevo = Toplevel()
    ventanaCorreoNuevo.title("Correo nuevo")
    ventanaCorreoNuevo.geometry("400x400+750+300")
    ventanaCorreoNuevo.resizable(0, 0)
    ventanaCorreoNuevo.iconbitmap("imagenes/candado.ico")

    et = StringVar()
    es = StringVar()
    Label(ventanaCorreoNuevo, text="De: %s" % correo).grid(row=0, column=0, sticky=NSEW)

    Label(ventanaCorreoNuevo, text="Para:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
    txt_Para = Entry(ventanaCorreoNuevo, textvariable=et, width=25)
    txt_Para.grid(row=1, column=1, padx=10, pady=10, sticky=E)

    Label(ventanaCorreoNuevo, text="Asunto:").grid(row=2, column=0, sticky=W)
    txt_Asunto = Entry(ventanaCorreoNuevo, textvariable=es, width=25)
    txt_Asunto.grid(row=2, column=1, padx=10, pady=10, sticky=E)

    Label(ventanaCorreoNuevo, text="Mensaje:").grid(row=3, column=0, sticky=W)
    txt_Mensaje = Text(ventanaCorreoNuevo, width=25, height=5)
    txt_Mensaje.grid(row=3, column=1, padx=10, pady=10, sticky=E)

    def enviar():
        enviarCorreo(correo, contrasenna,
                     destinatarios=txt_Para.get(),
                     asunto=txt_Asunto.get(),
                     cuerpo=txt_Mensaje.get("1.0", "end-1c"),
                     nombreArchivo=archivoCorreo)
        return ""

    btn_Enviar = Button(ventanaCorreoNuevo, text="Enviar", command=enviar)
    btn_Enviar.grid(row=4, column=0, sticky=NSEW)

    salir = Button(ventanaCorreoNuevo, text="Salir", command=ventanaCorreoNuevo.quit)
    salir.grid(row=4, column=1, sticky=NSEW)

def pantallaLogin():

    ventanaIniciarSesion = Toplevel(root)
    ventanaIniciarSesion.title("Iniciar sesión")
    ventanaIniciarSesion.geometry("300x250+750+300")
    ventanaIniciarSesion.resizable(0, 0)
    ventanaIniciarSesion.iconbitmap("imagenes/candado.ico")

    Label(ventanaIniciarSesion, text="Por favor ingrese sus datos para iniciar sesión.").pack()
    Label(ventanaIniciarSesion, text="").pack()

    username_verify = StringVar()
    password_verify = StringVar()

    Label(ventanaIniciarSesion, text="Usuario").pack()

    txt_Usuario = Entry(ventanaIniciarSesion, textvariable=username_verify)
    txt_Usuario.pack()

    Label(ventanaIniciarSesion, text="").pack()
    Label(ventanaIniciarSesion, text="Contraseña").pack()

    txt_Contrasenna = Entry(ventanaIniciarSesion, textvariable=password_verify, show='*')
    txt_Contrasenna.pack()

    Label(ventanaIniciarSesion, text="").pack()

    def funcionBotonIniciarSesion():
        correo = txt_Usuario.get().lower()
        contrasenna = txt_Contrasenna.get()

        #Comprobar que los espacios estén llenos
        if correo == "":
            showerror("Error", "El espacio correo no puede estar vacío.")
            return pantallaLogin()
        elif contrasenna == "":
            showerror("Error", "La espacio contraseña no puede estar vacío.")
            return pantallaLogin()

        # Creamos la conexión con el servidor
        sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)

        # Ciframos la conexión
        sesion_smtp.starttls()

        # Iniciamos sesión en el servidor
        try:
            sesion_smtp.login(correo, contrasenna)
            showinfo("Éxito", "Se ha iniciado sesión")
            return pantallaNuevoCorreo(correo, contrasenna)
        except:
            showerror("Error", "No se pudo iniciar sesión con la cuenta: " + correo)
            return pantallaLogin()

    Button(ventanaIniciarSesion, text="Iniciar sesión", width=10, height=1, command=funcionBotonIniciarSesion).pack()


def funcionBotonBuscar():
    cantidad = txt_Buscar.get()

    try:

        cantidad = int(cantidad)

        if cantidad > 50 or cantidad < 1:
            return showerror("Error", "La cantidad de frases debe ser menor o igual a 50 y mayor o igual a 1.")



    except:
        return showerror("Error", "La cantidad de frases debe ser un número entero.")

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

def separarFrasesSeleccionadas(frase):
    frase = frase[22:]
    listaDividir = frase.split(" Personaje: ")
    listaFrasesSeleccionadas.append(listaDividir)

def generarListaEnviarCorreo():

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
    print(frasesCorreo)

def funcionBotonEnviarCorreo():
    frasesSeleccionadas = listbox_Frases.curselection()
    if not len(frasesSeleccionadas) == 0:
        for frase in frasesSeleccionadas:
            separarFrasesSeleccionadas(listbox_Frases.get(frase, last=None))
        generarListaEnviarCorreo()
        generarXML(frasesCorreo)
        pantallaLogin()
    else:
        showerror("Error", "Debe seleccionar al menos una frase.")

def funcionBotonShare():
    if comprobarConexion():
        showinfo("Información", "Seleccione las frases que desee compartir.")

        btn_EnviarCorreo = Button(frame, text="Enviar correo", command=funcionBotonEnviarCorreo, width=36, height=1)
        btn_EnviarCorreo.place(x=681, y=300)
        btn_EnviarCorreo.config(font="Helvetica")

        listbox_Frases.config(state="normal", selectmode=MULTIPLE)


    else:
        showerror("Error", "No hay conexión a Internet.")


# Creación de la ventana
root = Tk()

# Propiedades de la ventana
root.title("Ventana principal")
root.iconbitmap("imagenes/icon.ico")
root.geometry("+400+200")
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

lee(archivoBackUp)

#Inicio de la ventana
root.mainloop()

