import functions
from graphviz import Digraph

def minizacaoAFD():

    folAFD = "AFD/"

    alfabeto = []
    estado_inicial = ""
    estados_finais = []


    verifica = functions.verificaAFcriado(folAFD)

    if not verifica:

        return
    else:

        func_transicaoAFD = functions.extrairDict(folAFD)
        estados = functions.readEstados(folAFD)
        estado_inicial, estados_finais, alfabeto = functions.extrairInfAF(folAFD, estado_inicial, estados_finais, alfabeto)


    #informaçoes automato minimizado
    tabMinimiza = {}
    valor = True
    combEstados = {}
    n_estados_finais = []
    n_func_transicaoAFD = {}
    n_estados = []

    for e1 in estados:

        for e2 in estados:
            
            if e1 != e2:

                tabMinimiza[(e1, e2)] = (e1 in estados_finais) ^ (e2 in estados_finais) #tabela minimizaçao

    
    while valor:

        valor = False
        for (e1, e2), diferente in tabMinimiza.items():

            if not diferente:

                for simbolo in {simbolo for (estado, simbolo) in n_func_transicaoAFD.keys()}:

                    chegada1 = n_func_transicaoAFD.get((e1, simbolo), [None])[0]
                    chegada2 = n_func_transicaoAFD.get((e2, simbolo), [None])[0]

                    if chegada1 and chegada2 and (chegada1 != chegada2):

                        if tabMinimiza.get((chegada1, chegada2), False) or tabMinimiza.get((chegada2, chegada1), False): #verifica se são estados diferentes e marcam eles 

                            tabMinimiza[(e1, e2)] = True
                            valor = True
                            break

    
    for (s1, s2), diferente in tabMinimiza.items(): # estados iguais sao marcados

        if not diferente:

            combEstados[s1] = combEstados.get(s1, s1)
            combEstados[s2] = combEstados.get(s1, s1)

    
   
    for estado in estados_finais: #atualiza a lista de estados finais do AFD

        novo_estado = combEstados.get(estado, estado)
        n_estados_finais.append(novo_estado)


    
    for (estado, simbolo), destinos in func_transicaoAFD.items(): #atualiza a lista de funçoes de transiçao do AFD

        novo_estado = combEstados.get(estado, estado)
        n_chegada = combEstados.get(destinos[0], destinos[0])

        n_chegada_a = "".join(n_chegada)
        n_func_transicaoAFD[(novo_estado, simbolo)] = n_chegada_a


    for estado in estados: #atualiza a lista de estados do AFD

        novo_estado = functions.estadoEquivalente(estado, combEstados)
        n_estados.append(novo_estado)


    n_estado_inicial = functions.estadoEquivalente(estado_inicial, combEstados)


    #desenho do automato minimizado

    automato = Digraph()  
    automato.attr(rankdir='LR') 
    automato.attr('node', shape='circle')

    automato.node('', shape='none')
    automato.edge('', n_estado_inicial)

    for estado in n_estados:

        if estado in estados_finais:

            automato.node((estado), shape='doublecircle', fontsize='17')

    for (estado, simbolo) in n_func_transicaoAFD:

        destino = n_func_transicaoAFD[(estado, simbolo)]
        automato.edge(estado, destino, label=simbolo)  # Adiciona as transições

    automato.render(folAFD + ('AFMinimizado'), format='png', cleanup=True)

