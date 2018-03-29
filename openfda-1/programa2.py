import http.client
import json #El modulo 'json' nos permite navegar por los ficheros json como si fueran listas o diccionarios.

#Nuestro programa es un cliente de openfda, no es un servidor.
headers={'User-Agent': 'http.client'}


connection = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexion con el API de openfda.

#Enviamos una peticion tipo "GET" junto con el recurso ('/drug/label.json?limit=10') que queremos solicitar,
#introducimos 'limit=10', ya que nos piden 10 objetos de la URL (en el API de fda se encuentra esta informacion).
connection.request("GET", "/drug/label.json?limit=10", None, headers)

respuesta= connection.getresponse() #Creamos una variable la cual tendra la respuesta de openfada.
print(respuesta.status, respuesta.reason) #Esto no haria falta imprimirlo, pero nos indica el estado del servidor y que este no esta caido.

info_completa = respuesta.read().decode('utf-8') #La variable 'info_completa' contiene la respuesta completa en formato json.
#Aplicamos el ".decode('utf-8')" por si en la informacion hay algun simbolo este se interprete correctamente.

connection.close() #Cerramos la conexion.


info_ordenada = json.loads(info_completa) #La variable 'info_ordenada' contiene la misma informacion pero ordenada.
#Empleamos 'loads' para transformar en listas, diccionarios, etc. la informacion y que sea mas facil trabajar con ella.

for i in range(len(info_ordenada['results'])): #Aplicamos un bucle 'for' para que recorra toda la lista,
                                               #ya que en este caso devuelve una lista con 10 objetos

    medicamento = info_ordenada['results'][i]#La 'i' en este caso son las posiciones, por ello aplicamos el bucle 'for' sobre el rango.
                                             #La variable 'medicamento' ira guardando la informacion.

    print('ID:', medicamento['id'])#Finalmente imprimimos por pantalla la 'id' de cada uno de los 10 medicamentos.