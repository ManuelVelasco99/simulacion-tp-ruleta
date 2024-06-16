import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

# Para ejecutar el test, se debe de pasar el argument "-t".  Ejemplo: py distPoisson.py -t

def poisson(lambdaValue):
    x = 0
    tr = 1.0
    b = math.exp(-lambdaValue)
    
    while True:
        r = random.random()
        
        tr *= r
        x += 1
        
        # Condición para salir del bucle
        if tr <= b:
            break
    
    return x

def main(lambdaValue, test=False):
    # Genero los valores con la distribución de Poisson
    poissonValues = [poisson(lambdaValue) for _ in range(1000)]

    # Creo el histograma con dichos valores
    plt.hist(poissonValues, bins=range(int(min(poissonValues)), int(max(poissonValues)) + 2), density=True, alpha=0.75, color='blue', edgecolor='black')

    if test:
        # Calculo frecuencias observadas y esperadas
        observed, _ = np.histogram(poissonValues, bins=range(int(min(poissonValues)), int(max(poissonValues)) + 2))
        expected = [len(poissonValues) * (math.exp(-lambdaValue) * lambdaValue**k) / math.factorial(k) for k in range(len(observed))]

        # Realizo el test de chi cuadrado
        chi_squared_stat = sum((observed[i] - expected[i])**2 / expected[i] for i in range(len(observed)))

        # Grados de libertad
        degrees_of_freedom = len(observed) - 1

        # Valor crítico de chi cuadrado para un nivel de significancia del 5%
        critical_value = chi2.ppf(0.95, degrees_of_freedom)

        # Nota para el valor de chi cuadrado
        plt.text(0.5, 0.9, f'Chi2 = {chi_squared_stat:.2f}\nGrados de libertad = {degrees_of_freedom}\nValor critico = {critical_value:.2f}',
                 horizontalalignment='left', verticalalignment='center', transform=plt.gca().transAxes, fontsize=10,
                 bbox=dict(facecolor='white', alpha=0.8))

        # Linea para el valor crítico
        plt.axvline(x=critical_value, color='red', linestyle='--', label='Valor critico')

    # Si se definio el test, muestra la respectiva grafica, si no muestra la grafica normal
    if test:
        plt.title(f'Distribución Poisson con Test (lambda = {lambdaValue})')
    else:
        plt.title(f'Distribución Poisson (lambda = {lambdaValue})')

    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "-t":
        main(3.5, test=True)
    else:
        main(3.5)
