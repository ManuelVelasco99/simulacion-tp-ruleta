import random
import matplotlib.pyplot as plt
import argparse
import numpy as np
import math


def generarGrafico(titulo, ejeX, ejeY, lista1, esperado):
    plt.title(titulo)
    plt.xlabel(ejeX)
    plt.ylabel(ejeY)
    
    lista1.insert(0, 0)
    plt.xlim(1, numero_tiradas + 1)
    plt.plot(lista1)

    puntosX = np.array([1, numero_tiradas])
    puntosY = np.array([esperado, esperado])
    plt.plot(puntosX, puntosY)
    
    plt.plot()
    plt.show()


# === Setear Argumentos
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--corridas", help="Valor del numero de corridas (15 por defecto)", default=15)
parser.add_argument("-t", "--tiradas", help="Valor del numero de tiradas por corrida (2000 por defecto)", default=2000)
parser.add_argument("-n", "--numero", help="Valor del numero a analizar (7 por defecto)", default=7)
args, unknown = parser.parse_known_args()
numero_corridas = int(args.corridas)
numero_tiradas = int(args.tiradas)
numero = int(args.numero)
print("Ejecutando " + str(numero_corridas) + " corridas de " + str(numero_tiradas) + " tiradas para el número " + str(numero))
# ===


# === Generar los valores aleatoreos
corridas = []
for i in range(numero_corridas):
    corridas.append([random.randint(0, 36) for _ in range(int(numero_tiradas))])
# ===

# === Seleccionar una corrida al azar, para mostrar gráficos individuales
num_corrida = random.randint(1, numero_corridas) - 1
corrida_seleccionada = corridas[num_corrida]
# ===

#print(corrida_seleccionada)

# === Generar los valores relativos de la corrida seleccionada
corrida_seleccionada_frecuencia = []

numero_apariciones = 0
for i in range(numero_tiradas):
    if corrida_seleccionada[i] == numero:
        numero_apariciones += 1
    corrida_seleccionada_frecuencia.append(numero_apariciones / (i + 1))
# ===


# === Generar valor promedio de la corrida seleccionada
corrida_seleccionada_promedio = []
total = 0

for i in range(numero_tiradas):
    total += corrida_seleccionada[i]
    corrida_seleccionada_promedio.append(total / (i + 1))
# ===


# === Generar varianza de cada corrida
corrida_seleccionada_varianza = []

for tirada in range(numero_tiradas):
    total = 0
    for i in range(tirada + 1):
        total += (corrida_seleccionada[i] - corrida_seleccionada_promedio[tirada]) ** 2
    corrida_seleccionada_varianza.append(total / (tirada + 1))
# ===


# === Generar desvio estandar de cada corrida
corrida_seleccionada_desvio = []

for tirada in range(numero_tiradas):
    corrida_seleccionada_desvio.append(math.sqrt(corrida_seleccionada_varianza[tirada]))
# ===



# === Generando grafico de la frecuencia relativa respecto del numero de tiradas
valor_esperado_frecuencia = 1/37
generarGrafico('Corrida número ' + str(num_corrida + 1), 'n (número de tiradas)', 'fr (frecuencia relativa)', corrida_seleccionada_frecuencia, valor_esperado_frecuencia)


# === Generando grafico del valor promedio respecto del numero de tiradas
valor_esperado_promedio = 18
generarGrafico('Corrida número ' + str(num_corrida + 1), 'n (número de tiradas)', 'vp (valor promedio de las tiradas)', corrida_seleccionada_promedio, valor_esperado_promedio)


# === Generando grafico de la varianza con respecto del numero de tiradas
generarGrafico('Corrida número ' + str(num_corrida + 1), 'n (número de tiradas)', 'vv (valor de la varianza)', corrida_seleccionada_varianza, 1)


# === Generando grafico del desvio estandar con respecto del numero de tiradas
generarGrafico('Corrida número ' + str(num_corrida + 1), 'n (número de tiradas)', 'vd (valor del desvío)', corrida_seleccionada_desvio, 1)
