import functions
from graphviz import Digraph

diretorioAFD = "static/AFD/"

def minimizacaoAFD():

    # Extraindo informações e transições do AFD
    estado_inicial, estados_finais, alfabeto = functions.extrairInfAF(diretorioAFD, "", [], [])
    transicoes = functions.extrairDict(diretorioAFD)
    estados = functions.readEstados(diretorioAFD)


    tabela_transicao = {}
    mudou = True
    estados_equivalentes = {}
    nova_func_transicao = {}
    estados_resultantes = []


    # Configuração inicial da tabela de distinção
    for estado1 in estados:
        for estado2 in estados:
            if estado1 != estado2:

                tabela_transicao[(estado1, estado2)] = (estado1 in estados_finais) != (estado2 in estados_finais)
            else:

                tabela_transicao[(estado1, estado2)] = True


    # Atualização da tabela de distinção
    while mudou:
        mudou = False
        for (estado1, estado2), distintos in tabela_transicao.items():

            if not distintos:

                for simbolo in alfabeto:

                    chegada1 = functions.estadoEquivalente(transicoes.get((estado1, simbolo)), estados_equivalentes)
                    chegada2 = functions.estadoEquivalente(transicoes.get((estado2, simbolo)), estados_equivalentes)
                    if chegada1 and chegada2 and chegada1 != chegada2:

                        if tabela_transicao.get((chegada1, chegada2), False) or tabela_transicao.get((chegada2, chegada1), False):

                            tabela_transicao[(estado1, estado2)] = True
                            mudou = True
                            break

    # Combinação de estados equivalentes
    for (estado1, estado2), distintos in tabela_transicao.items():

        if not distintos:

            estados_equivalentes[estado1] = estados_equivalentes.get(estado1, estado1)
            estados_equivalentes[estado2] = estados_equivalentes.get(estado1, estado1)

    # Criação dos novos estados para o AFD minimizado
    for estado in estados:

        novo_estado = functions.estadoEquivalente(estado, estados_equivalentes)
        if novo_estado not in estados_resultantes:

            estados_resultantes.append(novo_estado)

    # Construção da nova função de transição para o AFD minimizado
    for (estado, simbolo), chegada in transicoes.items():

        novo_estado = functions.estadoEquivalente(estado, estados_equivalentes)
        novo_chegada = functions.estadoEquivalente(chegada, estados_equivalentes)
        nova_func_transicao[(novo_estado, simbolo)] = novo_chegada

    # Definição dos novos estados finais
    novos_estados_finais = []
    for estado in estados_finais:

        novo_estado = functions.estadoEquivalente(estado, estados_equivalentes)
        if novo_estado not in novos_estados_finais:

            novos_estados_finais.append(novo_estado)


    # Ajuste do novo estado inicial
    novo_estado_inicial = functions.estadoEquivalente(estado_inicial, estados_equivalentes)


    # Salvando o AFD minimizado
    functions.arquivoAutomato(diretorioAFD, nova_func_transicao)
    functions.informacaoAutomato(diretorioAFD, novo_estado_inicial, novos_estados_finais, alfabeto).close()
    functions.crEstados(diretorioAFD, estados_resultantes).close()


    # Gerando a imagem do autômato minimizado
    transicoes_lista = functions.converter_para_lista_transicoes(nova_func_transicao)
    automato = functions.desenhar_automato(novo_estado_inicial, novos_estados_finais, transicoes_lista)
    automato.render(diretorioAFD + 'AutomatoMinimizado', format='png', cleanup=True)

    print("Processo de minimização concluído e arquivos gerados com sucesso.")