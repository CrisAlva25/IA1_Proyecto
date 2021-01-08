import pandas as pd
import numpy as np
import csv  
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

    #print(lista_retorno["Acatenango"])
    return lista_retorno, max_distancia, min_distancia

def conver(tipo):
    if tipo == "Traslado" or tipo == "FEMENINO":
        return 0.0
    else:
        return 1.0

#calculo de distancia en base a latitud y longitud
def distancia_usac(latitud, longitud):
    #variables
    latitud_usac = 14.589246
    longitud_usac = -90.551449

    #calculo
    radianes = math.pi/180
    dlat = latitud_usac - latitud
    dlon = longitud_usac - longitud

    R = 6372.795477598
    a = (math.sin(radianes*dlat/2))**2 + math.cos(radianes*latitud)*math.cos(radianes*latitud_usac)*(math.sin(radianes*dlon/2))**2
    distancia =2*R*math.asin(math.sqrt(a))
    return distancia

def lectura_dataset():
    #obtenemos datos
    datos = []
    distancias, max_dist, min_dist = lista_distancias_municipios()
    errores = []

    #maximos
    max_edad = 1
    max_año = 1

    #minimosW
    min_edad = 1000
    min_año = 1000

    #recorremos
    with open('datasets\Dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                try:
                    #calculamos la maxima y minima edad
                    if int(row[2]) > max_edad:
                        max_edad = int(row[2])
                    elif int(row[2]) < min_edad:
                        min_edad = int(row[2])

                    #calculamos la maxima y minima año
                    if int(row[7]) > max_año:
                        max_año = int(row[7])
                    elif int(row[7]) < min_año:
                        min_año = int(row[7])
                    #print(row[1])
                    datos.append([row[1],row[2],row[7],distancias[row[6]],conver(row[0])])
                except:
                    errores.append("no existe su municipio en nuestros datos " + row[6])
                line_count += 1
        print(f'Processed {line_count} lines.')

    #realizamos el proceso de escalado en todos los elementos posibles
    #print(min_edad, max_edad, min_año, max_año, min_dist, max_dist)
    #for error in errores:
    #    print(error)
    res = np.array(datos)
    np.random.shuffle(res)
    slice_point = int(len(datos)*0.7)
    test = res[slice_point:]
    train = res[:slice_point]
    
    test_x = []
    test_y = []
    train_x = []
    train_y = []

    for ele in test:
        test_x.append([
            float(conver(ele[0])),
            escalar_var(ele[1], min_edad, max_edad),
            escalar_var(ele[2], min_año, max_año),
            escalar_var(ele[3], min_dist, max_dist)
        ])
        test_y.append([float(ele[4])])

    for ele in train:
        train_x.append([
            float(conver(ele[0])),
            escalar_var(ele[1], min_edad, max_edad),
            escalar_var(ele[2], min_año, max_año),
            escalar_var(ele[3], min_dist, max_dist)
        ])
        train_y.append([float(ele[4])])

    #print(len(test_x))
    #print(test_y)
    #print(len(train_x))
    #print(len(train_y))

    train_x_orig = np.array(train_x).T
    train_y_orig = np.array(train_y).T
    test_x_orig = np.array(test_x).T
    test_y_orig = np.array(test_y).T
    print(np.array(train_x)[1])

    return train_x_orig, train_y_orig, test_x_orig, test_y_orig, distancias, [min_edad, max_edad, min_año, max_año, min_dist, max_dist]

def escalar_var(xi, mini, maximo):
    return (float(xi) - mini) / (maximo - mini)
    
#lista_distancias_municipios()
#lectura_dataset()