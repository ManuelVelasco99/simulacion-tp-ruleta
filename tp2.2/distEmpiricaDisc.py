from cgi import test
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ecdf, chi2

def f(x, muestra, minimo, maximo):
    rango = maximo - minimo
    cont, _ = np.histogram(muestra, bins=100, range=(minimo, maximo))
    anchoIntervalo = rango / len(cont)
    indiceIntervalo = int((x - minimo) / anchoIntervalo)
    return cont[indiceIntervalo] / len(muestra) / anchoIntervalo

def randomRechazo(muestra):
    minimo = min(muestra)
    maximo = max(muestra)

    r1 = np.random.uniform(minimo, maximo)
    r2 = np.random.uniform(0, max(muestra))
    while r2 > f(r1, muestra, minimo, maximo):
        r1 = np.random.uniform(minimo, maximo)
        r2 = np.random.uniform(0, max(muestra))

    return round(r1)

def calcFrecAbs(muestra, valoresGenerados):
    contadores = [0] * (max(muestra) - min(muestra) + 1)

    for x in range(len(valoresGenerados)):
        contadores[valoresGenerados[x] - min(muestra)] += 1
    return contadores
    
def calcFrecRelAcum(frecAbsolutas, cantValores):
    aux = 0
    frecRelAcumuladas = []
    
    for x in range(len(frecAbsolutas)):
        aux += frecAbsolutas[x]
        frecRelAcumuladas.append(aux / cantValores)
    
    return frecRelAcumuladas

def graficar(valores, muestra, minMuestra):
    if muestra:
        dist = ecdf(muestra)
        dist.cdf.plot(plt, **{"label":"Función densidad", "color":"orange"})

    plt.title('Método de Rechazo')
    plt.bar(x = np.arange(len(valores)) + minMuestra, height = valores, label='Valores generados')

    plt.legend()
    plt.show()

def testChiCuadrado(muestra1, muestra2, nc):
    # hip nula: las dos muestras siguen la misma distribución
    total = len(muestra1) + len(muestra2)
    frecObservadasTotal = {}
    
    frecObservadas1 = {}
    for m in muestra1:
        if m in frecObservadas1:
            frecObservadas1[m] += 1
        else:
            frecObservadas1[m] = 1
        if m in frecObservadasTotal:
            frecObservadasTotal[m] += 1
        else:
            frecObservadasTotal[m] = 1
    
    frecObservadas2 = {}
    for m in muestra2:
        if m in frecObservadas2:
            frecObservadas2[m] += 1
        else:
            frecObservadas2[m] = 1
        if m in frecObservadasTotal:
            frecObservadasTotal[m] += 1
        else:
            frecObservadasTotal[m] = 1

    frecEsperada1 = {}
    frecEsperada2 = {}
    for t in frecObservadasTotal:
        aux = frecObservadasTotal[t] / total * len(muestra1)
        frecEsperada1[t] = aux
    for t in frecObservadasTotal:
        aux = frecObservadasTotal[t] / total * len(muestra2)
        frecEsperada2[t] = aux

    chiM1, chiM2 = 0, 0
    for t in frecObservadasTotal:
        chiM1 += (frecObservadas1[t] - frecEsperada1[t])**2 / frecEsperada1[t]
        chiM2 += (frecObservadas2[t] - frecEsperada2[t])**2 / frecEsperada2[t]
    
    chiTotal = chiM1 + chiM2
    valorTabla = chi2.ppf(nc, len(frecObservadasTotal))

    print()
    print('\nPrueba de bondad de ajuste chi cuadrado')
    print(f"Estadístico obtenido: {chiTotal}")
    print(f"Valor crítico: {valorTabla} - Nivel de confianza: {nc * 100}%")
    print('Resultado: El generador pasa la prueba') if chiTotal < valorTabla else print('Resultado: El generador NO pasa la prueba')


if __name__ == "__main__":
    muestra = [12, 5, 4, 11, 9, 4, 9, 7, 4, 6, 14, 3]
    cantValores = 1000

    valoresGenerados = [randomRechazo(muestra) for _ in range(cantValores)]
    testChiCuadrado(valoresGenerados, muestra, 0.95)

    frecAbsolutas = calcFrecAbs(muestra, valoresGenerados)
    graficar(frecAbsolutas, [], min(muestra))
    
    frecRelAcumuladas = calcFrecRelAcum(frecAbsolutas, cantValores)
    graficar(frecRelAcumuladas, muestra, min(muestra))
