import numpy as np
from scipy.stats import binom, chisquare
import matplotlib.pyplot as plt
from math import sqrt, comb, trunc

def binomial_rejection_sampling(n, p):
    # Definir la función de probabilidad masiva de la binomial
    def pmf_binomial(k, n, p):
        return binom.pmf(k, n, p)
    
    # Encontrar la constante de escala M
    max_pmf = max(pmf_binomial(k, n, p) for k in range(n + 1))
    M = (n + 1) * max_pmf
    
    while True:
        # Generar k de la distribución uniforme U(0, n)
        k = np.random.randint(0, n + 1)
        
        # Generar u de la distribución uniforme continua U(0, 1)
        u = np.random.uniform(0, 1)
        
        # Verificar la condición de aceptación
        if u <= pmf_binomial(k, n, p) / (M * (1 / (n + 1))):
            return k
        
def testChiCuadrado(muestras):
  # Calcular frecuencias observadas
  observed_freq = np.bincount(muestras, minlength=n+1)

  # Calcular frecuencias esperadas
  expected_freq = np.array([binom.pmf(k, n, p) * len(muestras) for k in range(n+1)])

  # Realizar la prueba chi-cuadrado
  chi2_stat, p_value = chisquare(observed_freq, expected_freq)

  print(f"Chi-cuadrado: {chi2_stat}")
  print(f"p-valor: {p_value}")

  # Interpretación
  alpha = 0.05
  if p_value < alpha:
      print("No supera el test")
  else:
      print("Supera el test")


# Ejemplo de uso
n = 100
p = 0.5
samples = [binomial_rejection_sampling(n, p) for _ in range(1000)]

testChiCuadrado(samples)
x = np.arange(binom.ppf(0.0001, n, 0.5), binom.ppf(0.999, n, 0.5))
plt.plot(x, binom.pmf(x, n, p), '-r', ms=2, label='Distribucion binomial')
plt.hist(samples, density=True, bins=round(sqrt(len(samples))), edgecolor='black')
plt.title('Histograma de una variable aleatoria discreta con distribucion binomial')
plt.xlabel('Valor de la variable')
plt.ylabel('Ocurrencias')
plt.legend(loc='best', frameon=False)
plt.ylabel("Densidad de ocurrencias")
plt.show()