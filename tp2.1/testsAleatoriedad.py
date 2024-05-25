import numpy as np
from scipy.stats import chi2


def test_chi_cuadrado(num, categorias):
    frec_observada = np.zeros(categorias)
    rango_categorias = 10000 // categorias

    for number in num:
        cat = number // rango_categorias
        frec_observada[cat] += 1

    frec_esperada = len(num) / categorias
    estadistico_chi_cuad = np.sum((frec_observada - frec_esperada) ** 2 / frec_esperada)
    return estadistico_chi_cuad


def ejecutar_test_chi_cuadrado(numerosGenerados):
  categorias = 10
  estadistico_chi_cuad = test_chi_cuadrado(numerosGenerados, categorias)
  valor_critico = chi2.ppf(0.95, categorias - 1)

  print(f"Estadístico chi cuadrado: {estadistico_chi_cuad}")
  print(f"Valor crítico: {valor_critico}")

  if estadistico_chi_cuad < valor_critico:
      print("Supera el test chi cuadrado")
  else:
      print("No supera el test chi cuadrado")
    

def test_poker(numeros, a):
    # frecuencias esperadas
    esp_todos_iguales = 0.01 * len(numeros)
    esp_una_pareja = 0.297 * len(numeros)
    esp_dos_parejas = 0.4495 * len(numeros)
    esp_tres_iguales = 0.2401 * len(numeros)
    esp_todos_diferentes = 0.0024 * len(numeros)

    # Inicializa
    obs_todos_iguales = 0
    obs_una_pareja = 0
    obs_dos_parejas = 0
    obs_tres_iguales = 0
    obs_todos_diferentes = 0

    # hace la prueba de póker en cada número
    for i in numeros:
        # Obtiene los primeros tres dígitos decimales del número
        digito = str(i - int(i))[2:5]

        # Cuenta el número de ocurrencias de cada dígito
        contador_digitos = [digito.count(d) for d in digito]

        # Cuenta el número de parejas y el número de dígitos distintos
        contador_parejas = contador_digitos.count(2)
        contador_diferentes = contador_digitos.count(1)

        # Evalúa a qué mano de póker pertenece el número
        if contador_diferentes == 1:  # Todos los dígitos son iguales
            obs_todos_iguales += 1
        elif contador_diferentes == 3:  # Todos los dígitos son diferentes
            obs_todos_diferentes += 1
        elif contador_parejas == 1:  # Una pareja
            obs_una_pareja += 1
        elif contador_parejas == 2:  # Dos parejas
            obs_dos_parejas += 1
        elif contador_diferentes == 2:  # Tres iguales
            obs_tres_iguales += 1

    # Calcula la estadística chi-cuadrado para cada mano de póker
    chiCuadradoTodosIguales = (pow((obs_todos_iguales - esp_todos_iguales), 2)) / esp_todos_iguales
    chiCuadradoUnaPareja = (pow((obs_una_pareja - esp_una_pareja), 2)) / esp_una_pareja
    chiCuadradoDosParejas = (pow((obs_dos_parejas - esp_dos_parejas), 2)) / esp_dos_parejas
    chiCuadradoTresIguales = (pow((obs_tres_iguales - esp_tres_iguales), 2)) / esp_tres_iguales
    chiCuadradoTodosDistintos = (pow((obs_todos_diferentes - esp_todos_diferentes), 2)) / esp_todos_diferentes

    # Calcular la estadística de chi-cuadrado total.
    chiCuadrado = chiCuadradoTodosIguales + chiCuadradoUnaPareja + chiCuadradoDosParejas + chiCuadradoTresIguales + chiCuadradoTodosDistintos
    chi2Tabla = chi2.ppf(1 - 0.05, 5)
    print("El valor de chi cuadrado en tabla es:", chi2Tabla)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test Poker" if chiCuadrado > chi2Tabla else "Pasa el test Poker")