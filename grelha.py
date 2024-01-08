from celula import *
from bacteria import *
from obsrandom import *

A = 0
B = 1
C = 2

# A grelha consiste numa matriz de células
def cria_grelha(tamanho_grelha, comida_inicial_celula):
    grelha = []
    for i in range(tamanho_grelha): 
        linha = []
        for j in range(tamanho_grelha):
            linha.append(cria_celula(comida_inicial_celula))
        grelha.append(linha)

    return grelha

def repoe_alimento(grelha):
    for i in range(len(grelha)): 
        for j in range(len(grelha)):
            repoe_celula(grelha[i][j])

# Desloca uma bacteria
# retorno: True se conseguiu deslocar, False caso contrário
def desloca_bacteria(grelha, bacteria, deslocamento_maximo, max_celula):
    deslocamento_linha = unif_random(-deslocamento_maximo, deslocamento_maximo)
    deslocamento_coluna = unif_random(-deslocamento_maximo, deslocamento_maximo)

    linha = linha_bacteria(bacteria)
    coluna = coluna_bacteria(bacteria)
    nova_linha = (linha + deslocamento_linha) % len(grelha)
    nova_coluna = (coluna + deslocamento_coluna) % len(grelha)

    nova_celula = grelha[nova_linha][nova_coluna]
    if celula_cheia(nova_celula, max_celula) or (linha==nova_linha and coluna==nova_coluna):
        return False

    remove_bacteria(grelha[linha][coluna], bacteria)
    altera_posicao(bacteria, nova_linha, nova_coluna)
    adiciona_bacteria(nova_celula, bacteria, max_celula)

    return True

# Alimenta as bactérias de tipo A
# retorna a espécie morta
def alimenta_a(grelha, bacteria):
    linha = coluna_bacteria(bacteria)
    coluna = coluna_bacteria(bacteria)
    celula = grelha[linha][coluna]
    bacterias_b_c = []
    for bact in bacterias_celula(celula):
        if especie_bacteria(bact) == B or especie_bacteria(bact) == C:
            bacterias_b_c.append(bact)
    
    if len(bacterias_b_c) >= 1:
        bacteria_alimento = bacterias_b_c[unif_random(0, len(bacterias_b_c)-1)]
        remove_bacteria(celula, bacteria_alimento)
        return especie_bacteria(bacteria_alimento)
    
    if(comida_bacteria(bacteria)>=1):
        alimenta_de_bacteria(bacteria)
        return -1
    
    remove_bacteria(celula, bacteria)
    return A

# Alimenta as bactérias B e C
# retorna True se morreu, False caso contrario
def alimenta_b_c(grelha, bacteria):
    linha = coluna_bacteria(bacteria)
    coluna = coluna_bacteria(bacteria)
    celula = grelha[linha][coluna]
    if (comida_celula(celula) >= 1):
        alimenta_de_celula(celula)
        return False
    
    if(comida_bacteria(bacteria)>=1):
        alimenta_de_bacteria(bacteria)
        return False
    
    remove_bacteria(celula, bacteria)
    return True

# Retorna uma celula  
def celula_grelha(grelha, linha, coluna):
    return grelha[linha][coluna]
