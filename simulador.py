from cap import *
from evento import *
from obsrandom import *
from grelha import *

A = 0
B = 1
C = 2

N = 3
NA = 1
NB = 0
NC = 0
TS = 20
TD = 2
K = 5
TR = 1
TA = 5
TM = 5
TRP = 2
F = 2
Q = 4

bacteria = 0
linha = 0
coluna = 0

def distribui_bacterias(especie, n_bacterias, comida_inicial_bacteria, posicoes_livres, grelha, max_celula):
    for i in range(n_bacterias):
        global bacteria
        global linha
        global coluna

        # Se já não houver posições disponiveis
        if (len(posicoes_livres) == 0):
            return grelha
        
        linha, coluna = posicoes_livres[unif_random(0, len(posicoes_livres)-1)]
        celula = celula_grelha(grelha, linha, coluna)
        bacteria = cria_bacteria(especie, comida_inicial_bacteria, linha, coluna)
        adiciona_bacteria(celula, bacteria, max_celula)

        # Verifica se a célula já está cheia
        if(celula_cheia(celula, max_celula)):
            posicoes_livres.remove([linha, coluna])

grelha = cria_grelha(N, 1)
# Criação das bacterias
# Lista de posicoes para garantir que tentamos adicionar a uma célula que não está cheia
posicoes_livres = []
for i in range(N):
    for j in range(N):
        posicoes_livres.append([i, j])

distribui_bacterias(A, NA, F, posicoes_livres, grelha, Q)
distribui_bacterias(B, NB, F, posicoes_livres, grelha, Q)
distribui_bacterias(C, NC, F, posicoes_livres, grelha, Q)

for i in range(N):
    for j in range(N):
        print(grelha[i][j][0], end=' ')
    print()
