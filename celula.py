from bacteria import *
from evento import *
from cap import *
from obsrandom import *

# A célula consiste numa lista com uma lista de bactérias e comida
def cria_celula(comida_inicial_celula):
    return [[], comida_inicial_celula]

def comida_celula(celula):
    return celula[1]

def bacterias_celula(celula):
    return celula[0]

def alimenta_de_celula(celula):
    celula[1]-=1

def repoe_celula(celula):
    celula[1] = 1

# Tenta adicionar uma bactéria à celula.
# retorno: True se conseguir adicionar, False caso contrario
def adiciona_bacteria(celula, bacteria, max_celula):
    if(not celula_cheia(celula, max_celula)):
        celula[0].append(bacteria)
        ativa_bacteria(bacteria)
        return True
    desativa_bacteria(bacteria)
    return False

def remove_bacteria(celula, bacteria):
    lista_bacterias = celula[0]
    celula[0] = []
    for bact in lista_bacterias:
        if bact is bacteria:
            desativa_bacteria(bacteria)
        else:
            celula[0].append(bact)

# Verifica se a celula está cheia
def celula_cheia(celula, max_celula):
    return len(celula[0]) == max_celula

# Tenta reproduzir bacterias
def reproduz(bacteria_pai, celula, max_celula, comida_inicial_bacteria, cap, tempo_atual, TD, TR, TA, TM):
    if(celula_cheia(celula, max_celula)):
        return cap, False
    
    especie = especie_bacteria(bacteria_pai)
    
    num_bacterias_especie = 0
    for bacteria in celula[0]:
        if(especie_bacteria(bacteria) == especie):
            num_bacterias_especie += 1
    
    bacteria = cria_bacteria(especie, comida_inicial_bacteria, linha_bacteria(bacteria_pai),coluna_bacteria(bacteria_pai))

    if(num_bacterias_especie >= 2):
        adiciona_bacteria(celula, bacteria, max_celula)
        cap = adicionar_evento(cap, cria_evento(exp_random(TD)+tempo_atual, "Deslocamento", bacteria))
        cap = adicionar_evento(cap, cria_evento(exp_random(TR)+tempo_atual, "Reproducao", bacteria))
        cap = adicionar_evento(cap, cria_evento(exp_random(TA)+tempo_atual, "Alimentacao", bacteria))
        cap = adicionar_evento(cap, cria_evento(exp_random(TM)+tempo_atual, "Morte", bacteria))

        return cap, True

    return cap, False