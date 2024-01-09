import celula as cel
import bacteria as bct
import obsrandom 

A = 0
B = 1
C = 2

# A grelha consiste numa matriz de células
def cria_grelha(tamanho_grelha, comida_inicial_celula):
    grelha = []
    for i in range(tamanho_grelha): 
        linha = []
        for j in range(tamanho_grelha):
            linha.append(cel.cria_celula(comida_inicial_celula))
        grelha.append(linha)

    return grelha

def repoe_alimento(grelha):
    for i in range(len(grelha)): 
        for j in range(len(grelha)):
            cel.repoe_celula(grelha[i][j])

# Desloca uma bacteria
# retorno: True se conseguiu deslocar, False caso contrário
def desloca_bacteria(grelha, bacteria, deslocamento_maximo, max_celula):
    deslocamento_linha = obsrandom.unif_random(-deslocamento_maximo, deslocamento_maximo)
    deslocamento_coluna = obsrandom.unif_random(-deslocamento_maximo, deslocamento_maximo)

    linha = bct.linha_bacteria(bacteria)
    coluna = bct.coluna_bacteria(bacteria)
    nova_linha = (linha + deslocamento_linha) % len(grelha)
    nova_coluna = (coluna + deslocamento_coluna) % len(grelha)

    nova_celula = grelha[nova_linha][nova_coluna]
    if cel.celula_cheia(nova_celula, max_celula) or (linha==nova_linha and coluna==nova_coluna):
        return False

    cel.remove_bacteria(grelha[linha][coluna], bacteria)
    bct.altera_posicao(bacteria, nova_linha, nova_coluna)
    cel.adiciona_bacteria(nova_celula, bacteria, max_celula)

    return True

# Alimenta as bactérias de tipo A
# retorna a espécie morta
def alimenta_a(grelha, bacteria):
    linha = bct.linha_bacteria(bacteria)
    coluna = bct.coluna_bacteria(bacteria)
    celula = grelha[linha][coluna]
    bacterias_b_c = []
    for bact in cel.bacterias_celula(celula):
        if bct.especie_bacteria(bact) == B or bct.especie_bacteria(bact) == C:
            bacterias_b_c.append(bact)
    
    if len(bacterias_b_c) >= 1:
        bacteria_alimento = bacterias_b_c[obsrandom.unif_random(0, len(bacterias_b_c)-1)]
        cel.remove_bacteria(celula, bacteria_alimento)
        return bct.especie_bacteria(bacteria_alimento)
    
    if(bct.comida_bacteria(bacteria)>=1):
        bct.alimenta_de_bacteria(bacteria)
        return -1
    
    cel.remove_bacteria(celula, bacteria)
    return A

# Alimenta as bactérias B e C
# retorna True se morreu, False caso contrario
def alimenta_b_c(grelha, bacteria):
    linha = bct.linha_bacteria(bacteria)
    coluna = bct.coluna_bacteria(bacteria)
    celula = grelha[linha][coluna]
    if (cel.comida_celula(celula) >= 1):
        cel.alimenta_de_celula(celula)
        return False
    
    if(bct.comida_bacteria(bacteria)>=1):
        bct.alimenta_de_bacteria(bacteria)
        return False
    
    cel.remove_bacteria(celula, bacteria)
    return True

# Retorna uma celula  
def celula_grelha(grelha, linha, coluna):
    return grelha[linha][coluna]
