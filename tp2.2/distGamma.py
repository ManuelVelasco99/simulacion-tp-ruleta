import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma


k = 2
theta = 1.8 
N = 1000


def generar_gamma(): #metodo de rechazo
    samples = []
    while len(samples) < N:
        x = np.random.exponential(theta*(k+1))
        u = np.random.uniform(0, 1)

        if u*maxY <= gamma.pdf(x, k, scale = 1/theta):
            samples.append(x)
    
    return np.array(samples)
    

# Función de densidad de probabilidad de la distribución gamma
valores_x = np.linspace(0, gamma.ppf(0.999, k,scale = 1/theta), 1000)
valores_y = gamma.pdf(valores_x, k, scale = 1/theta)
maxY = max(valores_y)
plt.plot(valores_x, valores_y, 'r', label='Función de densidad de probabilidad')

# Histograma de muestras generadas
muestras = generar_gamma()
plt.hist(muestras, bins='sqrt', density=True, label='Muestras generadas', edgecolor = 'black')

# Configuración del gráfico
plt.title('Variable aleatoria con distribución gamma - Método de rechazo')
plt.xlabel('Valor de la variable')
plt.ylabel('Densidad de probabilidad')
plt.legend()
plt.show()