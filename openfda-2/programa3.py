import http.client
import json

headers={'User-Agent': 'http-client'}

num_skip=0
while True:
    connection = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexion con el API de openfda.

    connection.request("GET",'/drug/label.json?limit=100&skip=' +str(num_skip)+'&search=substance_name:"ASPIRIN"', None, headers)

    respuesta= connection.getresponse() #Creamos una variable la cual tendra la respuesta de openfada.
    print(respuesta.status, respuesta.reason) #Esto no haria falta imprimirlo, pero nos indica el estado del servidor y que este no esta caido.

    info_completa = respuesta.read().decode('utf-8') #La variable 'info_completa' contiene la respuesta completa en formato json.
    #Aplicamos el ".decode('utf-8')" por si en la informacion hay algun simbolo este se interprete correctamente.

    connection.close() #Cerramos la conexion.

    info_ordenada = json.loads(info_completa)  # La variable 'info_ordenada' contiene la misma informacion pero ordenada.
    #Empleamos 'loads' para transformar en listas, diccionarios, etc. la informacion y que sea mas facil trabajar con ella.

    for i in range(len(info_ordenada['results'])):
        medicamento=info_ordenada['results'][i]

        print('ID:', medicamento['id'])

        if(medicamento['openfda']):
            print('Fabricante:', medicamento['openfda']['manufacturer_name'][0])

    if (len(info_ordenada['results'])<100):
        break
    num_skip+=100
