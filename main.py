import random
import matplotlib.pyplot as plt
import argparse

# === Setear Argumentos
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--corridas", help="Valor del numero de corridas (3 por defecto)", default=3)
parser.add_argument("-t", "--tiradas", help="Valor del numero de tiradas por corrida (2000 por defecto)", default=2000)
parser.add_argument("-n", "--numero", help="Valor del numero a analizar (7 por defecto)", default=7)
args, unknown = parser.parse_known_args()
numero_corridas = int(args.corridas)
numero_tiradas = int(args.tiradas)
numero = int(args.numero)
print("Ejecutando " + str(numero_corridas) + " corridas de " + str(numero_tiradas) + " tiradas para el número " + str(
    numero))
# ===


# === Generar los valores aleatoreos
corridas = []
for i in range(0, int(numero_corridas)):
    corridas.append([random.randint(0, 36) for _ in range(int(numero_tiradas))])
# ===

# === Generar los valores relativos de cada corrida
corridas_relativas = []
for i in corridas:
    corrida_relativa = []
    numero_apariciones = 0
    for j in range(0, len(i)):
        if i[j] == int(numero):
            numero_apariciones += 1
        corrida_relativa.append(numero_apariciones / int(numero_tiradas))
    corridas_relativas.append(corrida_relativa)
# ===

# === Generar el valor esperado de las corridas
valor_esperado = []
for i in range(0, numero_tiradas):
    valor_esperado.append((1/37))
# ===

# === Generar valor promedio de cada corrida
corridas_valor_promedio = []
for i in corridas:
    corrida = i
    corrida_valor_promedio=[]
    for j in range(0, numero_tiradas):
        total = 0
        for h in range(0, j):
            total += corrida[h]
        corrida_valor_promedio.append(total / (j + 1))
    corridas_valor_promedio.append(corrida_valor_promedio)
# ===

# === Generar valor promedio esperado de las corridas
valor_promedio_esperado = []
valores_posibles = []
for i in range(0,37):
    valores_posibles.append(i)
total = 0
for valor in valores_posibles:
    total = total + valor
for i in range(0,numero_tiradas):
    valor_promedio_esperado.append(total/valores_posibles.__len__())
# ===

# === Generando grafico de la frecuencia relativa respecto del numero de tiradas para cada corrida
for corrida_relativa in corridas_relativas:
    plt.plot(corrida_relativa)
    plt.plot(valor_esperado)
    plt.show()
# ===

# === Generando grafico del valor promedio respecto del numero de tiradas para cada corrida
for corrida_valor_promedio in corridas_valor_promedio:
    plt.plot(corrida_valor_promedio)
    plt.plot(valor_promedio_esperado)
    plt.show()
# ===


