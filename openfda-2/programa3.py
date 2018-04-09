import http.client
import json

headers={'User-Agent': 'http-client'}

connection = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexion con el API de openfda.

contador=0 #Inicializamos una variable que usaremos como contador para obtener todos los medicamentos relacionados con las Aspirinas.
while True: #Empleamos un bucle 'while' infinito con valor inicial 'True' para recorrer el api de fda.

    connection.request("GET",'/drug/label.json?limit=100&skip=' +str(contador)+'&search=active_ingredient:"acetylsalicylic"', None, headers)
    #Enviamos una peticion tipo 'GET' junto al recurso al que le incorporamos datos adicionales como son 'limit'(nos devolvera el numero que le asignemos de medicamentos9,
    #'skip'(saltara el numero de medicamentos que le asignemos y devolvera los siguientes), 'search'(nos permite realizar una busqueda para que nos devuelva aquellos medicamentos que contengan aspirina).

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
    if (len(info_ordenada['results'])<100): #Si el programa devuelve menos de 100 medicamentos cerramos el bucle, ya que no habrian mas medicamentos que contuvieran aspirina.
        break

    contador+=100 #Si no se cumple el 'if' sumamos a la variable skip 100 para que al volver a iniciar el bucle se salte los 100 primeros medicamentos y devuelva los 100 siguientes.

connection.close()
