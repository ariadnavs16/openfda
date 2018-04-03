import http.server
import socketserver
import http.client
import json

PORT=8080 #Es el puerto en el que lanzaremos el servidor.

def lista_medicamentos():
    lista=[]
    headers={'User-Agent':'http-client'}

    connection = http.client.HTTPSConnection("api.fda.gov")  # Establecemos conexion con el API de openfda.

    # Enviamos una peticion tipo "GET" junto con el recurso ('/drug/label.json?limit=10') que queremos solicitar,
    # introducimos 'limit=10', ya que nos piden 10 objetos de la URL (en el API de fda se encuentra esta informacion).
    connection.request("GET", "/drug/label.json?limit=10", None, headers)

    respuesta = connection.getresponse()  # Creamos una variable la cual tendra la respuesta de openfada.
    print(respuesta.status,respuesta.reason)  # Esto no haria falta imprimirlo, pero nos indica el estado del servidor y que este no esta caido.

    info_completa = respuesta.read().decode('utf-8')  # La variable 'info_completa' contiene la respuesta completa en formato json.
    # Aplicamos el ".decode('utf-8')" por si en la informacion hay algun simbolo este se interprete correctamente.

    connection.close()  # Cerramos la conexion .

    info_ordenada = json.loads(info_completa)  # La variable 'info_ordenada' contiene la misma informacion pero ordenada.
    # Empleamos 'loads' para transformar en listas, diccionarios, etc. la informacion y que sea mas facil trabajar con ella.

    for i in range(len(info_ordenada['results'])):
        medicamento=info_ordenada['results'][i]

        if (medicamento['openfda']):
            print('Fabricante:', medicamento['openfda']['generic_name'][0])
            lista.append(medicamento['openfda']['generic_name'][0])
    return lista


###Es una clase derivada de BaseHTTPRequestHandler, por lo que hereda todos los metodos de esta clase.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    ###Peticion GET por HTTP. El recurso que nos solicitan se encuentra en self.path.
    def do_GET(self):
        ###LA primera linea del mensaje de respuesta es el estatus. Indicamos que OK.
        self.send_response(200)

        ###Cabeceras necesarias para que el cliente entienda el contenido HTML que le enviamos
        self.send_header('Content-type', 'text/html') #el tipo del contenido es texto html
        self.end_headers() #el tipo de info que va a devolver
        content='<html><body>'
        lista=lista_medicamentos()
        for i in lista:
            content+=i+'<br>'
        content+='</body></html>'

        self.wfile.write(bytes(content, 'utf8')) #Manera de contestar a la inforrmacion que han pedido
        return




    ###el servidor comienza aqui
    Handler=testHTTPRequestHandler ###establecemos como manejar nuestra propia clase

    httpd=socketserver.TCPServer(("",PORT), Handler)
    print("serving at port", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("")
    print("Server stopped!")
