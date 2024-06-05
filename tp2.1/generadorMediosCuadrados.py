semilla = 9731

def obtener_valores_centrales(num):
    str_number = str(num)
    length = len(str_number)
    
    if length < 4:
        return str_number
    
    start_index = length // 2 - 2
    end_index = start_index + 4
    
    return str_number[start_index:end_index]

def setSeed(nuevaSemilla):
    global semilla
    semilla = nuevaSemilla

def random():
    global semilla
    valor = semilla**2
    # agrega ceros al inicio si hay menos de 8 digitos
    if(len(str(valor)) < 8):
        while(len(str(valor)) < 8): 
            valor = "0" + str(valor)
        
    semilla = int(obtener_valores_centrales(valor))
    return float('0.' + str(semilla))
