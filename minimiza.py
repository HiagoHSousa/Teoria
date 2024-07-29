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

                tabMinimiza[(e1, e2)] = (e1 in estados_finais) != (e2 in estados_finais) #tabela minimizaçao

            else:

                tabMinimiza[(e1, e2)] = True

    while valor:

        valor = False
        for (e1, e2), diferente in tabMinimiza.items():

            if not diferente:

                for simbolo in alfabeto:

                    chegada1 = func_transicaoAFD.get((e1, simbolo))
                    chegada2 = func_transicaoAFD.get((e2, simbolo))

                    if chegada1 and chegada2 and (chegada1[0] != chegada2[0]):

                        if chegada1 and chegada2:

                            n_chegada1 = combEstados.get(chegada1[0], chegada1[0])
                            n_chegada2 = combEstados.get(chegada2[0], chegada2[0])

                            if (n_chegada1 != n_chegada2):

                                if tabMinimiza.get((n_chegada1, n_chegada2), False) or tabMinimiza.get((n_chegada2, n_chegada1), False):

                                    tabMinimiza[(e1, e2)] = True
                                    valor = True
                                    break
 

    for (s1, s2), diferente in tabMinimiza.items():
        if not diferente:
            combEstados[s1] = combEstados.get(s1, s1)
            combEstados[s2] = combEstados.get(s1, s1)

   
    for estado in estados_finais: #atualiza a lista de estados finais do AFD

        novo_estado = combEstados.get(estado, estado)

        if novo_estado not in n_estados_finais:
            n_estados_finais.append(novo_estado)


    
    n_func_transicaoAFD = functions.atualiza_delta_AFD(func_transicaoAFD, combEstados, alfabeto)


    for estado in estados:
        novo_estado = combEstados.get(estado, estado)
        if novo_estado not in n_estados:
            n_estados.append(novo_estado)

    n_estado_inicial = combEstados.get(estado_inicial, estado_inicial)




    #desenho do automato minimizado
    func_transicao_lista = functions.converter_para_lista_transicoes(n_func_transicaoAFD)
    automato = functions.desenhar_automato(n_estado_inicial, n_estados_finais, func_transicao_lista)
    automato.render(folAFD + ('AFMinimizado'), format='png', cleanup=True)



