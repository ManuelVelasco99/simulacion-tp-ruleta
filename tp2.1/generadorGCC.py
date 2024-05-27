divisor = 2**32                 #m
multiplicador = 1013904223      #a
incremento = 1664525            #c
semilla = 456


def setSeed(nuevaSemilla):
    global semilla
    semilla = nuevaSemilla

def next():
    global semilla
    semilla = (multiplicador * semilla * semilla + incremento) % divisor
    return semilla

