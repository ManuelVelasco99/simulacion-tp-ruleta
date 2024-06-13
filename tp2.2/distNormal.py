from matplotlib.pylab import chisquare
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2

# Parámetros de la distribución normal
EX = 2 # Media
STDX = 1  # Desviación estándar

# Generador distribucion normal en python del ejemplo en Fortran
def generate_normal(EX, STDX, n_samples):
    samples = []
    for _ in range(n_samples):
        sum_r = sum(np.random.uniform(0, 1, 12))
        x = STDX * (sum_r - 6.0) + EX
        samples.append(x)
    return np.array(samples)

# Método de rechazo
def metodo_rechazo(EX, STDX, n_samples):
    samples = []
    while len(samples) < n_samples:
        u1 = np.random.uniform(0, 1)
        u2 = np.random.uniform(0, 1)
        v1 = 2 * u1 - 1
        v2 = 2 * u2 - 1
        w = v1**2 + v2**2
        if w <= 1:
            y = np.sqrt(-2 * np.log(w) / w)
            x = v1 * y
            samples.append(STDX * x + EX)
    return np.array(samples)

# Método de transformada inversa
def metodo_t_inversa(EX, STDX, n_samples):
    u1 = np.random.uniform(0, 1, n_samples)
    u2 = np.random.uniform(0, 1, n_samples)
    z0 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    return STDX * z0 + EX

# Generar muestras
n_samples = 10000
samples_normal = generate_normal(EX, STDX, n_samples)
samples_rechazo = metodo_rechazo(EX, STDX, n_samples)
samples_inversa = metodo_t_inversa(EX, STDX, n_samples)

# Función de densidad de probabilidad (PDF) de la distribución normal
x = np.linspace(EX - 4*STDX, EX + 4*STDX, 1000)
pdf = norm.pdf(x, EX, STDX)

def testChiCuadradoNormal(lista, nc, cantIntervalos, shape, scale):
    """
    Prueba de bondad de ajuste chi-cuadrado para una distribución Normal.

    Args:
        lista: lista de datos generados.
        nc: nivel de confianza (por ejemplo, 0.95 para un 95% de confianza).
        cantIntervalos: cantidad de intervalos en los que se dividirán los datos.
        shape: parámetro de forma de la distribución Normal.
        scale: parámetro de escala de la distribución Normal.
    """
    # Calcular la cantidad de números y los intervalos
    cantNumeros = len(lista)
    intervalos = np.linspace(min(lista), max(lista), cantIntervalos + 1)

    # Calcular las frecuencias observadas
    frecuencias_observadas, _ = np.histogram(lista, bins=intervalos)

    # Calcular las frecuencias esperadas para cada intervalo
    frecuencias_esperadas = []
    for i in range(cantIntervalos):
        p1 = norm.cdf(intervalos[i + 1], loc=shape, scale=scale)
        p2 = norm.cdf(intervalos[i], loc=shape, scale=scale)
        probabilidad_intervalo = p1 - p2
        frec_esperada = cantNumeros * probabilidad_intervalo
        frecuencias_esperadas.append(frec_esperada)

    # Calcular el estadístico chi-cuadrado
    chiCuadrado = np.sum((frecuencias_observadas - frecuencias_esperadas) ** 2 / frecuencias_esperadas)

    # Obtener el valor crítico de la tabla chi-cuadrado
    valorTabla = chi2.ppf(nc, cantIntervalos - 1)

    # Imprimir los resultados
    print('Prueba de bondad de ajuste chi-cuadrado para distribución Normal')
    print(f"Estadístico obtenido: {chiCuadrado}")
    print(f"Valor crítico: {valorTabla} - Nivel de confianza: {nc * 100}%")
    if chiCuadrado < valorTabla:
        print('Resultado: Supera el test')
    else:
        print('Resultado: NO supera el test')

    return frecuencias_observadas, frecuencias_esperadas, chiCuadrado, valorTabla

# Realizar test de chi-cuadrado
testChiCuadradoNormal(samples_normal, 0.95, 50, EX, STDX)

# Generar graficas
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.hist(samples_normal, bins=50, density=True, alpha=0.6, color='b', label='Muestras')
plt.plot(x, pdf, 'r', label='Normal teórica')
plt.title('Generador distribucion normal')
plt.xlabel('Valor')
plt.ylabel('Densidad')
plt.legend()

plt.subplot(1, 3, 2)
plt.hist(samples_rechazo, bins=50, density=True, alpha=0.6, color='g', label='Muestras')
plt.plot(x, pdf, 'r', label='Normal teórica')
plt.title('Método de rechazo')
plt.xlabel('Valor')
plt.ylabel('Densidad')
plt.legend()

plt.subplot(1, 3, 3)
plt.hist(samples_inversa, bins=50, density=True, alpha=0.6, color='r', label='Muestras')
plt.plot(x, pdf, 'b', label='Normal teórica')
plt.title('Método de transformada inversa')
plt.xlabel('Valor')
plt.ylabel('Densidad')
plt.legend()

plt.tight_layout()
plt.show()
