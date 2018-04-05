#Importamos los siguientes modulos, ya que contienen funciones ya creadasen lenguajepython necesarias para nuestro programa.
import http.server
import socketserver
import http.client
import json

PORT = 8090 #Es el puerto en el que lanzaremos el servidor.


def lista_medicamentos(): #Creamos una funcion que nos devuelva una lista con la informacion de los medicamentos.

    list = [] #Inicializamos una lista vacia.
    headers = {'User-Agent': 'http-client'} #Esta funcion actua con cliente de fda, al cual le pide la informacion.

    connection = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexion con el API de openfda.
    connection.request("GET", "/drug/label.json?limit=10", None, headers)
    #Enviamos una peticion tipo "GET" junto con el recurso que queremos solicitar,introducimos 'limit=10', ya que nos piden 10 objetos de la URL.

    respuesta = connection.getresponse()  #Creamos una variable la cual tendra la respuesta de openfada.

    info_completa = respuesta.read().decode('utf-8')
    # Aplicamos el ".decode('utf-8')" por si en la informacion hay algun simbolo este se interprete correctamente.

    connection.close()

    info_ordenada = json.loads(info_completa)
    #Empleamos 'loads' para transformar en listas y diccionarios la informacion y que sea mas facil trabajar con ella.

    for i in range(len(info_ordenada['results'])):  #Aplicamos un bucle 'for' sobre el rango para que recorra toda informacion.
        medicamento = info_ordenada['results'][i]

        if (medicamento['openfda']):
            print('Nombre medicamento:', medicamento['openfda']['generic_name'][0])
            list.append(medicamento['openfda']['generic_name'][0])  #Con '.append' incorporamos la informacion a la lista que creamos inicalmente vacia.
        else:
            list.append('El nombre del medicamento no se encuentra disponible')

    return list



class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler): #Es una clase derivada de BaseHTTPRequestHandler, por lo que hereda los metodos de esta clase.

    # Definimos una funcion para responder ha una peticion tipo GET por HTTP,el recurso que nos solicitan se encuentra en self.path
    def do_GET(self):

        self.send_response(200) #En el status indicamos que OK.

        #Creamos el contenido del HTML para que el clienta entienda la informacion que le enviamos.
        self.send_header('Content-type', 'text/html') #Muestra al cliente que se trata de un HTML.
        self.end_headers()
        contenido="""<html>
        <head><title>Lista </title></head>
        <body style="background-color: lightblue">
        <h1> Lista de 10 medicamentos: </h2>"""

        list=lista_medicamentos ()
        for e in list:
            contenido += "<ul><li>"+e+"</li></ul>"+"<br>"
        contenido+="</body></html>"

        self.wfile.write(bytes(contenido, "utf8")) #El contenido lo codificamos en 'utf8' para que se escriba correctamente.
        return



# A continuacion, creamos el servidor.
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT) #Indica en que puerto estas atendiendo.
try:
    httpd.serve_forever() #El servidor esta esperando indefinidamente, hasta que lo paremos manualmente.
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")




