import http.client
import json

headers={'User-Agent': 'http-client'}

connection = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexion con el API de openfda.


connection.request("GET",'/drug/label.json?limit=100&search=active_ingredient:"acetylsalicylic"', None, headers)
#Enviamos una peticion tipo 'GET' junto al recurso al que le incorporamos datos adicionales como son 'limit' y 'search'.

respuesta= connection.getresponse() #Creamos una variable la cual tendra la respuesta de openfada.

info_completa = respuesta.read().decode('utf-8') #La variable 'info_completa' contiene la informacion de 'respuesta' en formato json.
    #Aplicamos el ".decode('utf-8')" por si en la informacion hay algun simbolo este se interprete correctamente.


info_ordenada = json.loads(info_completa)
    #Empleamos 'loads' para transformar en listas y diccionarios la informacion y que sea mas facil trabajar con ella.

for i in range(len(info_ordenada['results'])): #Aplicamos un bucle 'for' sobre el rango para que recorra toda informacion.
    medicamento=info_ordenada['results'][i]

    print('ID:', medicamento['id']) #Imprimimos por pantalla el 'id' de cada uno de los medicamentos.


    if(medicamento['openfda']):
        print('Fabricante:', medicamento['openfda']['manufacturer_name'][0])
    else:
        print('El nombre del fabricante no esta disponible')


connection.close()
