import generadorGLC
from scipy.stats import chi2
import numpy as np
import random
import statistics
import math

def armarIntervalos(lista, cantidad):
    long = (max(lista) - min(lista)) / cantidad
    intervalos = []
    inicio = min(lista)
    fin = inicio + long

    for x in range(cantidad):
        contador = 0
        for x in range(len(lista)):
            if (lista[x] >= inicio and lista[x] <= fin): #mirar el tema de incluir o no incluir el igual
                contador += 1
        intervalos.append(contador)
        inicio = fin
        fin = fin + long
    return intervalos

def pruebaChiCuadrado(intervalos, cantNumeros, nc):
    #La hipótesis es que todos los números tienen la misma probabilidad de aparecer -> distribución uniforme
    cantIntervalos = len(intervalos)
    frecEsperada = cantNumeros / cantIntervalos

    chiCuadrado = 0
    for x in range(cantIntervalos):
        aux = (intervalos[x] - frecEsperada) ** 2 / frecEsperada
        chiCuadrado += aux

    valorTabla = chi2.ppf(nc, cantIntervalos - 1)
    print()
    print(chiCuadrado)
    print(f'Prueba de bondad de ajuste chi cuadrado para una distribución uniforme con {nc} de nivel de confianza')
    print('El generador pasa la prueba') if chiCuadrado < valorTabla else print('El generador no pasa la prueba')


def pruebaEntropiaAproximada(U, m, r):
    
    def distanciaMaxima(v1, v2):
        distancias = []
        for x, y in zip(v1,v2):
            distancias.append(abs(x - y))
        return max(distancias)

    def calcularPhi(m):
        x = [[U[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]
        C = [
            len([1 for x_j in x if distanciaMaxima(x_i, x_j) <= r]) / (N - m + 1.0)
            for x_i in x
        ]
        return (N - m + 1.0) ** (-1) * sum(np.log(C))

    N = len(U)

    return abs(calcularPhi(m + 1) - calcularPhi(m))


def testRachas(lista, mediana):
    cantRachas, cantPositivos, cantNegativos, longitud = 0, 0, 0, len(lista)
    
    for i in range(longitud):
        if (lista[i] >= mediana and lista[i-1] < mediana) or (lista[i] < mediana and lista[i-1] >= mediana):
            cantRachas += 1

        if(lista[i]) >= mediana: 
            cantPositivos += 1
        else: 
            cantNegativos += 1
    
    rachasEsperadas = ((2 * cantPositivos * cantNegativos) / longitud) + 1
    desvioEstandar = math.sqrt((2*cantPositivos*cantNegativos * (2*cantPositivos*cantNegativos-longitud)) / ((longitud**2) * (longitud-1)))

    z = (cantRachas - rachasEsperadas) / desvioEstandar
  
    print("Test de rachas")
    print("Estadístico Z:", abs(z))

    if abs(z) > 1.96:
        print("La secuencia de números NO es aleatoria - 95% nivel de confianza")
    else:
        print("Los números son aleatorios")


if __name__ == "__main__":
    cantNumeros = 1000
    cantIntervalos = 10
    datosObservados = [generadorGLC.next() for _ in range(cantNumeros)]

    intervalos = armarIntervalos(datosObservados, cantIntervalos)
    nivelConfianza = 0.95
    pruebaChiCuadrado(intervalos, cantNumeros, nivelConfianza)


    U = np.array(datosObservados)
    print(pruebaEntropiaAproximada(U, 2, 3))


    mediana = statistics.median(datosObservados) 
    testRachas(datosObservados, mediana)