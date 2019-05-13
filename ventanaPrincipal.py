# Realizado por: Brayan Steven Marín Quirós y Ronny Jiménez Bonilla
# Fecha de creación: 02/04/2019 10:00am
# Última modificación: 02/04/2019 11:20pm
# Versión: 3.7.2

# Importación de funciones
from funciones import *

# Definición de fuciones
def cargarBackUp(raiz):
    """
    Función: Carga el archivo backUp en caso de existir
    Entradas: raiz(obj) Raiz que tiene la información del xml
    Salidas: Carga el backup y retorna ""
    """
    for personaje in raiz:
        autor = personaje.find("autor").text
        codigoApp = personaje.find("codigo").text
        cantApariciones = personaje.find("cantApariciones").text
        dicc[codigoApp] = int(cantApariciones)
        for frases in personaje.findall("frase"):
            frase = frases.find("texto").text
            idFrase = frases.find("id").text
            generarMatriz(idFrase, frase, autor, codigoApp)
    mostrarFrases()

    personaje = obtenerPersonajeMasFrases(mayorCantidadFrases)
    lbl_Apariciones.config(text="Personaje con más frases: " + personaje)
    return ""


def lee(nomArchLeer):
    """
    Función: Lee el archivo "backUp.xml"
    Entradas: nomArchLeer(string) Es el nombre del archivo
    Salidas: Llama a cargarBackUp y muestra un mensaje según lo ocurrido
    """

    try:
        tree = ElementTree.parse(nomArchLeer)
        raiz = tree.getroot()
        cargarBackUp(raiz)
        showinfo("Back up", "Se cargó con éxito el back up.")
    except:
        showinfo("Back up", "No se ha encontrado un archivo back up.")


def mostrarFrases():
    """
    Función: Muestra las frases en el listbox
    Entradas: NA
    Salidas: Muestra las frases en el listbox y retorna ""
    """
    listbox_Frases.config(state="normal")
    listbox_Frases.delete(0, END)  # Refrescar
    contador = 0
    for personaje in listaMatriz:
        for frase in personaje[1]:
            contador += 1
            listbox_Frases.insert(contador, "Código " + personaje[3] + " Frase: " + frase + " Personaje: "
                                  + personaje[0])
    listbox_Frases.config(state="disabled")
    return ""


def generarXML(pLista, backUp=False):
    """
    Función: Genera el archivo .xml
    Entradas: pLista(list) Lista que puede contener la información de la matriz principal o la información de la matriz
    que se enviará por correo, backUp(bool) Bandera que indica si se creará un xml para backUp o si será un xml para
    enviar por correo
    Salidas: Crea el archivo xml según lo especificado y retorna ""
    """
    if not len(pLista) == 0:
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

            try:
                os.mkdir("Archivos_correo")
            except:
                if backUp:
                    graba(archivoBackUp, raiz)
                else:
                    archivoCorreo = generarNombreArchivo()
                    file_Path = os.getcwd() + "\Archivos_correo" + archivoCorreo
                    archivoCorreo = archivoCorreo[1:]
                    directorio.append(file_Path)
                    directorio.append(archivoCorreo)
                    graba(directorio[0], raiz)
    else:
        showinfo("Error", "No hay frases por guardar.")
    return ""


def enviarCorreo(remitente, contrasenna, destinatarios, asunto, cuerpo):
    """
    Función: Envíar un correo con el archivo xml generado
    Entradas: remitente(str) Usuario que enviará el correo, contrasenna(str) Contraseña del usuario,
    destinatarios(list) Lista de destinatarios, asunto(str) Asunto del correo, cuerpo(str) Cuerpo del correo
    Salidas: Envía el correo y cierra la conexión
    """
    if comprobarConexion():

        # Iniciamos los parámetros del script
        ruta_adjunto = directorio[0]  # Lugar donde se encuentra el archivo
        nombre_adjunto = directorio[1]  # Nombre del archivo que se enviará

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
        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()

        # Enviamos el mensaje
        try:
            sesion_smtp.sendmail(remitente, destinatarios, texto)
            showinfo("Éxito", "Se ha enviado el correo a: " + destinatarios + " con éxito.")
        except:
            showerror("Error", "No se pudo enviar el mensaje a: " + destinatarios)
            mensaje = tk.messagebox.askquestion("Información", "¿Desea reintentar el envío?",icon="warning")
            if mensaje == 'yes':
                return pantallaNuevoCorreo(remitente, contrasenna)

        # Cerramos la conexión
        sesion_smtp.quit()
    else:
        showerror("Error", "No hay conexión a Internet.")


def popupmsg(msg):
    """
    Función:
    Entradas:
    Salidas:
    """
    popup = tk.Tk()
    popup.wm_title("Información")
    label = ttk.Label(popup, text=msg, font="Helvetica")
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def pantallaNuevoCorreo(correo, contrasenna):
    """
    Función: Inicia la pantalla para enviar un correo
    Entradas: correo(str) Correo del usuario, contrasenna(str) Contraseña del usuario
    Salidas: Se muestra la pantalla para enviar un correo
    """
    ventanaCorreoNuevo = Toplevel()
    ventanaCorreoNuevo.title("Correo nuevo")
    ventanaCorreoNuevo.geometry("490x280+750+300")
    ventanaCorreoNuevo.resizable(0, 0)
    ventanaCorreoNuevo.iconbitmap("imagenes/candado.ico")
    ventanaCorreoNuevo.config(bg="#5DA9F6")

    et = StringVar()
    es = StringVar()
    Label(ventanaCorreoNuevo, text="De: %s" % correo, bg="#5DA9F6", fg="white").grid(row=0, column=0, sticky=W)

    Label(ventanaCorreoNuevo, text="Para:", bg="#5DA9F6", fg="white").grid(row=1, column=0, sticky=W)
    txt_Para = Entry(ventanaCorreoNuevo, textvariable=et, width=25)
    txt_Para.grid(row=1, column=1, padx=10, pady=10, sticky=W)

    Label(ventanaCorreoNuevo, text="Asunto:", bg="#5DA9F6", fg="white").grid(row=2, column=0, sticky=W)
    txt_Asunto = Entry(ventanaCorreoNuevo, textvariable=es, width=25)
    txt_Asunto.grid(row=2, column=1, padx=10, pady=10, sticky=W)

    Label(ventanaCorreoNuevo, text="Mensaje:", bg="#5DA9F6", fg="white").grid(row=3, column=0, sticky=W)
    txt_Mensaje = Text(ventanaCorreoNuevo, width=25, height=5)
    txt_Mensaje.grid(row=3, column=1, padx=10, pady=10, sticky=W)

    lbl_archivo = Label(ventanaCorreoNuevo, text="Archivo adjunto: " + directorio[1])
    lbl_archivo.grid(row=4, column=0, sticky=W)
    lbl_archivo.config(bg="#5DA9F6", fg="white")

    def enviar():
        """
        Función: Envía el correo
        Entradas: NA
        Salidas: Envía el correo y cierra la ventana
        """
        if comprobarConexion():
            destinatarios = txt_Para.get()
            destinatarios = destinatarios.split(", " and ",")
            if destinatarios == "":
                showerror("Error", "El destinatario no puede estar vacío.")
                ventanaCorreoNuevo.destroy()
                return pantallaNuevoCorreo(correo, contrasenna)
            else:
                for destinatario in destinatarios:

                    enviarCorreo(correo, contrasenna,
                                 destinatario,
                                 asunto=txt_Asunto.get(),
                                 cuerpo=txt_Mensaje.get("1.0", "end-1c"))

                ventanaCorreoNuevo.destroy()
                activarMenuPrincipal()
        else:
            showerror("Error", "No hay conexión a Internet.")

    btn_Enviar = Button(ventanaCorreoNuevo, text="Enviar", command=enviar)
    btn_Enviar.grid(row=5, column=0, padx=10, pady=10, sticky=NSEW)
    btn_Enviar.config(font="Helvetica")

    def cerrarVentana():
        """
        Función: Activa los widgets del menú principal y cierra la ventaa
        Entradas: NA
        Salidas: NA
        """
        activarMenuPrincipal()
        ventanaCorreoNuevo.destroy()

    ventanaCorreoNuevo.protocol("WM_DELETE_WINDOW", cerrarVentana)


def pantallaLogin():
    """
    Función: Muestra la pantalla del login
    Entradas: Na
    Salidas: Muestra la pantalla del login
    """
    ventanaIniciarSesion = Toplevel(root)
    ventanaIniciarSesion.title("Iniciar sesión")
    ventanaIniciarSesion.geometry("300x250+750+300")
    ventanaIniciarSesion.resizable(0, 0)
    ventanaIniciarSesion.iconbitmap("imagenes/candado.ico")
    ventanaIniciarSesion.config(bg="#5DA9F6")

    Label(ventanaIniciarSesion, text="Por favor ingrese sus datos para iniciar sesión.", bg="#5DA9F6",
          fg="white").pack()
    Label(ventanaIniciarSesion, text="", bg="#5DA9F6").pack()

    username_verify = StringVar()
    password_verify = StringVar()

    Label(ventanaIniciarSesion, text="Correo electrónico", bg="#5DA9F6", fg="white").pack()

    txt_Usuario = Entry(ventanaIniciarSesion, textvariable=username_verify)
    txt_Usuario.pack()

    Label(ventanaIniciarSesion, text="", bg="#5DA9F6").pack()
    Label(ventanaIniciarSesion, text="Contraseña", bg="#5DA9F6", fg="white").pack()

    txt_Contrasenna = Entry(ventanaIniciarSesion, textvariable=password_verify, show='*')
    txt_Contrasenna.pack()

    Label(ventanaIniciarSesion, text="", bg="#5DA9F6").pack()

    def cerrarVentana():
        """
        Función: Activa los widgets del menú principal y cierra la ventaa
        Entradas: NA
        Salidas: NA
        """
        activarMenuPrincipal()
        ventanaIniciarSesion.destroy()

    ventanaIniciarSesion.protocol("WM_DELETE_WINDOW", cerrarVentana)

    def funcionBotonIniciarSesion():
        """
        Función: Inicia sesión con gmail
        Entradas: NA
        Salidas: Retorna pantallaCorreoNuevo en caso de tener un inicio de sesión exitoso, sino retorna pantallaLogin
        """
        correo = txt_Usuario.get().lower()
        contrasenna = txt_Contrasenna.get()

        # Comprobar que los espacios estén llenos
        if correo == "":
            showerror("Error", "El espacio correo no puede estar vacío.")
            ventanaIniciarSesion.destroy()
            return pantallaLogin()
        elif contrasenna == "":
            showerror("Error", "La espacio contraseña no puede estar vacío.")
            ventanaIniciarSesion.destroy()
            return pantallaLogin()

        # Creamos la conexión con el servidor
        sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)

        # Ciframos la conexión
        sesion_smtp.starttls()

        # Iniciamos sesión en el servidor
        try:
            sesion_smtp.login(correo, contrasenna)
            showinfo("Éxito", "Se ha iniciado sesión")
            ventanaIniciarSesion.destroy()
            return pantallaNuevoCorreo(correo, contrasenna)
        except:
            showerror("Error", "No se pudo iniciar sesión con la cuenta: " + correo)
            ventanaIniciarSesion.destroy()
            return pantallaLogin()

    Button(ventanaIniciarSesion, text="Iniciar sesión", width=10, height=1, command=funcionBotonIniciarSesion,
           font="Helvetica").pack()


def funcionBotonBuscar():
    """
    Función: Busca las frases según la cantidad de veces que el usuario lo solicite
    Entradas: NA
    Salidas: Muestra las frases buscadas por el usuario
    """
    if comprobarConexion():
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

            generarDiccionario(nombre)

        mostrarFrases()

        personaje = obtenerPersonajeMasFrases(mayorCantidadFrases)
        lbl_Apariciones.config(text="Personaje con más frases: " + personaje)
    else:
        showerror("Error", "No hay conexión a Internet.")


def funcionBotonShare():
    """
    Función: Permite seleccionar las frases para enviar por correo
    Entradas: NA
    Salidas: Habilita el listbox para seleccionar las frases y deshabilita el botón share, buscar y el txt_Buscar
    """
    if comprobarConexion():

        if len(listbox_Frases.get(0, END)) == 0:
            showerror("Error", "Se deben buscar frases primero.")
        else:
            showinfo("Información", "Seleccione las frases que desee compartir.")
            desactivarMenuPrincipal()

            def funcionBotonEnviarCorreo():
                """
                Función: Prepara toda la información necesaria para enviar un correo
                Entradas: NA
                Salidas: Habilita el btn_Share, btn_Buscar y txt_Buscar y abre la pantalla del login
                """

                frasesSeleccionadas = listbox_Frases.curselection()
                if not len(frasesSeleccionadas) == 0:
                    for frase in frasesSeleccionadas:
                        separarFrasesSeleccionadas(listbox_Frases.get(frase, last=None))
                    generarListaEnviarCorreo()
                    generarXML(frasesCorreo)
                    pantallaLogin()
                    btn_EnviarCorreo.place_forget()
                    listbox_Frases.config(state="disable")
                else:
                    showerror("Error", "Debe seleccionar al menos una frase.")

            btn_EnviarCorreo = Button(frame, text="Enviar correo", command=funcionBotonEnviarCorreo, width=36, height=1)
            btn_EnviarCorreo.place(x=681, y=300)
            btn_EnviarCorreo.config(font="Helvetica")
            listbox_Frases.config(state="normal", selectmode=MULTIPLE)


def cerrarPrograma():
    """
    Función: Pregunta si desea generar un backUp antes de cerrar el programa
    Entradas: NA
    Salidas: Genera un backUp si la respuesta es yes, sino solo cierra el programa
    """
    mensaje = tk.messagebox.askquestion("Cerrar", "Antes de cerrar el programa ¿Desea crear un respaldo?",
                                        icon="warning")

    if mensaje == 'yes':
        generarXML(listaMatriz, True)
    root.quit()


def activarMenuPrincipal():
    """
    Función: Activa los widgets del menú principal
    Entradas: NA
    Salidas: NA
    """
    btn_Share.config(state="normal")
    btn_Buscar.config(state="normal")
    txt_Buscar.config(state="normal")


def desactivarMenuPrincipal():
    """
    Función: Desactiva los widgets del menú principal
    Entradas: NA
    Salidas: NA
    """
    btn_Share.config(state="disable")
    btn_Buscar.config(state="disable")
    txt_Buscar.config(state="disable")


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
frame.config(width=800, height=625, bg="#5DA9F6")

# Creación label del título
lbl_Titulo = Label(frame, text="Frases de Star Wars")
lbl_Titulo.grid(row=0, column=0, padx=10, pady=10, sticky="n")
lbl_Titulo.config(font="Helvetica", fg="white", bg="#5DA9F6")

# Creación listbox
listbox_Frases = Listbox(frame, height=25, width=105)
listbox_Frases.grid(row=1, column=0, padx=10, pady=10)
listbox_Frases.config(state="disabled")

# Creación scroll bar vertical del listbox
scrollVertical = Scrollbar(frame, orient=VERTICAL, command=listbox_Frases.yview)
scrollVertical.grid(row=1, column=1, sticky='nsew')
scrollVertical.config(bg="#5DA9F6")
listbox_Frases['yscrollcommand'] = scrollVertical.set

# Creación scroll bar horizontal del listbox
scrollHorizontal = Scrollbar(frame, orient=HORIZONTAL, command=listbox_Frases.xview)
scrollHorizontal.grid(row=2, column=0, sticky='nsew')
listbox_Frases['xscrollcommand'] = scrollHorizontal.set

# Creación Entry buscar
txt_Buscar = Entry(frame)  # x=681
txt_Buscar.grid(row=1, column=3, padx=10, pady=10, sticky="n")
txt_Buscar.config(justify="center")

# Creación botón share
btn_Share = Button(frame, text="Share", command=funcionBotonShare, width=36, height=1)
btn_Share.place(x=681, y=100)
btn_Share.config(font="Helvetica")

# Creación label apariciones
lbl_Apariciones = Label(frame, text="Personaje con más frases: ")
lbl_Apariciones.place(x=681, y=425)
lbl_Apariciones.config(font="Helvetica", fg="white", bg="#5DA9F6")

# Creación botón buscar
btn_Buscar = Button(frame, text="Buscar", command=funcionBotonBuscar, width=20, height=1)
btn_Buscar.grid(row=1, column=2, sticky="n", padx=10, pady=10)
btn_Buscar.config(font="Helvetica")

# Carga el backUp
lee(archivoBackUp)

# Decisión al guardarBack al cerrar el programa principal
root.protocol("WM_DELETE_WINDOW", cerrarPrograma)

# Inicio de la ventana
root.mainloop()
