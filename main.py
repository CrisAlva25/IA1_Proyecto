import Archivo as Ar
from Util import Plotter
from Neural_Network.Data import Data
from Neural_Network.Model import NN_Model
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
    tabla_alpa = [0.001, 0.075, 1, 0.000250, 0.099, 0.005, 0.000001, 0.2, 0.5, 0.0005725]
    tabla_lamb = [0.0, 0.2, 0.05, 1.3, 0.75, 0.05, 0.1, 5, 7, 0.001]
    tabla_iter = [2500, 1500, 750, 5000, 1000, 150, 1500, 8000, 9513, 4431]
    tabla_keep = [1.0, 0.55, 0.12, 0.47, 0.96, 0.66, 0.88, 0.37, 0.78, 0.01]
    return tabla_alpa[alp], tabla_lamb[lamb], tabla_iter[itera], tabla_keep[keep]

#me regresa si muta o no
def porcentaje(percent=50):
    return random.randrange(100) < percent

def programa():
    #obtengo los valores 
    train_X, train_Y, val_X, val_Y = Ar.lectura_dataset()

    #creo los datasets
    train_set = Data(train_X, train_Y)
    val_set = Data(val_X, val_Y)

    #definimos capas
    capas1 = [train_set.n, 15, 7, 1]

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
    return mejor[0]

ganador = programa()
alfa, lamb, ite, keep = get_hyperParams(ganador.constantes[0], ganador.constantes[1], ganador.constantes[2], ganador.constantes[3])
print("Alpha: ", alfa)
print("Lambda: ", lamb)
print("Iteraciones: ", ite)
print("Keep: ", keep)
print("Fintess: ", ganador.fitness)