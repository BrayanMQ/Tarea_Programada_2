# Realizado por: Brayan Steven Marín Quirós y Ronny Jiménez Bonilla
# Fecha de creación: 02/04/2019 10:00am
# Última modificación: 02/04/2019 11:20pm
# Versión: 3.7.2



def funcionBotonBuscar():
    r = request("GET", "http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote")
    json_body = r.json()

    id = json_body["id"]
    frase = json_body["starWarsQuote"]
    print(id, frase)


def funcionBotonShare():
    print("")
