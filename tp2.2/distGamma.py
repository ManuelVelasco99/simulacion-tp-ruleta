import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma


alpha = 2
beta = 1.8 
N = 1000
muestras = []


def gamma_pdf(x, alpha, beta):
    return gamma.pdf(x,alpha, scale = 1/beta)

def graficar_gamma():
    while len(muestras) < N:
        x = np.random.exponential(beta*(alpha+1))
        u = np.random.uniform(0, 1)

        if u*maxY <= gamma_pdf(x, alpha, beta):
            muestras.append(x)

# Función de densidad de probabilidad de la distribución gamma
x_vals = np.linspace(0, gamma.ppf(0.999, alpha,scale = 1/beta), 1000)
y_vals = gamma_pdf(x_vals, alpha, beta)
maxY = max(y_vals)
plt.plot(x_vals, y_vals, 'r', label='Función de densidad de probabilidad')



# Histograma de muestras generadas
graficar_gamma()
plt.hist(muestras, bins='sqrt', density=True, label='Muestras generadas', edgecolor = 'black')

# Configuración del gráfico
plt.title('Variable aleatoria con distribución gamma - Método de rechazo')
plt.xlabel('Valor de la variable')
plt.ylabel('Densidad de probabilidad')
plt.legend()
plt.show()