#He empleado uneditor online (json editor online) para poder trabajar con la informacion de la URL, ya que esta en formato json.

#Importamos los siguientes modulos, ya que contienen funciones ya creadas en lenguaje python que seran necesarias para nuestro programa.
import http.client
import json

#Nuestro programa es cliente de openfda.
headers={'User-Agent': 'http.client'} #En la cabecera indicamos el navegador que estamos utilizando para pedir la iformacion.


connection = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexion con el API de openfda, es una funcion del modulo http.client.
connection.request("GET", "/drug/label.json", None, headers) #Enviamos una peticion tipo "GET",junto con el recurso ('/drug/label.json') que queremos solicitar.
respuesta= connection.getresponse() #Creamos una variable la cual tendra la respuesta de openfada (del servidor).

info_completa = respuesta.read().decode('utf-8') #La variable 'info_completa' contiene la informacion de 'respuesta' en formato json.
#Aplicamos el ".decode('utf-8')" por si en la informacion hay algun simbolo este se interprete correctamente.

connection.close() #Cerramos la conexion.


info_ordenada = json.loads(info_completa)#La variable 'info_ordenada' contiene la misma informacion pero ordenada.
#Empleamos 'loads' para transformar en listas y diccionarios la informacion y que sea mas facil trabajar con ella.

medicamento=info_ordenada['results'][0]#La informacion del medicamento se encuentra dentro de un diccionario cuya clave es 'results'.
                                       #Dentro del cual hay una lista de donde cogemos el primer valor.

print('Identificador(id):', medicamento['id']) #Para obtener la id del medicamento nos metemos en el diccionario de medicamento con la clave 'id'.

print('Proposito del producto', medicamento['purpose'][0]) #Para obtener el proposito realizamos el mismo porcedimiento que para el id, pero en este caso la clave del diccionario sera 'purpose'

#Por ultimo, el fabricante se obtiene con la clave 'openfda' en cuyo interior hay otro diccionario en el que empleamos la clave 'manufacturer_name'y por ultimo la posicion 0 de la lista.
print('Nombre del fabricante', medicamento['openfda']['manufacturer_name'][0])