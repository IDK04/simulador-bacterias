# A bactéria consiste numa lista com a sua espécie, comida,
# um bool para saber se está ativa e a sua posiçao atual.
def cria_bacteria(especie, comida_inicial_bacteria, linha, coluna):
    return [especie, comida_inicial_bacteria, True, [linha, coluna]]

def especie_bacteria(bacteria):
    return bacteria[0]

def comida_bacteria(bacteria):
    return bacteria[1]

def alimenta_de_bacteria(bacteria):
    bacteria[1] -= 1

def bacteria_ativa(bacteria):
    return bacteria[2]

def desativa_bacteria(bacteria):
    bacteria[2] = False

def altera_posicao(bacteria, linha, coluna):
    bacteria[3] = [linha, coluna]

def posicao_bacteria(bacteria):
    return bacteria[3]
