import http.client
import json

headers={'User-Agent': 'http.client'}

connection = http.client.HTTPSConnection("api.fda.gov")

#Enviamos una peticion tipo "GET" junto con el recurso ('/drug/label.json?limit=10') que queremos solicitar,
#introducimos 'limit=10', ya que nos piden obtener 10 medicamentos de la URL.
connection.request("GET", "/drug/label.json?limit=10", None, headers)

respuesta= connection.getresponse() #Creamos una variable la cual tendra la respuesta de openfada.

info_completa = respuesta.read().decode('utf-8')
#Aplicamos el ".decode('utf-8')" por si en la informacion hay algun simbolo este se interprete correctamente.

connection.close()


info_ordenada = json.loads(info_completa) #Empleamos 'loads' para transformar en listas y diccionarios la informacion y que sea mas facil trabajar con ella.
num=0
for i in range(len(info_ordenada['results'])): #Aplicamos un bucle 'for' para que recorra toda la lista,
                                               #ya que en este caso devuelve una lista con 10 objetos

    medicamento = info_ordenada['results'][i] #Al aplicar el bucle 'for' sobre el rango la 'i' son posiciones.
    num+=1                                         #La variable 'medicamento' ira guardando la informacion.

    print('ID medicamento',num,':', medicamento['id'])#Finalmente imprimimos por pantalla la 'id' de cada uno de los 10 medicamentos.

