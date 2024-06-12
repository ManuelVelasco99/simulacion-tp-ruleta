import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma, chi2, norm


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


def testChiCuadradoGamma(lista, nc, cantIntervalos, shape, scale):
    """
    Prueba de bondad de ajuste chi-cuadrado para una distribución Gamma.

    Args:
        lista: lista de datos generados.
        nc: nivel de confianza (por ejemplo, 0.95 para un 95% de confianza).
        cantIntervalos: cantidad de intervalos en los que se dividirán los datos.
        shape: parámetro de forma (k) de la distribución Gamma.
        scale: parámetro de escala (theta) de la distribución Gamma.
    """
    # Calcular la cantidad de números y los intervalos
    cantNumeros = len(lista)
    intervalos = np.linspace(min(lista), max(lista), cantIntervalos + 1)

    # Calcular las frecuencias observadas
    frecuencias_observadas, _ = np.histogram(lista, bins=intervalos)

    # Calcular las frecuencias esperadas para cada intervalo
    frecuencias_esperadas = []
    for i in range(cantIntervalos):
        p1 = gamma.cdf(intervalos[i + 1], shape, scale=scale)
        p2 = gamma.cdf(intervalos[i], shape, scale=scale)
        probabilidad_intervalo = p1 - p2
        frec_esperada = cantNumeros * probabilidad_intervalo
        frecuencias_esperadas.append(frec_esperada)

    # Calcular el estadístico chi-cuadrado
    chiCuadrado = np.sum((frecuencias_observadas - frecuencias_esperadas) ** 2 / frecuencias_esperadas)

    # Obtener el valor crítico de la tabla chi-cuadrado
    valorTabla = chi2.ppf(nc, cantIntervalos - 1)

    # Imprimir los resultados
    print('Prueba de bondad de ajuste chi-cuadrado para distribución Gamma')
    print(f"Estadístico obtenido: {chiCuadrado}")
    print(f"Valor crítico: {valorTabla} - Nivel de confianza: {nc * 100}%")
    print('Resultado: Supera el test') if chiCuadrado < valorTabla else print('Resultado: NO supera el test')

    return frecuencias_observadas, frecuencias_esperadas


# Histograma de muestras generadas
muestras = generar_gamma()
testChiCuadradoGamma(muestras, 0.95, 10, k, 1/theta)
plt.hist(muestras, bins='sqrt', density=True, label='Muestras generadas', edgecolor = 'black')

# Configuración del gráfico
plt.title('Variable aleatoria con distribución gamma - Método de rechazo')
plt.xlabel('Valor de la variable')
plt.ylabel('Densidad de probabilidad')
plt.legend()
plt.show()