import numpy as np
import matplotlib.pyplot as plt

def pascal_distribution(k, q, size=1000):
    """
    Genera muestras de una distribución de Pascal (binomial negativa) siguiendo
    el algoritmo de la subrutina FORTRAN proporcionada.
    
    Parameters:
        k: número de éxitos requeridos
        q: probabilidad de éxito en cada intento
        size: número de muestras a generar
    """
    samples = []
    qr = np.log(q)
    
    for _ in range(size):
        tr = 1.0
        for _ in range(k):
            r = np.random.rand()
            tr *= r
        nx = np.log(tr) / qr
        samples.append(nx)
    
    return samples

# Parámetros
k = 4  # número de éxitos requeridos
q = 0.2 # probabilidad de éxito en cada intento

# Generar la distribución
samples = pascal_distribution(k, q, size=1000)

# Graficar la distribución
plt.figure(figsize=(8, 6))
plt.hist(samples, bins=30, density=True, alpha=0.7, color='steelblue', edgecolor='black')
plt.title('Distribución de Pascal')
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
