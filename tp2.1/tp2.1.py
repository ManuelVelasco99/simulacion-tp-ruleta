import generadorGLC, generadorGCC, generadorMediosCuadrados
from scipy.stats import chi2, norm
import scipy.stats as ss
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
            if (lista[x] >= inicio and lista[x] < fin):
                contador += 1

        intervalos.append(contador)
        inicio = fin
        fin = fin + long
    intervalos[-1] += 1
    return intervalos

def testChiCuadrado(lista, nc, cantIntervalos):
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

    print('Prueba de bondad de ajuste chi cuadrado')
    print(f"Estadístico obtenido: {chiCuadrado}")
    print(f"Valor crítico: {valorTabla} - Nivel de confianza: {nc * 100}%")
    print('Resultado: El generador pasa la prueba') if chiCuadrado < valorTabla else print('Resultado: El generador NO pasa la prueba')


def testKolmogorovSmirnov(lista):
    media, desvio = ss.norm.fit(lista)
    kstest = ss.kstest(lista,"norm",args=(media, desvio))

    print('\nTest de Bondad Kolmogorov-Smirnov para distribución normal: ')
    significacion = (1 - kstest.pvalue) * 100
    print(f"Nivel de significacion: {significacion}%")
 
    if kstest.pvalue < 0.01:
        print('Los números son independientes.')
    else:
        print('Los números NO son independientes.')


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
        digito = str(i)[:3]

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
    chi_cuad_todos_iguales = (pow((esp_todos_iguales - obs_todos_iguales), 2)) / esp_todos_iguales
    chi_cuad_una_pareja = (pow((esp_una_pareja - obs_una_pareja), 2)) / esp_una_pareja
    chi_cuad_dos_parejas = (pow(( esp_dos_parejas - obs_dos_parejas), 2)) / esp_dos_parejas
    chi_cuad_tres_iguales = (pow((esp_tres_iguales - obs_tres_iguales), 2)) / esp_tres_iguales
    chi_cuad_todos_diferentes = (pow(( esp_todos_diferentes - obs_todos_diferentes), 2)) / esp_todos_diferentes

    # Calcular la estadística de chi-cuadrado total.
    chi_cuadrado = chi_cuad_todos_iguales + chi_cuad_una_pareja + chi_cuad_dos_parejas + chi_cuad_tres_iguales + chi_cuad_todos_diferentes
    chi_2_tabla = chi2.ppf(1 - a, 99)
    print("Resultado del test con una confianza del", (1 - a) * 100, "%:",
          "No pasa el test Poker" if chi_cuadrado > chi_2_tabla else "Pasa el test Poker")


def testRachas(lista, nivelConfianza):
    cantRachas, cantPositivos, cantNegativos, longitud = 0, 0, 0, len(lista)
    mediana = statistics.median(datosGenerados)

    for i in range(longitud):
        if (lista[i] >= mediana and lista[i-1] < mediana) or (lista[i] < mediana and lista[i-1] >= mediana):
            cantRachas += 1

        if(lista[i]) >= mediana: 
            cantPositivos += 1
        else: 
            cantNegativos += 1
    
    rachasEsperadas = ((2 * cantPositivos * cantNegativos) / longitud) + 1
    desvioEstandar = math.sqrt((2*cantPositivos*cantNegativos * (2*cantPositivos*cantNegativos-longitud)) / ((longitud**2) * (longitud-1)))

    if (desvioEstandar == 0): desvioEstandar = 0.00001
    z = (cantRachas - rachasEsperadas) / desvioEstandar
    
    aux = 1 - (1 - nivelConfianza) / 2
    valorTabla = norm.ppf(aux)

    print('\nTest de rachas')
    print(f"Estadístico obtenido Z: {abs(z)}")
    print(f"Valor crítico: {valorTabla} - Nivel de confianza: {nivelConfianza * 100}%")
    if abs(z) > valorTabla:
        print("La secuencia de números NO es aleatoria")
    else:
        print("Los números son aleatorios")



if __name__ == "__main__":
    nivelConfianza = 0.95
    cantNumeros = 1000
    cantIntervalos = 100 #justificar elección en base a la cantidad de números generados
    
    #generadorGLC
    print('\n\n---Generador Lineal Congruencial---\n')
    datosGenerados = [generadorGLC.next() for _ in range(cantNumeros)]
    testChiCuadrado(datosGenerados, nivelConfianza, cantIntervalos)
    test_poker(datosGenerados, 1-nivelConfianza)
    testRachas(datosGenerados, nivelConfianza)
    testKolmogorovSmirnov(datosGenerados)

    #generadorMediosCuadrados
    print('\n\n---Generador Medios Cuadrados---\n')
    datosGenerados = [generadorMediosCuadrados.next() for _ in range(cantNumeros)]
    testChiCuadrado(datosGenerados, nivelConfianza, cantIntervalos)
    test_poker(datosGenerados, 1-nivelConfianza)
    testRachas(datosGenerados, nivelConfianza)
    testKolmogorovSmirnov(datosGenerados)

    #generadorGCC
    print('\n\n---Generador Cuadrático Congruencial---\n')
    datosGenerados = [generadorGCC.next() for _ in range(cantNumeros)]
    testChiCuadrado(datosGenerados, nivelConfianza, cantIntervalos)
    test_poker(datosGenerados, 1-nivelConfianza)
    testRachas(datosGenerados, nivelConfianza)
    testKolmogorovSmirnov(datosGenerados)

    #generadorPython
    print('\n\n---Generador Lenguaje Python---\n')
    datosGenerados = [random.random() for _ in range(cantNumeros)]
    testChiCuadrado(datosGenerados, nivelConfianza, cantIntervalos)
    test_poker(datosGenerados, 1-nivelConfianza)
    testRachas(datosGenerados, nivelConfianza)
    testKolmogorovSmirnov(datosGenerados)
