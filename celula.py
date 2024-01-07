from bacteria import *

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
        return True
    return False

def remove_bacteria(celula, bacteria):
    celula[0].remove(bacteria)

# Verifica se a celula está cheia
def celula_cheia(celula, max_celula):
    return len(celula[0]) == max_celula

# Tenta reproduzir bacterias
# retorno: True se conseguir reproduzir, False caso contrário
def reproduz(especie, celula, max_celula, comida_inicial_bacteria):
    if(celula_cheia(celula, max_celula)):
        return False
    
    num_bacterias_especie = 0
    for bacteria in celula[0]:
        if(especie_bacteria(bacteria) == especie):
            num_bacterias_especie += 1
    
    bacteria = cria_bacteria(especie, comida_inicial_bacteria)

    if(num_bacterias_especie >= 2):
        adiciona_bacteria(celula, bacteria, max_celula)

    return True