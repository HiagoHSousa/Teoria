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





def minimizacaoAFD():
    folAFD = "AFD/"
    
    # Extrair informações do AFD
    estado_inicial, estados_finais, alfabeto = functions.extrairInfAF(folAFD, "", set(), set())
    transicoes = functions.extrairDict(folAFD)
    
    # 1. Inicializar as partições
    P = [set(estados_finais), {estado for estado in transicoes if estado not in estados_finais}]
    
    while True:
        nova_P = []
        for grupo in P:
            particoes = {}
            for estado in grupo:
                chave = tuple(transicoes.get((estado, simbolo), None) for simbolo in alfabeto)
                if chave not in particoes:
                    particoes[chave] = set()
                particoes[chave].add(estado)
            nova_P.extend(particoes.values())
        
        if nova_P == P:
            break
        P = nova_P
    
    # 2. Construir o novo AFD
    novo_transicoes = {}
    novo_estados_finais = []
    novo_estados = []
    novo_estado_inicial = None

    mapa_estados = {}

    for grupo in P:
        # Verificar o conteúdo de grupo
        print(f"Grupo original: {grupo}")

        # Garantindo que `grupo` contém apenas strings
        grupo_str = list(grupo)  # Converter o grupo em uma lista de strings, se necessário

        # Verificar o conteúdo de grupo_str
        print(f"Grupo como strings: {grupo_str}")

        try:
            novo_estado = "".join(sorted(grupo_str))
        except TypeError as e:
            print(f"Erro ao criar novo estado: {e}")
            print(f"Tipo de grupo_str: {[type(item) for item in grupo_str]}")
            raise

        novo_estados.append(novo_estado)
        for estado in grupo:
            mapa_estados[estado] = novo_estado
        
        if estado_inicial in grupo:
            novo_estado_inicial = novo_estado
        if any(estado in estados_finais for estado in grupo):
            novo_estados_finais.append(novo_estado)
    
    # Verificar se todos os estados de destino estão mapeados
    for (estado, simbolo), destino in transicoes.items():
        if estado in mapa_estados:
            if destino in mapa_estados:
                novo_transicoes[(mapa_estados[estado], simbolo)] = mapa_estados[destino]
            else:
                # Adiciona o estado de destino ao mapa se ele não estiver presente
                novo_estado_destino = "".join(sorted([destino]))  # Garantindo que destino é uma string
                mapa_estados[destino] = novo_estado_destino
                novo_transicoes[(mapa_estados[estado], simbolo)] = novo_estado_destino
        else:
            # Adiciona o estado de origem ao mapa se ele não estiver presente
            novo_estado_origem = "".join(sorted([estado]))  # Garantindo que origem é uma string
            mapa_estados[estado] = novo_estado_origem
            if destino in mapa_estados:
                novo_transicoes[(novo_estado_origem, simbolo)] = mapa_estados[destino]
            else:
                novo_estado_destino = "".join(sorted([destino]))  # Garantindo que destino é uma string
                mapa_estados[destino] = novo_estado_destino
                novo_transicoes[(novo_estado_origem, simbolo)] = novo_estado_destino

    # Salva o AFD minimizado em um arquivo
    functions.arquivoAutomato(folAFD + "Minimizado", novo_transicoes).close()
    functions.informacaoAutomato(folAFD + "Minimizado", novo_estado_inicial, novo_estados_finais, alfabeto).close()
    functions.crEstados(folAFD + "Minimizado", novo_estados).close()

    # Desenhar o AFD minimizado
    automato = Digraph()
    automato.attr(rankdir='LR')
    automato.attr('node', shape='circle')    
        
    automato.node('->', shape='none', width='0', height='0', label='')
    automato.edge('->', novo_estado_inicial)
        
    for estado_final in novo_estados_finais: 
        automato.node(estado_final, shape='doublecircle', fontsize='17')

    for (estado, simbolo) in novo_transicoes:
        destino = novo_transicoes[(estado, simbolo)]
        automato.edge(estado, destino, label=simbolo) 

    automato.render(folAFD + ('AFDMinimizado'), format='png', cleanup=True)