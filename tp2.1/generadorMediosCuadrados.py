import testsAleatoriedad


def obtener_valores_centrales(num):
    str_number = str(num)
    length = len(str_number)
    
    if length < 4:
        return str_number
    
    start_index = length // 2 - 2
    end_index = start_index + 4
    
    return str_number[start_index:end_index]


semilla = 92458139658673422
#semilla = 1931
numerosGenerados = []
categorias = 10

for i in range(50):
    valor = semilla**2
    nuevaSemilla = int(obtener_valores_centrales(valor))
    semilla = nuevaSemilla
    numerosGenerados.append(semilla)

testsAleatoriedad.ejecutar_test_chi_cuadrado(numerosGenerados)
testsAleatoriedad.test_poker(numerosGenerados, 0.025)