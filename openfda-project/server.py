#Importamos los siguientes modulos, ya que contienen funciones ya creadas en lenguaje python necesarias para nuestro programa.
import http.server
import http.client
import json
import socketserver

#El servidor escucha en el puerto 8000
PORT=8000
IP='localhost'

#Creamos una clase aplicando la herencia, por lo que la clase creada hereda las funciones de la clase padre.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def pagina_formulario(self): #Creamos una funcion que devuelva la pagina web con el formulario en lenguaje html.
        pagina_principal = """
            <html>
                <head> <title>OpenFDA </title> </head>
                <body style="background-color:lightblue">
                    <h1>Formulario OpenFDA</h1>
                    <h3><SMALL>Elija una de las siguientes opciones</SMALL></h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>
                    
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                </body>
            </html> """
        return pagina_principal

    #La siguiente funcion devuelve una pagina web con un listado de la informacion que se pide al escoger una de las opciones en el formulario anterior.
    def pagina_web (self, lista):
        pagina_html = """<html>
                            <head> <title>OpenFDA</title> </head>
                            <body style="background-color: lightblue"> """
        for e in lista:
            pagina_html += "<ul><li>" +e+ "</li></ul>"+"<br>"
        pagina_html += "</body></html>"
        return pagina_html

    #Creamos una funcion para obtener la informacion de openfda.
    def obtener_resultados (self, limit=10):
        connection = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexion con el API de openfda.
        connection.request("GET","/drug/label.json" + "?limit="+str(limit))  #Enviamos una peticion tipo "GET" junto con el recurso que queremos solicitar.
        print ("/drug/label.json" + "?limit="+str(limit))

        respuesta = connection.getresponse()#Creamos una variable la cual tendra la respuesta de openfada.
        info_raw = respuesta.read().decode("utf8")# Aplicamos el ".decode('utf-8')" por si en la informacion hay algun simbolo este se interprete correctamente.
        info= json.loads(info_raw) #Empleamos la función '.loads' para transformar en diccionarios la informacion y que sea mas facil trabajar con ella.
        info_resultados = info['results']
        return info_resultados


    #Definimos una funcion para responder a peticiones tipo GET
    def do_GET(self):
        recurso_connection = self.path.split("?") #Dividimos con ".split()" el recurso que nos solicitan, el recurso se encuentra en "self.path".
        #Comprobamos si el recurso que nos han solicitado contiene parametros
        if len(recurso_connection) > 1:
            parametros = recurso_connection[1]
        else:
            parametros = ""

        limit=10 #Le damos un valor por defecto a limit.

        #Obtenemos el valor de los parametros del recurso, en este caso del parametro 'limit'.
        if parametros:
            param_limit = parametros.split("=")
            if param_limit[0] == "limit":
                limit = int(param_limit[1]) #Asignamos a la variable limit el valor que este tiene en el recurso introducido.
                print("Limit: {}".format(limit))
        else:
            print("El recurso introducido no tiene parametros o los parametros introducidos no se encuentran en el servidor")


        #A continuacion tratamos las posibles peticiones,y las escogidas en el formulario.

        if self.path=='/': #El resurso solicitado no contiene parametros.
            #Primero creamos la cabecera que se enviara al cliente.
            self.send_response(200) #Enviamos el status 200 para indicar que la solicitus ha tenido exito.
            self.send_header('Content-type', 'text/html') #Muestra al cliente que la informacion que recibe esta en formato html.
            self.end_headers()

            html=self.pagina_formulario() #Se accede a la funcion creada anteriormente y devuelve la pagina web con el formulario.
            self.wfile.write(bytes(html, "utf8")) #Informacion enviada al cliente.

        elif 'listDrugs' in self.path: #Si en el resurso aparece 'listDrugs', al escoger esta opcion en el formulario aparecera.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            medicamentos_list = []
            contenido = self.obtener_resultados(limit) #Accede a la funcion creada anteriormente con la informacion obtenida de openfda.
            #La informacion se encuentra en diccionarios, accedemos a ellos para obtener la informacion que nos interesa.
            for item in contenido:
                if ('generic_name' in item['openfda']):
                    medicamentos_list.append (item['openfda']['generic_name'][0]) #Añade a la lista la informacion, en este caso el nombre de los medicamentos.
                else:
                    medicamentos_list.append("Nombre del medicamento no disponible")
            pagina_html = self.pagina_web(medicamentos_list) #La pagina web que aparece es la creada en la funcion anterior ('pagina_web) y cuya variable sera la lista de medicamentos creada.
            self.wfile.write(bytes(pagina_html, "utf8"))


        #Siguen la misma estructura que el anterior.
        elif 'listCompanies' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            list_companies = []
            contenido = self.obtener_resultados(limit)
            for item in contenido:
                if ('manufacturer_name' in item['openfda']):
                    list_companies.append (item['openfda']['manufacturer_name'][0])
                else:
                    list_companies.append("Nombre de la empresa no disponible")
            pagina_html = self.pagina_web(list_companies)
            self.wfile.write(bytes(pagina_html, "utf8"))


        elif 'listWarnings' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            list_warnings = []
            contenido = self.obtener_resultados(limit)
            for item in contenido:
                if ('warnings' in item):
                    list_warnings.append (item['warnings'][0])
                else:
                    list_warnings.append('Advertencias del farmaco no disponible')
            pagina_html = self.pagina_web(list_warnings)
            self.wfile.write(bytes(pagina_html, "utf8"))


        elif 'searchDrug' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10
            drug=self.path.split('=')[1]

            list_search_drugs = []
            connection= http.client.HTTPSConnection("api.fda.gov")
            #Establecemos conexion con openfda y enviamos una peticion tipo 'GET' con el recurso que queremos solicitar.
            #En este casoempleamos dos parametros 'limit' y 'search'.
            connection.request("GET", "/drug/label.json" + "?limit="+ str(limit) + "&search=active_ingredient:" + drug)
            respuesta = connection.getresponse()
            info_raw = respuesta.read().decode("utf8")
            info = json.loads(info_raw)
            info_drugs = info['results']
            for item in info_drugs:
                if ('generic_name' in item['openfda']):
                    list_search_drugs.append(item['openfda']['generic_name'][0])
                else:
                    list_search_drugs.append('Nombre del medicamento no disponible')
            pagina_html = self.pagina_web(list_search_drugs)
            self.wfile.write(bytes(pagina_html, "utf8"))


        elif 'searchCompany' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10
            company=self.path.split('=')[1]

            list_search_companies = []
            connection = http.client.HTTPSConnection("api.fda.gov")
            connection.request("GET", "/drug/label.json" + "?limit=" + str(limit) + '&search=openfda.manufacturer_name:' + company)
            respuesta = connection.getresponse()
            info_raw = respuesta.read().decode("utf8")
            info = json.loads(info_raw)
            info_companies = info['results']

            for item in info_companies:
                if ('manufacturer_name' in item['openfda']):
                    list_search_companies.append(item['openfda']['manufacturer_name'][0])
                else:
                    list_search_companies.append('Nombre de la empresa no disponible')
            pagina_html = self.pagina_web(list_search_companies)
            self.wfile.write(bytes(pagina_html, "utf8"))


        #Introduciomos las siguientes extensiones al codigo.
        elif 'redirect' in self.path: #El servidor web redirige al cliente a la pagina principal.
            print('Mandamos la redirección a la pagina principal')
            self.send_response(301)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()

        elif 'secret' in self.path: #Se trata de una URL de acceso restringido.
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()

        else: #Si el recurso solicitado no se encuentra en el servidor.
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())
        return








#A continuacion creamos el servidor
socketserver.TCPServer.allow_reuse_address= True #Añadimos esta linea para no tener que esta cambiando el puerto, nos permite reutilizarlo.

Handler = testHTTPRequestHandler #Instancia de la clase creada anteriormente.

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever() #El servidor esta esperando indefinidamente, hasta que lo paremos manualmente.
except KeyboardInterrupt:
    pass
httpd.server_close()
print("")
print("El servidor ha sido interrumpido")
