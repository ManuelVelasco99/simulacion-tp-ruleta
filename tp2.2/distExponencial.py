import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import expon

def generar_exponencial(numero, lambda_param):
    
    # Aplicar la transformada inversa
    exponenciales = -np.log(numero) / lambda_param
    
    return exponenciales


# Parámetro lambda
lambda_param = 0.5

# Número de valores a generar
n = 1000

def graficar_exponencial():
    numero = [random.uniform(0, 1) for i in range(n)]
    num = generar_exponencial(numero, lambda_param)

    # Definir funcion de densidad y graficar para comparar
    x = np.linspace(expon.ppf(0.0001, scale=1 / lambda_param), expon.ppf(0.999, scale=1 / lambda_param), 100)
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, expon.pdf(x, scale=1 / lambda_param), 'r-', lw=2, alpha=0.6, label='exponencial ')
    ax.legend(loc='best', frameon=False)

    # Histograma de densidades de x aceptadas por el metodo de rechazo
    ax.hist(num, density=True, bins='auto', histtype='stepfilled')
    plt.ylabel("Densidad de ocurrencias")
    plt.xlabel("Valor de la variable")
    plt.title('Variable aleatoria con distribucion Exponencial - Método de rechazo')
    plt.show()

graficar_exponencial()

