import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import expon, chi2

# Parámetro lambda
lambda_param = 0.5

# Número de valores a generar
n = 1000

def generarExponencialTransfInversa(numero, lambda_param):
    
    # metodo de la transformada inversa
    exponenciales = -np.log(numero) / lambda_param
    
    return exponenciales

def generarExponencialRechazo(lambda_, M, n):
    muestras = []
    c = lambda_ * M
    
    while len(muestras) < n:
        X = np.random.uniform(0, M)
        U = np.random.uniform(0, 1)
        
        if U <= (lambda_ * np.exp(-lambda_ * X)) / c:
            muestras.append(X)
    
    return np.array(muestras)


def armarIntervalos(lista, cantIntervalos):
    min_val = min(lista)
    max_val = max(lista)
    intervalos = np.linspace(min_val, max_val, cantIntervalos + 1)
    frecuencias = np.histogram(lista, bins=intervalos)[0]
    return frecuencias, intervalos

def testChiCuadrado(lista, nc, cantIntervalos):
    # La hipótesis es que los datos siguen una distribución exponencial
    cantNumeros = len(lista)
    media_muestral = np.mean(lista)
    lambda_muestral = 1 / media_muestral
    
    frecuencias_observadas, intervalos = armarIntervalos(lista, cantIntervalos)
    
    frecuencias_esperadas = []
    for i in range(cantIntervalos):
        intervalo_inf = intervalos[i]
        intervalo_sup = intervalos[i+1]
        probabilidad_intervalo = expon.cdf(intervalo_sup, scale=1/lambda_muestral) - expon.cdf(intervalo_inf, scale=1/lambda_muestral)
        frecuencia_esperada = cantNumeros * probabilidad_intervalo
        frecuencias_esperadas.append(frecuencia_esperada)
    
    chiCuadrado = sum((fo - fe) ** 2 / fe for fo, fe in zip(frecuencias_observadas, frecuencias_esperadas))
    
    valorTabla = chi2.ppf(nc, cantIntervalos - 1)
    
    print('Prueba de bondad de ajuste chi cuadrado para distribución exponencial')
    print(f"Estadístico obtenido: {chiCuadrado}")
    print(f"Valor crítico: {valorTabla} - Nivel de confianza: {nc * 100}%")
    print('Resultado: Supera el test') if chiCuadrado < valorTabla else print('Resultado: NO supera el test')
    return frecuencias_observadas, frecuencias_esperadas

def graficarExponencialInversa():
    numero = [random.uniform(0, 1) for i in range(n)]
    num = generarExponencialTransfInversa(numero, lambda_param)

    # Definir funcion de densidad y graficar para comparar
    x = np.linspace(expon.ppf(0.0001, scale=1 / lambda_param), expon.ppf(0.999, scale=1 / lambda_param), 100)
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, expon.pdf(x, scale=1 / lambda_param), 'r-', lw=2, alpha=0.6, label='Función de densidad de probabilidad')
    ax.legend(loc='best', frameon=False)

    testChiCuadrado(num, 0.95, 10)
    # Histograma de densidades de x aceptadas por el metodo de rechazo
    ax.hist(num, density=True, bins='auto', edgecolor='black', label='Muestras generadas')
    plt.ylabel("Densidad de ocurrencias")
    plt.xlabel("Valor de la variable")
    plt.title('Variable aleatoria con distribucion Exponencial - Método T. inversa')
    plt.show()

def graficarExponencialRechazo():
    M = 10
    num = generarExponencialRechazo(lambda_param,M,n)

    # Definir funcion de densidad y graficar para comparar
    x = np.linspace(expon.ppf(0.0001, scale=1 / lambda_param), expon.ppf(0.999, scale=1 / lambda_param), 100)
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, expon.pdf(x, scale=1 / lambda_param), 'r-', lw=2, alpha=0.6, label='Función de densidad de probabilidad')
    ax.legend(loc='best', frameon=False)

    testChiCuadrado(num, 0.95, 10)
    # Histograma de densidades de x aceptadas por el metodo de rechazo
    ax.hist(num, density=True, bins='auto', edgecolor='black', label='Muestras generadas')
    plt.ylabel("Densidad de ocurrencias")
    plt.xlabel("Valor de la variable")
    plt.title('Variable aleatoria con distribucion Exponencial - Método Rechazo')
    plt.show()


graficarExponencialInversa()
graficarExponencialRechazo()

