import generadorGLC, generadorGCC, generadorMediosCuadrados
from scipy.stats import chi2, norm
import scipy.stats as ss
import statistics, math, random
import matplotlib.pyplot as plt
import numpy as np


def armarIntervalos(lista, cantidad):
    long = 1 / cantidad #los numeros pertenecen al intervalo [0, 1)
    inicio = 0
    fin = inicio + long
    intervalos = []

    for _ in range(cantidad):
        contador = 0
        for x in range(len(lista)):
            if (lista[x] >= inicio and lista[x] < fin):
                contador += 1

        intervalos.append(contador)
        inicio = fin
        fin = fin + long

    return intervalos

def testChiCuadrado(lista, nc, cantIntervalos):
    #La hipótesis es que todos los números tienen la misma probabilidad de aparecer -> distribución uniforme
    cantNumeros = len(lista)
    intervalos = armarIntervalos(datosGenerados, cantIntervalos)
    frecEsperada = cantNumeros / cantIntervalos

    chiCuadrado = 0
    for x in range(cantIntervalos):
        aux = (intervalos[x] - frecEsperada) ** 2 / frecEsperada
        chiCuadrado += aux

    valorTabla = chi2.ppf(nc, cantIntervalos - 1)

    print('Prueba de bondad de ajuste chi cuadrado para distribución uniforme')
    print(f"Estadístico obtenido: {chiCuadrado}")
    print(f"Valor crítico: {valorTabla} - Nivel de confianza: {nc * 100}%")
    print('Resultado: El generador pasa la prueba') if chiCuadrado < valorTabla else print('Resultado: El generador NO pasa la prueba')
    return intervalos

def testKolmogorovSmirnov(lista):
    media, desvio = ss.norm.fit(lista)
    kstest = ss.kstest(lista,"norm",args=(media, desvio))

    print('\nTest de Bondad Kolmogorov-Smirnov para distribución normal')
    significacion = (1 - kstest.pvalue) * 100
    print(f"Nivel de significacion: {significacion}%")
 
    if kstest.pvalue < 0.01:
        print('Los números son independientes')
    else:
        print('Los números NO son independientes')

def testPoker(numeros, a):
    frecObsTrio, frecObsUnPar, frecObsTodasDistintas = 0, 0, 0
    secuencia = []
    grupo = []

    for x in range(len(numeros)):
        aux = str(numeros[x])[2]
        grupo.append(int(aux))
        if (x % 3 == 2):
            secuencia.append(grupo)
            grupo = []

    frecEspTrio = 0.01 * len(secuencia)
    frecEspUnPar = 0.27 * len(secuencia)
    frecEspTodasDistintas = 0.72 * len(secuencia)
    
    

    for grupo in secuencia:
        if grupo[0] == grupo[1] and grupo[1] == grupo[2]:
            frecObsTrio += 1
        elif grupo[0] == grupo[1] or grupo[1] == grupo[2] or grupo[0] == grupo[2]:
            frecObsUnPar += 1
        else:
            frecObsTodasDistintas += 1
        

    # Calcula la estadística chi-cuadrado para cada mano de póker
    chiCuadradoTrio = (frecObsTrio - frecEspTrio) ** 2 / frecEspTrio
    chiCuadradoUnPar = (frecObsUnPar - frecEspUnPar) ** 2 / frecEspUnPar
    chiCuadradoTodasDistintas = (frecObsTodasDistintas - frecEspTodasDistintas) ** 2 / frecEspTodasDistintas
    
    # Calcular la estadística de chi-cuadrado total.
    chiCuadrado = chiCuadradoTrio + chiCuadradoUnPar + chiCuadradoTodasDistintas
    valorTabla = chi2.ppf(1 - a, 2) #los grados de libertad provienen de las manos de 3 numeros y 3 posibilidades (menos 1)

    print('\nTest de Poker formando manos de 3 elementos')
    print(f"Estadístico obtenido: {chiCuadrado}")
    print(f"Valor crítico: {valorTabla} - Nivel de confianza: {(1-a) * 100}%")
    print('Resultado: El generador pasa el test') if chiCuadrado < valorTabla else print('Resultado: El generador NO pasa el test')


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

    print('\nTest de rachas según mediana')
    print(f"Estadístico obtenido Z: {abs(z)}")
    print(f"Valor crítico: {valorTabla} - Nivel de confianza: {nivelConfianza * 100}%")
    if abs(z) > valorTabla:
        print("La secuencia de números NO es aleatoria")
    else:
        print("Los números son aleatorios")


def generarGraficoXY(lista, nroSubplot):
    plt.subplot(1, 2, nroSubplot)
    puntosX = list(range(len(lista)))
    plt.scatter(puntosX, lista)
    plt.title('Dispersión Valores Pseudoaleatorios')
    plt.xlabel('N° de ejecución')
    plt.ylabel('N° obtenido')
    plt.plot()

def generarGraficoBarras(lista, nro_subplot, esperado):
    plt.subplot(1, 2, nro_subplot)
    plt.bar(x = np.arange(len(lista)) + 1, height = lista)
    puntosX = np.array([1, len(lista)])
    puntosY = np.array([esperado, esperado])
    plt.plot(puntosX, puntosY, label = "Valor esperado", color = "darkorange")
    plt.title('Frecuencias Absolutas de 100 Intervalos')
    plt.legend()
    plt.xlabel('N° de intervalo')
    plt.ylabel('Frecuencia absoluta')
    plt.plot()


def mostrarGrafico(titulo):
    plt.suptitle(titulo)
    figManager = plt.get_current_fig_manager()
    figManager.resize(1000, 500)
    plt.tight_layout()
    plt.show()


def testearGenerador(generador, nombre):
    global datosGenerados
    print(f"\n\n---{nombre}---\n")
    datosGenerados = [generador.random() for _ in range(cantNumeros)]
    intervalos = testChiCuadrado(datosGenerados, nivelConfianza, cantIntervalos)
    testPoker(datosGenerados, 1-nivelConfianza)
    testRachas(datosGenerados, nivelConfianza)
    testKolmogorovSmirnov(datosGenerados)
    generarGraficoXY(datosGenerados, 1)
    generarGraficoBarras(intervalos, 2, len(datosGenerados)/cantIntervalos)
    mostrarGrafico(nombre)


if __name__ == "__main__":
    nivelConfianza = 0.95
    cantNumeros = 1000
    cantIntervalos = 100 #justificar elección en base a la cantidad de números generados
    datosGenerados = []
    
    testearGenerador(generadorGLC, 'Generador Lineal Congruencial')    
    testearGenerador(generadorMediosCuadrados, 'Generador Medios Cuadrados')
    testearGenerador(generadorGCC, 'Generador Cuadrático Congruencial')
    testearGenerador(random, 'Generador Lenguaje Python')
