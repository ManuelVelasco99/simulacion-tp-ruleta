import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ecdf

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


if __name__ == "__main__":
    muestra = [12, 5, 4, 11, 9, 4, 9, 7, 4, 6, 14, 3]
    cantValores = 1000

    valoresGenerados = [randomRechazo(muestra) for _ in range(cantValores)]
    frecAbsolutas = calcFrecAbs(muestra, valoresGenerados)
    graficar(frecAbsolutas, [], min(muestra))
    
    frecRelAcumuladas = calcFrecRelAcum(frecAbsolutas, cantValores)
    graficar(frecRelAcumuladas, muestra, min(muestra))
