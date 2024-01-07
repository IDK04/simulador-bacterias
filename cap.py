from evento import *

# A cap corresponde a uma lista de eventos
def criar_cap():
    return []

# Adicionar um evento dependendo dos tempos
def adicionar_evento(cap, evento):
    return [e for e in cap if tempo_evento(e)<tempo_evento(evento)]+[evento]+\
            [e for e in cap if tempo_evento(e)>tempo_evento(evento)]

# Retorna o proximo evento e remove-o da cap
# retorno: False se não houver eventos, evento caso contrário
def pop_evento(cap):
    if len(cap) == 0:
        return False
    
    evento = cap[0]
    cap = cap[1:]
    return evento

def mostra_eventos(cap):
    for evento in cap:
        print(tempo_evento(evento), tipo_evento(evento))
