import numpy as np
from scipy.stats import chi2


def obtener_valores_centrales(num):
    str_number = str(num)
    length = len(str_number)
    
    if length < 4:
        return str_number
    
    start_index = length // 2 - 2
    end_index = start_index + 4
    
    return str_number[start_index:end_index]

def chi_square_test(numbers, categories):
    observed_freq = np.zeros(categories)
    category_range = 10000 // categories

    for number in numbers:
        category = number // category_range
        observed_freq[category] += 1

    expected_freq = len(numbers) / categories
    chi_square_stat = np.sum((observed_freq - expected_freq) ** 2 / expected_freq)
    return chi_square_stat


semilla = 92458139658673422
numerosGenerados = []
categorias = 10

for i in range(50):
    valor = semilla**2
    nuevaSemilla = int(obtener_valores_centrales(valor))
    semilla = nuevaSemilla
    numerosGenerados.append(semilla)

chi_square_stat = chi_square_test(numerosGenerados, categorias)
critical_value = chi2.ppf(0.95, categorias - 1)

print(f"Estadístico chi cuadrado: {chi_square_stat}")
print(f"Valor crítico: {critical_value}")

if chi_square_stat < critical_value:
    print("No se puede rechazar la hipótesis nula: los números son aleatorios")
else:
    print("Se rechaza la hipótesis nula: los números no son aleatorios")
    

