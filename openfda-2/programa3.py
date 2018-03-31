import http.client
import json

headers={'User-Agent': 'http-client'} #Cabecera que indica que nuestro programa es un cliente.

contador=0 #Inicializamos una variable que usaremos como contador para obtener todos los medicamentos relacionados con las Aspirinas.

while True: #Empleamos un bucle 'while' con valor inicial 'True' para recorrer el api de fda

    connection = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexion con el API de openfda.

    connection.request("GET",'/drug/label.json?limit=100&skip=' +str(contador)+'&search=substance_name:"ASPIRIN"', None, headers)

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
            print('Fabricantes que producen aspirinas:', medicamento['openfda']['manufacturer_name'][0])

    if (len(info_ordenada['results'])<100):
        break
    contador+=100
