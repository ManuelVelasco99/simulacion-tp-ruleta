divisor = 2**31 - 1                 #m
multiplicador = 1103515245      #a
incremento = 12345            #c
semilla = 795489


def setSeed(nuevaSemilla):
    global semilla
    semilla = nuevaSemilla

def random():
    global semilla
    semilla = (multiplicador * semilla * semilla + incremento) % divisor
    return semilla / divisor
