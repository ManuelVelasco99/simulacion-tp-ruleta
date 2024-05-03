import random
import matplotlib.pyplot as plt
import argparse
import numpy as np


class Ruleta:
    rojo = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    negro = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    primeraColumna = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
    segundaColumna = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
    terceraColumna = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
    
    def __init__(self, min, max):
        self.apuestaMinima = min
        self.apuestaMaxima = max

    def girar(self, seleccion):
        numero = random.randint(0, 36)

        if isinstance(seleccion, int):
            return seleccion == numero
        elif seleccion == 'rojo':
            return numero in self.rojo
        elif seleccion == 'negro':
            return numero in self.negro
        #seguir con las opciones. Para par o impar y las docenas no hace falta hacer lista, se puede calcular


class Apuesta:
    capital = []
    def __init__(self, seleccion, multiplicador, estrategia, capital, apuestaMinima):
        self.seleccion = seleccion
        self.multiplicador = multiplicador
        self.capital.append(capital)
        self.apuestaActual = apuestaMinima

        match (estrategia):
            case 'm':
                self.estrategia = Martingala
            case 'd':
                self.estrategia = Dalembert
            case 'f':
                self.estrategia = Fibonacci
            case 'o':
                self.estrategia = Otra

    def calcularCapital(self, gana):
        nuevoCapital = self.capital[-1] - self.apuestaActual
        if gana:
            nuevoCapital = nuevoCapital + self.apuestaActual * self.multiplicador
        
        self.capital.append(nuevoCapital)
    
    def calcularSigApuesta(self, gana, min, max):
        aux = self.estrategia.calcularSigApuesta(gana, self.apuestaActual, min)
        if max:
            if (aux > max):
                aux = max

            if self.capital[-1] >= aux:
                self.apuestaActual = aux
            elif self.capital[-1] > 0:
                self.apuestaActual = self.capital[-1]
            else:
                self.apuestaActual = -1
        else:
            self.apuestaActual = aux


class Martingala:
    def calcularSigApuesta(gana, apuestaActual, apuestaMinima):
        if gana:
            return apuestaMinima
        else:
            return apuestaActual * 2

class Dalembert:
    pass

class Fibonacci:
    pass

class Otra:
    pass



def generarGrafico(titulo, nro_subplot, ejeX, ejeY, lista1, esperado):
    plt.subplot(1, 2, nro_subplot)
    plt.title(titulo)
    plt.xlabel(ejeX)
    plt.ylabel(ejeY)

    
    lista1.insert(0, 0)
    plt.xlim(1, len(lista1) + 1)
    plt.plot(lista1, label = "Capital tirada n")

    puntosX = np.array([1, len(lista1)])
    puntosY = np.array([esperado, esperado])
    plt.plot(puntosX, puntosY, label = "Capital inicial")
    
    plt.legend()
    plt.plot()


#region === Setear Argumentos
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--corridas", help="Valor del numero de corridas (15 por defecto)", default=15)
parser.add_argument("-n", "--seleccion", help="Selección: un número, \"rojo\", \"negro\", ... - rojo por defecto", default='rojo')
parser.add_argument("-s", "--estrategia", help="Estrategia a utilizar: \"m\" - Martingala, \"d\" - D'Alemnert, \"f\" - Fibonacci, \"o\" - Definir otra - m por defecto", default='m')
parser.add_argument("-a", "--capital", help="Capital: \"i\" para infinito o el monto si es finito - 30000 por defecto", default=30000)
args, unknown = parser.parse_known_args()

numCorridas = int(args.corridas)
seleccion = args.seleccion
estrategia = args.estrategia

if isinstance(seleccion, int):
    seleccion = int(seleccion)

if isinstance(args.capital, int): 
    capitalInicial = int(args.capital)
else:
    capitalInicial = False

print("Ejecutando ruleta.\nNúmero de corridas: " + str(numCorridas) + " - Selección: " + str(seleccion) + " - Estrategia: " + estrategia + " - Capital: " + str(capitalInicial))
#endregion



multiplicador = 2 #crear método para asignarlo dinámicamente

apuestaMinima = 1000
apuestaMaxima = False
capitalObjetivo = 100000

if (capitalInicial):
    apuestaMaxima = 20000
    capitalObjetivo = capitalInicial * 10


ruleta = Ruleta(apuestaMinima, apuestaMaxima)
apuesta = Apuesta(seleccion, multiplicador, estrategia, capitalInicial, apuestaMinima)

i = 1

while apuesta.apuestaActual != -1 and apuesta.capital[-1] < capitalObjetivo:
    apuestaAnterior = apuesta.apuestaActual
    gana = ruleta.girar(apuesta.seleccion)
    apuesta.calcularCapital(gana)
    apuesta.calcularSigApuesta(gana, ruleta.apuestaMinima, ruleta.apuestaMaxima)
    print('Tirada ' + str(i) + ' - Apostó: ' + str(apuestaAnterior) + ' - Ganó: ' + str(gana) + ' - Nuevo capital: ' + str(apuesta.capital[-1]))
    i+=1




generarGrafico('Capital', 1, 'n (número de tirada)', 'cc (cantidad de capital)', apuesta.capital, capitalInicial)

#plt.suptitle('CORRIDA NÚMERO ' + str(num_corrida + 1))

figManager = plt.get_current_fig_manager()
figManager.resize(1000, 500)
plt.tight_layout()
plt.show()