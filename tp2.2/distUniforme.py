import random, numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform, chi2

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

def armarIntervalos(lista, a, b):
    cantIntervalos = int(len(lista) / 10)
    long = (b - a) / cantIntervalos #los numeros pertenecen al intervalo [a, b]
    inicio = a
    fin = inicio + long
    intervalos = []

    for _ in range(cantIntervalos):
        contador = 0
        for x in range(len(lista)):
            if (lista[x] >= inicio and lista[x] < fin):
                contador += 1

        intervalos.append(contador)
        inicio = fin
        fin = fin + long
    
    intervalos[-1] += lista.count(b)
    return intervalos

def testChiCuadrado(lista, nc, a, b, titulo):
    # para distribución uniforme
    cantNumeros = len(lista)
    intervalos = armarIntervalos(lista, a, b)
    cantIntervalos = len(intervalos)
    frecEsperada = cantNumeros / cantIntervalos

    chiCuadrado = 0
    for x in range(cantIntervalos):
        aux = (intervalos[x] - frecEsperada) ** 2 / frecEsperada
        chiCuadrado += aux

    valorTabla = chi2.ppf(nc, cantIntervalos - 1)

    print('\n' + titulo)
    print('Prueba de bondad de ajuste chi cuadrado para distribución uniforme')
    print(f"Estadístico obtenido: {chiCuadrado}")
    print(f"Valor crítico: {valorTabla} - Nivel de confianza: {nc * 100}%")
    print('Resultado: El generador pasa la prueba') if chiCuadrado < valorTabla else print('Resultado: El generador NO pasa la prueba')


if __name__ == "__main__":
    a = 25
    b = 50
    cantValores = 1000

    transInversa = [randomTransInversa(a, b) for _ in range(cantValores)]
    rechazo = [randomRechazo(a, b) for _ in range(cantValores)]

    testChiCuadrado(transInversa, 0.95, a, b, 'Método Transformada Inversa')
    testChiCuadrado(rechazo, 0.95, a, b, 'Método de Rechazo')

    graficar(transInversa, a, b, 'Método Transformada Inversa')
    graficar(rechazo, a, b, 'Método de Rechazo')
