import functions
from graphviz import Digraph

def minizacaoAFD():

    folAFD = "static/AFD/"

    alfabeto = []
    estado_inicial = ''
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

                for simbolo in {simbolo for (estado, simbolo) in func_transicaoAFD.keys()}:

                    chegada1 = func_transicaoAFD.get((e1, simbolo), [None])
                    chegada2 = func_transicaoAFD.get((e2, simbolo), [None])

                    if chegada1 and chegada2 and chegada1[0] and chegada2[0]:

                        

                            n_chegada1 = combEstados.get(chegada1[0], chegada1[0])
                            n_chegada2 = combEstados.get(chegada2[0], chegada2[0])

                            if (n_chegada1 != n_chegada2):

                                if tabMinimiza.get((n_chegada1, n_chegada2), False) or tabMinimiza.get((n_chegada2, n_chegada1), False):

                                    tabMinimiza[(e1, e2)] = True
                                    valor = True
                                    break
 

    for (e1, e2), diferente in tabMinimiza.items():
        if not diferente:
            combEstados[e1] = combEstados.get(e1, e1)
            combEstados[e2] = combEstados.get(e1, e1)


    for estado in estados: #atualiza a lista de estados do AFD

        novo_estado = combEstados.get(estado, estado)

        if novo_estado not in n_estados:
            n_estados.append(novo_estado)


    n_finais = []
    novos_estados_finais = []
    for s1 in estados:
        for s2 in estados:
            if tabMinimiza[(s1,s2)] == True:
                print(f"S1: {s1}")
                print(f"S2: {s2}")
                if s1 in estados_finais and s2 in estados_finais and (s1 not in n_finais and s2 not in n_finais): #verifica onde ta vazio  e se é final e dps junta
                    n_finais.extend([s1,s2])
                    n_finais = list(set(n_finais)) #se tiver repetido tira.
                    if (n_finais == s1 and n_finais == s2):
                        novos_estados_finais  = estados_finais
                    else:
                        novos_estados_finais  = [''.join(n_finais)]



    for (estado, simbolo), chegada in func_transicaoAFD.items():
        if chegada:
            novo_estado = combEstados.get(estado, estado)
            nova_chegada = combEstados.get(chegada[0], chegada[0])
            n_func_transicaoAFD[(novo_estado, simbolo)] = nova_chegada


    print(f"Novos estados: {n_estados}")

    print(f"Novos estados finais: {n_finais} e {novos_estados_finais}")

    n_estado_inicial = combEstados.get(estado_inicial, estado_inicial)


    # Criar o gráfico do autômato minimizado
    automato = Digraph()
    automato.attr(rankdir='LR')
    automato.attr('node', shape='circle')
    
    automato.node('', shape='none')
    automato.edge('', n_estado_inicial)
    
    for estado in n_finais:
        """
        if estado in n_finais:
            estado = novos_estados_finais
        """
        automato.node((estado), shape='doublecircle', fontsize='19', fontcolor='green')
    
    for (estado, simbolo), destino in n_func_transicaoAFD.items():
        """
        if destino in n_finais:
            destino = novos_estados_finais
        """
        automato.edge(estado, (destino), label=simbolo)

    automato.render(folAFD + 'AutomatoMinimizado', format='png', cleanup=True)




