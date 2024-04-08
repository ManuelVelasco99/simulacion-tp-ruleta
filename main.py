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
    plt.plot(lista1, label = "Valor obtenido")

    puntosX = np.array([1, numero_tiradas])
    puntosY = np.array([esperado, esperado])
    plt.plot(puntosX, puntosY, label = "Valor esperado")
    
    plt.legend()
    plt.plot()
    plt.show()


#region === Setear Argumentos
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--corridas", help="Valor del numero de corridas (15 por defecto)", default=15)
parser.add_argument("-t", "--tiradas", help="Valor del numero de tiradas por corrida (2000 por defecto)", default=2000)
parser.add_argument("-n", "--numero", help="Valor del numero a analizar (7 por defecto)", default=7)
args, unknown = parser.parse_known_args()
numero_corridas = int(args.corridas)
numero_tiradas = int(args.tiradas)
numero = int(args.numero)
print("Ejecutando " + str(numero_corridas) + " corridas de " + str(numero_tiradas) + " tiradas para el número " + str(numero))
#endregion


#region === Generar los valores aleatorios
corridas = []
for i in range(numero_corridas):
    corridas.append([random.randint(0, 36) for _ in range(int(numero_tiradas))])
#endregion


#region === Seleccionar una corrida al azar, para mostrar gráficos individuales
num_corrida = random.randint(1, numero_corridas) - 1
corrida_seleccionada = corridas[num_corrida]
#endregion

#print(corridas[0])
#print(corridas[1])
#print(corridas[2])

#region === Generar valores frecuencia relativa
general_frecuencia = []
apariciones = 0

for i in range(numero_tiradas):
    for c in corridas:
        if c[i] == numero:
            apariciones += 1
    
    general_frecuencia.append(apariciones / ((i + 1) * numero_corridas))


corrida_seleccionada_frecuencia = []
apariciones = 0

for i in range(numero_tiradas):
    if corrida_seleccionada[i] == numero:
        apariciones += 1
    corrida_seleccionada_frecuencia.append(apariciones / (i + 1))
#endregion


#region === Generar valores promedio
general_promedio = []
corridas_promedios = []
total = 0

for i in range(numero_tiradas):
    for c in corridas:
        total += c[i]
    general_promedio.append(total / ((i + 1) * numero_corridas))


for c in corridas:
    aux = []
    total = 0
    for i in range(numero_tiradas):
        total += c[i]
        aux.append(total / (i + 1))
    corridas_promedios.append(aux)


corrida_seleccionada_promedio = corridas_promedios[num_corrida]
#endregion


#region === Generar valores varianza
general_varianza = []

for tirada in range(numero_tiradas):
    total = 0
    for c in corridas:
        for i in range(tirada + 1):
            total += (c[i] - corridas_promedios[corridas.index(c)][tirada]) ** 2
            a = 1
    
    general_varianza.append(total / ((tirada + 1) * numero_corridas))


corrida_seleccionada_varianza = []

for tirada in range(numero_tiradas):
    total = 0
    for i in range(tirada + 1):
        total += (corrida_seleccionada[i] - corrida_seleccionada_promedio[tirada]) ** 2
    corrida_seleccionada_varianza.append(total / (tirada + 1))
#endregion


# === Generar valores desvio estandar
general_desvio = []

for tirada in range(numero_tiradas):
    general_desvio.append(math.sqrt(general_varianza[tirada]))


corrida_seleccionada_desvio = []

for tirada in range(numero_tiradas):
    corrida_seleccionada_desvio.append(math.sqrt(corrida_seleccionada_varianza[tirada]))
# ===


#region Gráficos
valor_esperado_frecuencia = 1/37
generarGrafico('Frecuencia relativa - Corrida número ' + str(num_corrida + 1), 'n (número de tiradas)', 'fr (frecuencia relativa)', corrida_seleccionada_frecuencia, valor_esperado_frecuencia)

valor_esperado_promedio = 18
generarGrafico('Valor promedio - Corrida número ' + str(num_corrida + 1), 'n (número de tiradas)', 'vp (valor promedio de las tiradas)', corrida_seleccionada_promedio, valor_esperado_promedio)

valor_esperado_varianza = ((36 - 0 + 1) ** 2 - 1) / 12
generarGrafico('Varianza - Corrida número ' + str(num_corrida + 1), 'n (número de tiradas)', 'vv (valor de la varianza)', corrida_seleccionada_varianza, valor_esperado_varianza)

valor_esperado_desvio = math.sqrt(((36 - 0 + 1) ** 2 - 1) / 12)
generarGrafico('Desvío estándar - Corrida número ' + str(num_corrida + 1), 'n (número de tiradas)', 'vd (valor del desvío)', corrida_seleccionada_desvio, valor_esperado_desvio)

generarGrafico('Frecuencia relativa - Promedio de todas las corridas', 'n (número de tiradas)', 'fr (frecuencia relativa)', general_frecuencia, valor_esperado_frecuencia)

generarGrafico('Valor promedio - Promedio de todas las corridas', 'n (número de tiradas)', 'vp (valor promedio de las tiradas)', general_promedio, valor_esperado_promedio)

generarGrafico('Varianza - Promedio de todas las corridas', 'n (número de tiradas)', 'vv (valor de la varianza)', general_varianza, valor_esperado_varianza)

generarGrafico('Desvío estándar - Promedio de todas las corridas', 'n (número de tiradas)', 'vd (valor del desvío)', general_desvio, valor_esperado_desvio)

#endregion