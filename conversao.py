import functions
import os
from graphviz import Digraph


def conversaoAFNAFN():

    folAFN = "static/AFN/"
    folAFD = "static/AFD/"
    tamPalavra = 5

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
    functions.testar_multiplas_linguagens_geradas(folAFN, folAFD, tamPalavra)