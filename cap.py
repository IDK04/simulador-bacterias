from evento import *

# A cap corresponde a uma lista de eventos
def criar_cap():
    return []

# Adicionar um evento dependendo dos tempos
def adicionar_evento(cap, evento):
    return [e for e in cap if tempo_evento(e)<tempo_evento(evento)]+[evento]+\
            [e for e in cap if tempo_evento(e)>tempo_evento(evento)]

def proximo_evento(cap):
    if len(cap) == 0:
        return False
    return cap[0]

def elimina_evento(cap):
    if len(cap) == 0:
        return False
    return cap[1:]

def mostra_eventos(cap):
    for evento in cap:
        print(tempo_evento(evento), tipo_evento(evento), bacteria_evento(evento))
