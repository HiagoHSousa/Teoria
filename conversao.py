import functions
import os
from graphviz import Digraph

def conversaoAFNAFN():

    folAFN = "AFN/"
    folAFD = "AFD/"


    #informaçoes AFN
    func_transicaoAFN = functions.extrairDict(folAFN)
    estado_inicial, estados_finais, alfabeto = functions.extrairInfAF(folAFN, "", set(), set())



    estadoIniLista = [estado_inicial] #deixa como lista o estado inicial para fazer as transiçoes posteriormente

    #informaçoes AFD
    estadosAFD = []
    tabTranAFD = {}
    estados_finaisAFD = []


    fila = [estadoIniLista] #vai armazenar os estados


    while fila:

        estado_atual = fila.pop(0)
        estadoAtualStr = "".join(estado_atual)
        
        # Adiciona o estado atual à lista de estados do AFD
        if estadoAtualStr not in ["" .join(e) for e in estadosAFD]:
            estadosAFD.append(estado_atual)


        for simbolo in alfabeto:

            estado_seguinte = [] #armazena os estados que virao a partir do atual

            for estado in estado_atual:

                if (estado, simbolo) in func_transicaoAFN:

                    for novoEstado in func_transicaoAFN[(estado, simbolo)]:

                        if novoEstado not in estado_seguinte:

                            estado_seguinte.append(novoEstado)  #adiciona um estado na lista de seguinte caso ele nao exista

        
            if estado_seguinte:
                estadoSegStr = "".join(estado_seguinte)
                tabTranAFD[(estadoAtualStr, simbolo)] = estadoSegStr
                    
                if estado_seguinte not in estadosAFD:
                        fila.append(estado_seguinte)

        if any(estado in estados_finais for estado in estado_atual):
            estados_finaisAFD.append(estadoAtualStr)

    # Salva o AFD em um arquivo
    functions.arquivoAutomato(folAFD, tabTranAFD).close()
    functions.informacaoAutomato(folAFD, estado_inicial, estados_finaisAFD, alfabeto).close()
    functions.crEstados(folAFD, ["".join(e) for e in estadosAFD]).close()


    #desenhar o AFD convertido INIC
    automato = Digraph()
    automato.attr(rankdir='LR')
    automato.attr('node', shape='circle')    
        
    automato.node('->', shape='none', width='0', heigth='0',label='')
    automato.edge('->', estado_inicial)
        
    for estado_final in estados_finaisAFD: 

        automato.node(estado_final, shape='doublecircle', fontsize='17')

    for (estado, simbolo) in tabTranAFD:

        destino = tabTranAFD[(estado, simbolo)]
        automato.edge(estado,destino,label=simbolo) 

    automato.render(folAFD + ('AFDConvertido'), format='png', cleanup=True)
    #desenhar o AFD convertido FIM



    #teste de equivalencia
    print("Para testar a equivalencia do AFN e do AFD, digite uma palavra: ", end="")

    palavra = input().strip()

    testar_equivalencia(folAFN, folAFD, palavra)



def testar_afn(func_transicaoAFN , estado_inicial, estados_finais, palavra):
    
    estados_atuais = [estado_inicial]

    for simbolo in palavra:
        novos_estados = []
        for estado_atual in estados_atuais:
            prox_estados = func_transicaoAFN .get((estado_atual, simbolo), [])
            novos_estados.extend(prox_estados)
        estados_atuais = novos_estados
    return any(estado in estados_finais for estado in estados_atuais)


def testar_afd(func_transicaoAFD , estado_inicial, estados_finais, palavra):

    estado_atual = estado_inicial

    for simbolo in palavra:
        estado_atual = func_transicaoAFD.get((estado_atual, simbolo))
        if estado_atual is None:
            return False
    return estado_atual in estados_finais


def testar_equivalencia(folAFN, folAFD, palavra):

    func_transicaoAFN = functions.extrairDict(folAFN)
    estado_inicial_afn, estados_finais_afn, alfabeto_afn = functions.extrairInfAF(folAFN, None, set(), set())
    
    func_transicaoAFD = functions.extrairDict(folAFD)
    estado_inicial_afd, estados_finais_afd, alfabeto_afd = functions.extrairInfAF(folAFD, None, set(), set())

    resultado_afn = testar_afn(func_transicaoAFN, estado_inicial_afn, estados_finais_afn, palavra)
    resultado_afd = testar_afd(func_transicaoAFD, estado_inicial_afd, estados_finais_afd, palavra)

    if resultado_afn == resultado_afd:
        print(f"A palavra '{palavra}' é {'aceita' if resultado_afn else 'rejeitada'} tanto pelo AFN quanto pelo AFD.")
    else:
        print(f"A palavra '{palavra}' não é pelo AFN e pelo AFD.")