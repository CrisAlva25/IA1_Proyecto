import pandas as pd
import math

"""
Voy a crear los datos en este archivo, primero realizare la separacion y calculo de distancias entre
la universidad y los municipios existentes
"""

def lista_distancias_municipios():
    lista_retorno = {}
    dataset = pd.read_csv("datasets\Municipios.csv")

    max_distancia = 0
    min_distancia  = 10000
    distancia = 0

    for row in dataset.itertuples():
        distancia = distancia_usac(row[4],row[5])
        lista_retorno[row[3]] = distancia

        #calculamos la maxima y minima distancia
        if distancia > max_distancia:
            max_distancia = distancia
        elif distancia < min_distancia:
            min_distancia = distancia

    #print(lista_retorno)
    return lista_retorno, max_distancia, min_distancia

#calculo de distancia en base a latitud y longitud
def distancia_usac(latitud, longitud):
    #variables
    latitud_usac = 14.589246
    longitud_usac = -90.551449

    #calculo
    radianes = math.pi/180
    dlat = latitud_usac - latitud
    dlon = longitud_usac - longitud

    R = 5372.795477598
    a = (math.sin(radianes*dlat/2))**2 + math.cos(radianes*latitud)*math.cos(radianes*latitud_usac)*(math.sin(radianes*dlon/2))**2
    distancia =2*R*math.asin(math.sqrt(a))
    return distancia

def lectura_dataset():

    #obtenemos datos
    datos = []
    distancias, max_dist, min_dist = lista_distancias_municipios()
    dataset = pd.read_csv("datasets\Dataset.csv")

    #maximos
    max_edad = 1
    max_año = 1

    #minimosW
    min_edad = 1000
    min_año = 1000

    #recorremos
    for row in dataset.itertuples():
        try:
            #calculamos la maxima y minima edad
            if row[3] > max_edad:
                max_edad = row[3]
            elif row[3] < min_edad:
                min_edad = row[3]

            #calculamos la maxima y minima año
            if row[8] > max_año:
                max_año = row[8]
            elif row[8] < min_año:
                min_año = row[8]

            datos.append([row[2],row[3],row[8],distancias[row[7]]])
        except:
            print("no existe su municipio en nuestros datos " + row[7])

    #realizamos el proceso de escalado en todos los elementos posibles
    #print(min_edad, max_edad, min_año, max_año, min_dist, max_dist)
    retorno_escalado = []
    for ele in datos:
        retorno_escalado.append([
            ele[0], 
            escalar_var(ele[1], min_edad, max_edad),
            escalar_var(ele[2], min_año, max_año),
            escalar_var(ele[3], min_dist, max_dist),
        ])
    return retorno_escalado


def escalar_var(xi, mini, maximo):
    return (xi - mini) / (maximo - mini)
    

#lista_distancias_municipios()
#lectura_dataset()