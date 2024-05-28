import generadorGLC, generadorGCC, generadorMediosCuadrados
from scipy.stats import chi2
import numpy as np
import statistics, math, random

def armarIntervalos(lista, cantidad):
    long = (max(lista) - min(lista)) / cantidad
    intervalos = []
    inicio = min(lista)
    fin = inicio + long

    for x in range(cantidad):
        contador = 0
        for x in range(len(lista)):
            if (lista[x] >= inicio and lista[x] < fin): #mirar el tema de incluir o no incluir el igual
                contador += 1

        intervalos.append(contador)
        inicio = fin
        fin = fin + long
    intervalos[-1] += 1
    return intervalos

def pruebaChiCuadrado(lista, nc, cantIntervalos):
    #La hipótesis es que todos los números tienen la misma probabilidad de aparecer -> distribución uniforme
    cantNumeros = len(lista)
    intervalos = armarIntervalos(datosGenerados, cantIntervalos)
    cantIntervalos = len(intervalos)
    frecEsperada = cantNumeros / cantIntervalos

    chiCuadrado = 0
    for x in range(cantIntervalos):
        aux = (intervalos[x] - frecEsperada) ** 2 / frecEsperada
        chiCuadrado += aux

    valorTabla = chi2.ppf(nc, cantIntervalos - 1)
    print()
    print(chiCuadrado)
    print(f'Prueba de bondad de ajuste chi cuadrado para una distribución uniforme con {nc} de nivel de confianza')
    print('El generador pasa la prueba') if chiCuadrado < valorTabla else print('El generador no pasa la prueba')


def pruebaEntropiaAproximada(lista, m, r):
    
    def distanciaMaxima(v1, v2):
        distancias = []
        for x, y in zip(v1,v2):
            distancias.append(abs(x - y))
        return max(distancias)

    def calcularPhi(m):
        x = [[U[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]
        C = [
            len([1 for x_j in x if distanciaMaxima(x_i, x_j) <= r]) / (N - m + 1.0)
            for x_i in x
        ]
        return (N - m + 1.0) ** (-1) * sum(np.log(C))

    U = np.array(lista)
    N = len(U)
    return abs(calcularPhi(m + 1) - calcularPhi(m))


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
    chi_cuad_todos_iguales = (pow((obs_todos_iguales - esp_todos_iguales), 2)) / esp_todos_iguales
    chi_cuad_una_pareja = (pow((obs_una_pareja - esp_una_pareja), 2)) / esp_una_pareja
    chi_cuad_dos_parejas = (pow((obs_dos_parejas - esp_dos_parejas), 2)) / esp_dos_parejas
    chi_cuad_tres_iguales = (pow((obs_tres_iguales - esp_tres_iguales), 2)) / esp_tres_iguales
    chi_cuad_todos_diferentes = (pow((obs_todos_diferentes - esp_todos_diferentes), 2)) / esp_todos_diferentes

    # Calcular la estadística de chi-cuadrado total.
    chi_cuadrado = chi_cuad_todos_iguales + chi_cuad_una_pareja + chi_cuad_dos_parejas + chi_cuad_tres_iguales + chi_cuad_todos_diferentes
    chi_2_tabla = chi2.ppf(1 - 0.05, 5)
    print("El valor de chi cuadrado en tabla es:", chi_2_tabla)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test Poker" if chi_cuadrado > chi_2_tabla else "Pasa el test Poker")


def testRachas(lista, mediana):
    cantRachas, cantPositivos, cantNegativos, longitud = 0, 0, 0, len(lista)
    
    for i in range(longitud):
        if (lista[i] >= mediana and lista[i-1] < mediana) or (lista[i] < mediana and lista[i-1] >= mediana):
            cantRachas += 1

        if(lista[i]) >= mediana: 
            cantPositivos += 1
        else: 
            cantNegativos += 1
    
    rachasEsperadas = ((2 * cantPositivos * cantNegativos) / longitud) + 1
    desvioEstandar = math.sqrt((2*cantPositivos*cantNegativos * (2*cantPositivos*cantNegativos-longitud)) / ((longitud**2) * (longitud-1)))

    z = (cantRachas - rachasEsperadas) / desvioEstandar
  
    print("Test de rachas")
    print("Estadístico Z:", abs(z))

    if abs(z) > 1.96:
        print("La secuencia de números NO es aleatoria - 95% nivel de confianza")
    else:
        print("Los números son aleatorios")



if __name__ == "__main__":
    nivelConfianza = 0.95 #para el test de bondad chi-cuadrado
    cantNumeros = 1000
    cantIntervalos = 100 #justificar elección en base a la cantidad de números generados
    
    #generadorGLC
    print('\n\n---Generador Lineal Congruencial---\n')
    datosGenerados = [generadorGLC.next() for _ in range(cantNumeros)]
    pruebaChiCuadrado(datosGenerados, nivelConfianza, cantIntervalos)
    print(pruebaEntropiaAproximada(datosGenerados, 2, 3))
    test_poker(datosGenerados, 1-nivelConfianza)
    testRachas(datosGenerados, statistics.median(datosGenerados))

    #generadorMediosCuadrados
    print('\n\n---Generador Medios Cuadrados---\n')
    datosGenerados = [generadorMediosCuadrados.next() for _ in range(cantNumeros)]
    pruebaChiCuadrado(datosGenerados, nivelConfianza, cantIntervalos)
    print(pruebaEntropiaAproximada(datosGenerados, 2, 3))
    test_poker(datosGenerados, 1-nivelConfianza)
    testRachas(datosGenerados, statistics.median(datosGenerados))

    #generadorGCC
    print('\n\n---Generador Cuadrático Congruencial---\n')
    datosGenerados = [generadorGCC.next() for _ in range(cantNumeros)]
    pruebaChiCuadrado(datosGenerados, nivelConfianza, cantIntervalos)
    print(pruebaEntropiaAproximada(datosGenerados, 2, 3))
    test_poker(datosGenerados, 1-nivelConfianza)
    testRachas(datosGenerados, statistics.median(datosGenerados))
