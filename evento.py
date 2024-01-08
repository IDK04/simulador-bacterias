# Tipos de evento:
# - Deslocamento
# - Alimentacao
# - Reproducao
# - Reposicao
# - Morte

def cria_evento(tempo, tipo, bacteria):
    return [tempo, tipo, bacteria]

def tempo_evento(evento):
    return evento[0]

def tipo_evento(evento):
    return evento[1]

def bacteria_evento(evento):
    return evento[2]