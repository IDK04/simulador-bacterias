from cap import *
from evento import *
from obsrandom import *
from grelha import *
import matplotlib.pyplot as plt

A = 0
B = 1
C = 2

# Distribui bacterias do tipo "especie" pela grelha e retorna o cap com os
# eventos default de cada bacteria
def distribui_bacterias(especie, n_bacterias, comida_inicial_bacteria, posicoes_livres, grelha, max_celula, cap):
    for i in range(n_bacterias):

        # Se já não houver posições disponiveis
        if (len(posicoes_livres) == 0):
            return cap
        
        linha, coluna = posicoes_livres[unif_random(0, len(posicoes_livres)-1)]
        celula = celula_grelha(grelha, linha, coluna)
        bacteria = cria_bacteria(especie, comida_inicial_bacteria, linha, coluna)
        adiciona_bacteria(celula, bacteria, max_celula)

        cap = adicionar_evento(cap, cria_evento(exp_random(TD), "Deslocamento", bacteria))
        cap = adicionar_evento(cap, cria_evento(exp_random(TR), "Reproducao", bacteria))
        cap = adicionar_evento(cap, cria_evento(exp_random(TA), "Alimentacao", bacteria))
        cap = adicionar_evento(cap, cria_evento(exp_random(TM), "Morte", bacteria))

        # Verifica se a célula já está cheia
        if(celula_cheia(celula, max_celula)):
            posicoes_livres.remove([linha, coluna])

    return cap

def simulador(N, NA, NB, NC, TS, TD, K, TR, TA, TM, TRP, F, Q):

    grelha = cria_grelha(N, 1)

    bacterias_A = [NA]
    bacterias_B = [NB]
    bacterias_C = [NC]

    tempos_A = [0]
    tempos_B = [0]
    tempos_C = [0]

    num_A = NA
    num_B = NB
    num_C = NC

    # Criação das bacterias
    # Lista de posicoes para garantir que tentamos adicionar a uma célula que não está cheia
    posicoes_livres = []
    for i in range(N):
        for j in range(N):
            posicoes_livres.append([i, j])

    cap = criar_cap()
    tempo_atual = 0
    tempo_maximo = TS

    cap = distribui_bacterias(A, NA, F, posicoes_livres, grelha, Q, cap)
    cap = distribui_bacterias(B, NB, F, posicoes_livres, grelha, Q, cap)
    cap = distribui_bacterias(C, NC, F, posicoes_livres, grelha, Q, cap)

    # Inicializa o evento de reposição
    cap = adicionar_evento(cap, cria_evento(exp_random(TM), "Reposicao", 0))

    evento_atual = proximo_evento(cap)
    bacteria_atual = bacteria_evento(evento_atual)
    tempo_atual = tempo_evento(evento_atual)
    cap = elimina_evento(cap)

    while tempo_atual <= tempo_maximo:

        # Bactéria ser diferente de 0 quer dizer que existe bactéria
        # (há um evento que não leva bacteria, sem esta condiçao dava erro)
        if bacteria_atual != 0 and bacteria_ativa(bacteria_atual):
            celula_bacteria = celula_grelha(grelha, linha_bacteria(bacteria_atual), coluna_bacteria(bacteria_atual))
            if tipo_evento(evento_atual) == "Morte":
                remove_bacteria(celula_bacteria, bacteria_atual)
                if especie_bacteria(bacteria_atual) == A:
                    num_A -= 1
                elif especie_bacteria(bacteria_atual) == B:
                    num_B -= 1
                elif especie_bacteria(bacteria_atual) == C:
                    num_C -= 1

            elif tipo_evento(evento_atual) == "Deslocamento":
                desloca_bacteria(grelha, bacteria_atual, K, Q)
                cap = adicionar_evento(cap, cria_evento(tempo_atual+exp_random(TD), "Deslocamento", bacteria_atual))

            elif tipo_evento(evento_atual) == "Alimentacao":
                if especie_bacteria(bacteria_atual) == A:
                    especie_morta = alimenta_a(grelha, bacteria_atual)
                    if especie_morta == A:
                        num_A -= 1
                    elif especie_morta == B:
                        num_B -= 1
                    elif especie_morta == C:
                        num_C -= 1
                else:
                    if alimenta_b_c(grelha, bacteria_atual):
                        # Morreu
                        if especie_bacteria(bacteria_atual) == B:
                            num_B -= 1
                        elif especie_bacteria(bacteria_atual) == C:
                            num_C -= 1

                cap = adicionar_evento(cap, cria_evento(tempo_atual+exp_random(TA), "Alimentacao", bacteria_atual))
            
            elif tipo_evento(evento_atual) == "Reproducao":
                cap, conseguiu_reproduzir = reproduz(bacteria_atual, celula_bacteria, Q, F, cap, tempo_atual, TD, TR, TA, TM)
                if conseguiu_reproduzir:
                    if especie_bacteria(bacteria_atual) == A:
                        num_A += 1
                    elif especie_bacteria(bacteria_atual) == B:
                        num_B += 1
                    elif especie_bacteria(bacteria_atual) == C:
                        num_C += 1

                cap = adicionar_evento(cap, cria_evento(tempo_atual+exp_random(TR), "Reproducao", bacteria_atual))

        # Evento geral
        if bacteria_atual == 0 and tipo_evento(evento_atual) == "Reposicao":
            repoe_alimento(grelha)
            cap = adicionar_evento(cap, cria_evento(tempo_atual+exp_random(TRP), "Reposicao", 0))

        tempos_A.append(tempo_atual)
        tempos_B.append(tempo_atual)
        tempos_C.append(tempo_atual)

        bacterias_A.append(num_A)
        bacterias_B.append(num_B)
        bacterias_C.append(num_C)

        evento_atual = proximo_evento(cap)
        bacteria_atual = bacteria_evento(evento_atual)
        tempo_atual = tempo_evento(evento_atual)
        cap = elimina_evento(cap)

        if(len(cap) == 0):
            break

    plt.plot(tempos_A, bacterias_A, label = 'A')
    plt.plot(tempos_B, bacterias_B, label = 'B')
    plt.plot(tempos_C, bacterias_C, label = 'C')

    plt.xlabel("Tempo")
    plt.ylabel("Numero de bacterias")

    plt.axis([0, TS, 0, 5 + max(max(bacterias_A), max(bacterias_B), max(bacterias_C))])
    plt.legend()
    plt.show()

N = 10
NA = 30
NB = 50
NC = 50
TS = 20
TD = 2
K = 5
TR = 1
TA = 5
TM = 5
TRP = 2
F = 2
Q = 4

simulador(N, NA, NB, NC, TS, TD, K, TR, TA, TM, TRP, F, Q)