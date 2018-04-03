#Importamos los siguientes modulos, ya que seran necesarios para nuestro programa.(ya existen en el lenguaje python)
import http.client
import json #El modulo 'json' nos permite navegar por los ficheros json como si fueran listas o diccionarios.

#Nuestro programa es un cliente de openfda, no es un servidor.
headers={'User-Agent': 'http.client'} #La variable es un diccionario, que se utiliza para cuando vas a pedir informacion indica que navegador estas utilizando.


connection = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexion con el API de openfda.(es del modulo http.client)(protocolo https puerto443)
connection.request("GET", "/drug/label.json", None, headers) #Enviamos una peticion tipo "GET",
                                                            #junto con el recurso ('/drug/label.json') que queremos solicitar
respuesta= connection.getresponse() #Creamos una variable la cual tendra la respuesta de openfada (del servidor).

info_completa = respuesta.read().decode('utf-8') #La variable 'info_completa' contiene la respuesta completa en formato json.
#Aplicamos el ".decode('utf-8')" por si en la informacion hay algun simbolo este se interprete correctamente.

connection.close() #Cerramos la conexion.(la puedes cerrar mas abajo pero no es necesario porque ya tienes la info de la conexion)



#aqui ya estamos tratando el json
#info_completa es un string muy complicado
#info_ordenada es un diccionario, dentro puede tener listas
info_ordenada = json.loads(info_completa)#La variable 'info_ordenada' contiene la misma informacion pero ordenada.
#Empleamos 'loads' para transformar en listas y diccionarios la informacion y que sea mas facil trabajar con ella.(modulo json)

medicamento=info_ordenada['results'][0]#La iinformacion del medicamento se encuentra dentro de un diccionario cuya clave es result.
                                       #Dentro del cual hay una lista de donde cogemos el primer valor.

print('Identificador(id):', medicamento['id']) #Para obtener la id del medicamento nos metemos en el diccionario de medicamento con la clave 'id'.
                                              #Imprimimos dicha informacion, ya que nos la pide el enunciado.

print('Proposito del producto', medicamento['purpose'][0]) #Para obtener el proposito realizamos el mismo porcedimiento que para el id, pero en este caso la clave del diccionario sera 'purpose'

#Por ultimo, el fabricante se obtiene con la clave 'openfda' en cuyo interior hay otro diccionario,
#nos metemos en la clave 'manufacturer_name, este contiene una lista, por ello cogemos la posicion 0 para obtener al fabricante.
print('Nombre del fabricante', medicamento['openfda']['manufacturer_name'][0])