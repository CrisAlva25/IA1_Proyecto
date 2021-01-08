import Archivo as Ar
import numpy as np
from Util import Plotter
from Neural_Network.Data import Data
from Neural_Network.Model2 import NN_Model
import random

ONLY_SHOW = False

class Individuo:
    def __init__(self, constantes,fitness):
        self.constantes = constantes
        self.fitness = fitness

def entrenar_neuronas(train_set, val_set, capas1, ind):
    alpha, lambd, iterations, keep_prob = get_hyperParams(ind[0], ind[1], ind[2], ind[3])
    # Se define el modelo
    nn1 = NN_Model(train_set, capas1, alpha, iterations, lambd, keep_prob)
    #nn2 = NN_Model(train_set, capas1, alpha=0.01, iterations=50000, lambd=0.7, keep_prob=1)

    # Se entrena el modelo
    nn1.training(False)
    #nn2.training(False)

    # Se analiza el entrenamiento
    #Plotter.show_Model([nn1])

    #print('Entrenamiento Modelo 1')
    #nn1.predict(train_set)
    #print('Validacion Modelo 1')
    return nn1.predict(val_set)

#aqui empieza mi algoritmo genetico
def crear_poblacion(train_set, val_set, capas1):
    poblacion = []
    for i in range(10):
        temp = []
        for j in range(4):
            temp.append(random.randint(0,9))
        nuevo = Individuo(temp, entrenar_neuronas(train_set, val_set, capas1, temp))
        poblacion.append(nuevo)
    return poblacion

#Seleccion de padres
def seleccionTorneo(poblacion):
    #print("torneo")
    retorno = []
    retorno.append(poblacion[0] if poblacion[0].fitness > poblacion[9].fitness else poblacion[9])
    retorno.append(poblacion[1] if poblacion[1].fitness > poblacion[8].fitness else poblacion[8])
    retorno.append(poblacion[2] if poblacion[2].fitness > poblacion[7].fitness else poblacion[7])
    retorno.append(poblacion[3] if poblacion[3].fitness > poblacion[6].fitness else poblacion[6])
    retorno.append(poblacion[4] if poblacion[4].fitness > poblacion[5].fitness else poblacion[5])
    return retorno

def cruzarPadres(poblacion, train_set, val_set, capas1):
    resultado = poblacion[:]
    resultado.append(getHijo(poblacion[0], poblacion[1],train_set, val_set, capas1)) #1 con 2
    resultado.append(getHijo(poblacion[2], poblacion[4],train_set, val_set, capas1)) #3 con 5
    resultado.append(getHijo(poblacion[0], poblacion[2],train_set, val_set, capas1)) #1 con 3
    resultado.append(getHijo(poblacion[2], poblacion[3],train_set, val_set, capas1)) #3 con 4
    resultado.append(getHijo(poblacion[0], poblacion[4],train_set, val_set, capas1)) #1 con 5
    random.shuffle(resultado)
    return resultado

def getHijo(padre1, padre2, train_set, val_set, capas1):
    hijo = []
    for i in range(4):
        hijo.append(padre1.constantes[i] if porcentaje() else padre2.constantes[i])
    hijo = mutarHijo(hijo)
    return Individuo(hijo,entrenar_neuronas(train_set, val_set, capas1, hijo))

def mutarHijo(hijo):
    i = random.randint(0,3)
    hijo[i] = random.randint(0,9)
    return hijo

#para obtener mis hyper paramaetros
def get_hyperParams(alp, lamb, itera, keep):
    tabla_alpa = [0.0001, 0.0075, 0.95, 0.00250, 0.0099, 0.0025, 0.000014, 0.02, 0.05, 0.0001725]
    tabla_lamb = [0.0, 0.02, 0.005, 0.13, 0.0075, 0.025, 0.0111, 0.5, 0.7, 0.001]
    tabla_iter = [2500, 1500, 750, 5000, 1000, 150, 1500, 8000, 9513, 4431]
    tabla_keep = [1.0, 0.55, 0.012, 0.047, 0.96, 0.066, 0.88, 0.037, 0.78, 0.01]
    return tabla_alpa[alp], tabla_lamb[lamb], tabla_iter[itera], tabla_keep[keep]

#me regresa si muta o no
def porcentaje(percent=50):
    return random.randrange(100) < percent

def programa():
    #obtengo los valores 
    train_X, train_Y, val_X, val_Y, distancias, min_max = Ar.lectura_dataset()

    #creo los datasets
    train_set = Data(train_X, train_Y)
    val_set = Data(val_X, val_Y)

    #definimos capas
    capas1 = [train_set.n, 15, 10, 5, 1]

    poblacion = crear_poblacion(train_set, val_set, capas1)
    loop = True
    iteraciones = 1

    while loop:
        mejoresPadres = seleccionTorneo(poblacion)
        poblacion = cruzarPadres(mejoresPadres, train_set, val_set, capas1)
        if iteraciones == 3:
            loop = False
        iteraciones = iteraciones + 1
    
    mejor = sorted(poblacion, key=lambda x: x.fitness, reverse = True)
    print("iteraciones: ", iteraciones)
    return mejor[0], train_set, val_set, capas1, distancias, min_max

def escalar_var(xi, mini, maximo):
    return (float(xi) - mini) / (maximo - mini)

def principal():
    ganador,train_set, val_set, capas1, distancias, min_max = programa()
    alfa, lamb, ite, keep = get_hyperParams(ganador.constantes[0], ganador.constantes[1], ganador.constantes[2], ganador.constantes[3])
    print("--------------------- SOLUCION ENCONTRADA ---------------------")
    print("Alpha: ", alfa)
    print("Lambda: ", lamb)
    print("Iteraciones: ", ite)
    print("Keep: ", keep)
    print("Fintess: ", ganador.fitness)

    # Se define el modelo
    nn1 = NN_Model(train_set, capas1, alpha=alfa, iterations=ite, lambd=lamb, keep_prob=keep)
    #nn2 = NN_Model(train_set, capas1, alpha=0.01, iterations=50000, lambd=0.7, keep_prob=1)

    # Se entrena el modelo
    nn1.training(False)

    loop = True
    while loop:
        print("1. Predecir ")
        print("2. Salir ")
        seleccion = input("Opcion :")
        if seleccion == "1":
            genero = input("Elija su genero: 1. Masculino, 0.Femenino: ")
            edad = input("Seleccione su edad: ")
            año = input("Su año de inscripcion: ")
            municipio = input("Municipio de residencia: ")

            pre = [float(genero), escalar_var(edad, min_max[0],min_max[1]), escalar_var(año, min_max[2],min_max[3]), escalar_var(distancias[municipio], min_max[4],min_max[5])]
            pre = np.array(pre)
            arr_pre = [pre]
            arr_pre = (np.array(arr_pre)).T

            arr_res = np.zeros(1)
            arr_res2 = [arr_res]
            arr_res2 = (np.array(arr_res2)).T

            predict = Data(arr_pre, arr_res2)
            valor = nn1.predic2(predict)
            if int(valor) == 1 :
                print("Usted no se trasladara")
            else:
                print("Usted se trasladara")
        
        else:
            loop = False
            

principal()