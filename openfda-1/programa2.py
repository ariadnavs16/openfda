import http.client
import json #El modulo 'json' nos permite navegar por los ficheros json como si fueran listas o diccionarios.

#Nuestro programa es un cliente de openfda, no es un servidor.
headers={'User-Agent': 'http.client'}


connection = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexion con el api de openfda.
connection.request("GET", "/drug/label.json", None, headers) #Enviamos una peticion tipo "GET",
                                                           #junto con el recurso ('/drug/label.json') que queremos solicitar
respuesta= connection.getresponse() #Creamos una variable la cual tendra la respuesta de openfada.
print(respuesta.status, respuesta.reason) #Esto no haria falta imprimirlo, pero nos indica el estado del servidor y que este no esta caido.

info_completa = respuesta.read().decode('utf-8') #La variable 'info_completa' contiene la respuesta completa en formato json.
#Aplicamos el ".decode('utf-8')" por si en la informacion hay algun simbolo este se interprete correctamente.

connection.close() #Cerramos la conexion.

fichero= open ('label.json', 'w')
fichero.write(info_completa)
fichero.close()


info_ordenada = json.loads(info_completa) #La variable 'info_ordenada' contiene la misma informacion pero ordenada.
#Empleamos 'loads' para transformar en listas, diccionarios, etc. la informacion y que sea mas facil trabajar con ella.

for i in range(len(info_ordenada['results'])):
    medicamento = info_ordenada['results'][i]

    print('ID:', medicamento['id'])