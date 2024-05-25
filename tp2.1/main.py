import generadorGLC
from scipy.stats import chi2

def armarIntervalos(lista, cantidad):
    long = (max(lista) - min(lista)) / cantidad
    intervalos = []
    inicio = min(lista)
    fin = inicio + long

    for x in range(cantidad):
        contador = 0
        for x in range(len(lista)):
            if (lista[x] >= inicio and lista[x] <= fin): #mirar el tema de incluir o no incluir el igual
                contador += 1
        intervalos.append(contador)
        inicio = fin
        fin = fin + long
    return intervalos

def pruebaChiCuadrado(intervalos, cantNumeros, nc):
    #La hipótesis es que todos los números tienen la misma probabilidad de aparecer -> distribución uniforme
    cantIntervalos = len(intervalos)
    frecEsperada = cantNumeros / cantIntervalos

    chiCuadrado = 0
    for x in range(cantIntervalos):
        aux = (intervalos[x] - frecEsperada) ** 2 / frecEsperada
        chiCuadrado += aux

    valorTabla = chi2.ppf(nc, cantIntervalos - 1)
    print()
    print(chiCuadrado)
    print('Prueba de bondad de ajuste chi cuadrado para una distribución uniforme con ' + str(nc) + ' de nivel de confianza')
    print('El generador pasa la prueba') if chiCuadrado < valorTabla else print('El generador no pasa la prueba')


if __name__ == "__main__":
    cantNumeros = 1000
    cantIntervalos = 10
    datosObservados = [generadorGLC.next() for _ in range(cantNumeros)]

    intervalos = armarIntervalos(datosObservados, cantIntervalos)
    nivelConfianza = 0.95
    pruebaChiCuadrado(intervalos, cantNumeros, nivelConfianza)