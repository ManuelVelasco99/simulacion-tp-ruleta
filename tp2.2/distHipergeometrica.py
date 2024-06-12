import random, math, numpy as np
import matplotlib.pyplot as plt
from scipy.stats import hypergeom

def f(x, N, K, n):
    if x > n: return -1
    return (math.comb(K, x) * math.comb(N-K, n-x)) / math.comb(N, n)

def randomRechazo(M, N, n):
    #a=0, b=n, max(f)=n
    c = 1
    decremento = 0.001
    while c * n > 1:
        if c - decremento <= 0: decremento *= 0.1
        c -= decremento

    r1 = random.random()
    r2 = random.random()
    while (r2 > c * f(round(N * r1), M, N, n)):
        r1 = random.random()
        r2 = random.random()
    
    x = round(N * r1)
    return x

def generarGraficoBarras(valores, M, N, n):
    plt.title('Método de Rechazo')
    x = np.arange(0, n+1)
    pmf = hypergeom.pmf(x, M, N, n)
    plt.plot(x, pmf, 'r-', alpha=0.6, label='Función densidad')
    plt.xticks(x)

    plt.bar(x = np.arange(len(valores)), height = valores, label='Valores generados')
    plt.plot()
    plt.legend()
    plt.show()


if __name__ == "__main__":
    M = 200
    N = 80
    n = 15
    cantValores = 1000
    contadores = [0] * (n+1)

    for x in range(cantValores):
        contadores[randomRechazo(M, N, n)] += 1

    for x in range(len(contadores)):
        contadores[x] /= cantValores

    generarGraficoBarras(contadores, M, N, n)
