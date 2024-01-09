import cap as cp
import evento
import obsrandom
import grelha as gr
import bacteria as bct
import celula as cel
import matplotlib.pyplot as plt

A = 0
B = 1
C = 2

# Distribui bacterias do tipo "especie" pela grelha e retorna o cap com os
# eventos default de cada bacteria
def distribui_bacterias(especie, n_bacterias, comida_inicial_bacteria, posicoes_livres, grelha, max_celula, cap, id_atual):
    for i in range(n_bacterias):

        # Se já não houver posições disponiveis
        if (len(posicoes_livres) == 0):
            return cap
        
        linha, coluna = posicoes_livres[obsrandom.unif_random(0, len(posicoes_livres)-1)]
        celula = gr.celula_grelha(grelha, linha, coluna)
        bacteria = bct.cria_bacteria(especie, comida_inicial_bacteria, linha, coluna, id_atual)
        id_atual += 1
        cel.adiciona_bacteria(celula, bacteria, max_celula)

        cap = cp.adicionar_evento(cap, evento.cria_evento(obsrandom.exp_random(TD), "Deslocamento", bacteria))
        cap = cp.adicionar_evento(cap, evento.cria_evento(obsrandom.exp_random(TR), "Reproducao", bacteria))
        cap = cp.adicionar_evento(cap, evento.cria_evento(obsrandom.exp_random(TA), "Alimentacao", bacteria))
        cap = cp.adicionar_evento(cap, evento.cria_evento(obsrandom.exp_random(TM), "Morte", bacteria))

        # Verifica se a célula já está cheia
        if(cel.celula_cheia(celula, max_celula)):
            posicoes_livres.remove([linha, coluna])

    return cap

def simulador(N, NA, NB, NC, TS, TD, K, TR, TA, TM, TRP, F, Q):

    id_atual = 0

    grelha = gr.cria_grelha(N, 1)

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

    cap = cp.criar_cap()
    tempo_atual = 0
    tempo_maximo = TS

    cap = distribui_bacterias(A, NA, F, posicoes_livres, grelha, Q, cap, id_atual)
    id_atual += NA+1
    cap = distribui_bacterias(B, NB, F, posicoes_livres, grelha, Q, cap, id_atual)
    id_atual += NB +1
    cap = distribui_bacterias(C, NC, F, posicoes_livres, grelha, Q, cap, id_atual)
    id_atual += NC + 1

    # Inicializa o evento de reposição
    cap = cp.adicionar_evento(cap, evento.cria_evento(obsrandom.exp_random(TM), "Reposicao", 0))

    evento_atual = cp.proximo_evento(cap)
    bacteria_atual = evento.bacteria_evento(evento_atual)
    tempo_atual = evento.tempo_evento(evento_atual)
    cap = cp.elimina_evento(cap)

    while tempo_atual <= tempo_maximo and len(cap)>0:

        # Bactéria ser diferente de 0 quer dizer que existe bactéria
        # (há um evento que não leva bacteria, sem esta condiçao dava erro)
        if bacteria_atual != 0 and bct.bacteria_ativa(bacteria_atual):
            celula_bacteria = gr.celula_grelha(grelha, bct.linha_bacteria(bacteria_atual), bct.coluna_bacteria(bacteria_atual))
            if evento.tipo_evento(evento_atual) == "Morte":
                cel.remove_bacteria(celula_bacteria, bacteria_atual)
                if bct.especie_bacteria(bacteria_atual) == A:
                    num_A -= 1
                elif bct.especie_bacteria(bacteria_atual) == B:
                    num_B -= 1
                elif bct.especie_bacteria(bacteria_atual) == C:
                    num_C -= 1

            elif evento.tipo_evento(evento_atual) == "Deslocamento":
                gr.desloca_bacteria(grelha, bacteria_atual, K, Q)
                cap = cp.adicionar_evento(cap, evento.cria_evento(tempo_atual+obsrandom.exp_random(TD), "Deslocamento", bacteria_atual))

            elif evento.tipo_evento(evento_atual) == "Alimentacao":
                if bct.especie_bacteria(bacteria_atual) == A:
                    especie_morta = gr.alimenta_a(grelha, bacteria_atual)
                    if especie_morta == A:
                        num_A -= 1
                    elif especie_morta == B:
                        num_B -= 1
                    elif especie_morta == C:
                        num_C -= 1
                else:
                    if gr.alimenta_b_c(grelha, bacteria_atual):
                        # Morreu
                        if bct.especie_bacteria(bacteria_atual) == B:
                            num_B -= 1
                        elif bct.especie_bacteria(bacteria_atual) == C:
                            num_C -= 1

                cap = cp.adicionar_evento(cap, evento.cria_evento(tempo_atual+obsrandom.exp_random(TA), "Alimentacao", bacteria_atual))
            
            elif evento.tipo_evento(evento_atual) == "Reproducao":
                cap, conseguiu_reproduzir = cel.reproduz(bacteria_atual, celula_bacteria, Q, F, cap, tempo_atual, TD, TR, TA, TM, id_atual)
                if conseguiu_reproduzir:
                    id_atual += 1
                    if bct.especie_bacteria(bacteria_atual) == A:
                        num_A += 1
                    elif bct.especie_bacteria(bacteria_atual) == B:
                        num_B += 1
                    elif bct.especie_bacteria(bacteria_atual) == C:
                        num_C += 1

                cap = cp.adicionar_evento(cap, evento.cria_evento(tempo_atual+obsrandom.exp_random(TR), "Reproducao", bacteria_atual))

        # Evento geral
        if bacteria_atual == 0 and evento.tipo_evento(evento_atual) == "Reposicao":
            gr.repoe_alimento(grelha)
            cap = cp.adicionar_evento(cap, evento.cria_evento(tempo_atual+obsrandom.exp_random(TRP), "Reposicao", 0))

        tempos_A.append(tempo_atual)
        tempos_B.append(tempo_atual)
        tempos_C.append(tempo_atual)

        bacterias_A.append(num_A)
        bacterias_B.append(num_B)
        bacterias_C.append(num_C)

        evento_atual = cp.proximo_evento(cap)
        bacteria_atual = evento.bacteria_evento(evento_atual)
        tempo_atual = evento.tempo_evento(evento_atual)
        cap = cp.elimina_evento(cap)
    
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