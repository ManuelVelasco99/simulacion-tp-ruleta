import random, numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform

def f(a, b):
    return 1 / (b - a)

def randomTransInversa(a, b):
    r = random.random()
    x = a + (b - a) * r
    return x

def randomRechazo(a, b):
    c = 1
    decremento = 0.001
    while c * f(a, b) > 1:
        if c - decremento <= 0: decremento *= 0.1
        c -= decremento
    
    r1 = random.random()
    r2 = random.random()
    while (r2 > c * f(a, b)):
        r1 = random.random()
        r2 = random.random()
    
    x = a + (b - a) * r1
    return x

def graficar(valores, a, b, titulo):
    dist = uniform(loc=a, scale=b-a)
    x = np.linspace(dist.ppf(0), dist.ppf(1), 100)
    pdf = dist.pdf(x)

    plt.title(titulo)
    plt.hist(valores, density=True, histtype='bar', edgecolor='black', alpha=0.5, label='Valores generados')
    plt.plot(x, pdf, 'r-', alpha=0.6, label='Función densidad')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    a = 25
    b = 50
    cantValores = 1000

    transInversa = [randomTransInversa(a, b) for _ in range(cantValores)]
    rechazo = [randomRechazo(a, b) for _ in range(cantValores)]

    graficar(transInversa, a, b, 'Método Transformada Inversa')
    graficar(rechazo, a, b, 'Método de Rechazo')
