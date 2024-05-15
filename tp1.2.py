import random
import matplotlib.pyplot as plt
import argparse
import numpy as np

class Ruleta:
    rojo = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    negro = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    
    def __init__(self, min, max):
        self.apuestaMinima = min
        self.apuestaMaxima = max

    def girar(self, seleccion):
        numero = random.randint(0, 36)

        if isinstance(seleccion, int):
            return seleccion == numero
        else:
            match seleccion:
                case 'rojo':
                    return numero in self.rojo
                case 'negro':
                    return numero in self.negro
                case 'par':
                    return numero % 2 == 0 and numero != 0
                case 'impar':
                    return numero % 2 != 0
                case 'doc1':
                    return numero > 0 and numero < 13
                case 'doc2':
                    return numero > 12 and numero < 25
                case 'doc3':
                    return numero > 24 and numero < 37
                case 'col1':
                    return numero % 3 == 1
                case 'col2':
                    return numero % 3 == 2
                case 'col3':
                    return numero % 3 == 0 and numero != 0


class Apuesta:
    def __init__(self, seleccion, multiplicador, estrategia, capital, apuestaMinima):
        self.capital = []
        self.ganadas = [0]
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
            case 'p':
                self.estrategia = Paroli

    def calcularCapital(self, gana):
        nuevoCapital = self.capital[-1] - self.apuestaActual
        g = self.ganadas[-1] * (len(self.ganadas) - 1)
        if gana:
            nuevoCapital = nuevoCapital + self.apuestaActual * self.multiplicador
            g += 1
        
        self.capital.append(nuevoCapital)
        self.ganadas.append(g / len(self.ganadas))
    
    def calcularSigApuesta(self, gana, min, max):
        aux = self.estrategia.calcularSigApuesta(gana, self.apuestaActual, min)
        if aux < min:
            aux = min
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
    def calcularSigApuesta(gana, apuestaActual, apuestaMinima):
        if gana:
            return apuestaActual - apuestaMinima
        else:
            return apuestaActual + apuestaMinima

class Fibonacci:
    nAnterior = 1
    
    def calcularSigApuesta(gana, apuestaActual, apuestaMinima):
        if gana:
            Fibonacci.nAnterior -= 2
            if Fibonacci.nAnterior < 1: Fibonacci.nAnterior = 1
        else:
            Fibonacci.nAnterior += 1
            
        return Fibonacci.calcularTerminoNFib() * apuestaMinima

    def calcularTerminoNFib(): #0 1 1 2 3 5 8 13 21
        if Fibonacci.nAnterior == 1: return 1
        if Fibonacci.nAnterior == 2: return 1
        
        aux1 = 1
        aux2 = 1
        for _ in range(3, Fibonacci.nAnterior + 1):
            aux3 = aux1 + aux2
            aux1 = aux2
            aux2 = aux3
        return aux3

class Paroli:
    contador = 0

    def calcularSigApuesta(gana, apuestaActual, apuestaMinima):
        if gana:
            Paroli.contador += 1
        if (not gana) or Paroli.contador == 3 :
            Paroli.contador = 0
            return apuestaMinima
        else:
            return apuestaActual * 2
        

def generarGraficoLineas(titulo, nro_subplot, ejeX, ejeY, lista, esperado, multiplesListas = False):
    plt.subplot(1, 2, nro_subplot)
    plt.title(titulo)
    plt.xlabel(ejeX)
    plt.ylabel(ejeY)
    aux = 0

    if multiplesListas:
        for x in range(numCorridas):
            plt.plot(lista[x].capital)
            if len(lista[x].capital) > aux: aux = len(lista[x].capital)
    else:
        plt.plot(lista, label = "Capital tirada n")
        aux = len(lista)

    puntosX = np.array([0, aux - 1])
    puntosY = np.array([esperado, esperado])
    plt.plot(puntosX, puntosY, label = "Capital inicial")
    
    plt.legend()
    plt.plot()

def generarGraficoBarras(titulo, nro_subplot, ejeX, ejeY, lista, esperado, multiplesListas = False):
    plt.subplot(1, 2, nro_subplot)
    plt.title(titulo)
    plt.xlabel(ejeX)
    plt.ylabel(ejeY)
    plt.ylim(0, 1)

    if multiplesListas:
        for x in range(numCorridas):
            lista[x].ganadas.pop(0)
            plt.bar(x = np.arange(len(lista[x].ganadas)) + 1, height = lista[x].ganadas)
    else:
        lista.pop(0)
        plt.bar(x = np.arange(len(lista)) + 1, height = lista)
        puntosX = np.array([0, len(lista) + 1])
        puntosY = np.array([esperado, esperado])
        plt.plot(puntosX, puntosY, label = "Valor esperado", color = "darkorange")
        plt.legend()

    plt.plot()

def mostrarGrafico(titulo):
    plt.suptitle(titulo)
    figManager = plt.get_current_fig_manager()
    figManager.resize(1000, 500)
    plt.tight_layout()
    plt.show()

def tipoSeleccion(arg):
        opciones = ['rojo', 'negro', 'par', 'impar', 'docena1', 'docena2', 'docena3', 'col1', 'col2', 'col3']
        if str.lower(arg) in opciones:
            return str.lower(arg)
        elif arg.isdigit() and int(arg) >= 0 and int(arg) <= 36:
            return int(arg)
        raise argparse.ArgumentTypeError('La selección ingresada no es válida')

def tipoCapital(arg):
    if str.lower(arg) == 'i':
        return str.lower(arg)
    elif arg.isdigit() and int(arg) >= 1000:
        return int(arg)
    raise argparse.ArgumentTypeError('El capital ingresado no es válido')

def main():
    if (isinstance(seleccion, int)):
        multiplicador = 36
        frEsperada = 1/37
    elif (seleccion == 'rojo' or seleccion == 'negro' or seleccion == 'par' or seleccion == 'impar'):
        multiplicador = 2
        frEsperada = 18/37
    elif (seleccion == 'doc1' or seleccion == 'doc2' or seleccion == 'doc3' or seleccion == 'col1' or seleccion == 'col2' or seleccion == 'col3'):
        multiplicador = 3
        frEsperada = 12/37


    apuestaMinima = 1000
    apuestaMaxima = False
    capitalObjetivo = 100000

    if (capitalInicial):
        apuestaMaxima = 20000
        capitalObjetivo = capitalInicial * 10

    ruleta = Ruleta(apuestaMinima, apuestaMaxima)
    apuestas = []

    for x in range(numCorridas):
        apuesta = Apuesta(seleccion, multiplicador, estrategia, capitalInicial, apuestaMinima)
        print('\nCorrida ' + str(x))
        i = 1

        while apuesta.apuestaActual != -1 and apuesta.capital[-1] < capitalObjetivo:
            apuestaAnterior = apuesta.apuestaActual
            gana = ruleta.girar(apuesta.seleccion)
            apuesta.calcularCapital(gana)
            apuesta.calcularSigApuesta(gana, ruleta.apuestaMinima, ruleta.apuestaMaxima)
            print('Tirada ' + str(i) + ' - Apostó: ' + str(apuestaAnterior) + ' - Ganó: ' + str(gana) + ' - Nuevo capital: ' + str(apuesta.capital[-1]))
            i+=1
        
        apuestas.append(apuesta)



    numSeleccionada = random.randint(0, numCorridas - 1)

    generarGraficoLineas('Capital', 1, 'n (número de tirada)', 'cc (cantidad de capital)', apuestas[numSeleccionada].capital, capitalInicial)
    generarGraficoBarras('Frecuencia relativa apuesta favorable', 2, 'n (número de tiradas)', 'fr (frecuencia relativa)', apuestas[numSeleccionada].ganadas, frEsperada)
    mostrarGrafico('CORRIDA NÚMERO ' + str(numSeleccionada + 1))

    generarGraficoLineas('Capital', 1, 'n (número de tirada)', 'cc (cantidad de capital)', apuestas, capitalInicial, True)
    generarGraficoBarras('Frecuencia relativa apuesta favorable', 2, 'n (número de tiradas)', 'fr (frecuencia relativa)', apuestas, frEsperada, True)
    mostrarGrafico('MÚLTIPLES CORRIDAS')


    #    print("Ejecutando ruleta.\nNúmero de corridas: " + str(numCorridas) + " - Selección: " + str(seleccion) + " - Estrategia: " + estrategia + " - Capital: " + str(capitalInicial))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--corridas', default=15, type=int, help='Valor del número de corridas (Por defecto: %(default)s)')
    parser.add_argument('-n', '--seleccion', default='rojo', type=tipoSeleccion, help="Selección: un número, \"rojo\", \"negro\", \"par\", \"impar\", \"docena1\", \"docena2\", \"docena3\", \"col1\", \"col2\", \"col3\" (Por defecto: %(default)s)")
    parser.add_argument('-s', '--estrategia', default='m', choices=['m','d','f','p'], help="Estrategia a utilizar: \"m\" - Martingala, \"d\" - D'Alemnert, \"f\" - Fibonacci, \"p\" - Paroli (Por defecto: %(default)s)", )
    parser.add_argument('-a', '--capital', default=30000, type=tipoCapital, help="Capital: \"i\" para infinito o el monto si es finito (Por defecto: %(default)s - Mínimo 1000)")
    args, unknown = parser.parse_known_args()

    numCorridas = args.corridas
    seleccion = args.seleccion
    estrategia = args.estrategia

    if args.capital == 'i':
        capitalInicial = False
    else:
        capitalInicial = args.capital

    print("Ejecutando ruleta.\nNúmero de corridas: " + str(numCorridas) + " - Selección: " + str(seleccion) + " - Estrategia: " + estrategia + " - Capital: " + str(capitalInicial))
    main()