import os
import time
from graphviz import Digraph
import itertools


def arquivoAutomato(folder, func_transicao): #passa as funcoes de transicao para um arquivo

    arquivoAF = open(folder + ('AFCriado.txt'), 'w') 
    arquivoAF.writelines(str(func_transicao))
    return arquivoAF


def informacaoAutomato(folder, estado_inicial, estados_finais, alfabeto): #passa as informacoes para um arquivo

    informacaoAF = open(folder + ('informacaoAF'), 'w')
    informacaoAF.write(estado_inicial + '\n')
    informacaoAF.writelines(' '.join(estados_finais))
    informacaoAF.write('\n')
    informacaoAF.writelines(' '.join(alfabeto))
    return informacaoAF


def crEstados(folder, estados): #passa os estados para um arquivo
    
    arqui = open(folder + ('estados.txt'), 'w+')
    arqui.writelines('\n'.join(estados))
    return arqui


def readEstados(folder): #le o arquivo de estados

    with open(os.path.join(folder, 'estados.txt'), 'r') as arq:
        estados = arq.readlines()
    estados = [item.strip() for item in estados]
    return estados


def estadoEquivalente(estado, combEstados):#econtra os estados equivalentes
        
        while estado in combEstados and combEstados[estado] != estado:
            estado = combEstados[estado]

        return estado


def extrairInfAF(folder, estado_inicial, estados_finais, alfabeto): #le o arquivo de informaçoes do AF

    filepath = os.path.join(folder, 'informacaoAF')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    
    with open(filepath, 'r') as file:
        linhas = file.readlines()
    
    estado_inicial = linhas[0].strip()
    estados_finais = linhas[1].strip().split()
    alfabeto = linhas[2].strip().split()
    
    return estado_inicial, estados_finais, alfabeto



def extrairDict(folder): #le o arquivo das transiçoes do AF

    filepath = os.path.join(folder, 'AFCriado.txt')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    
    with open(filepath, 'r') as file:
        conteudo = file.read()
    
    func_transicao = eval(conteudo)
    return func_transicao


def verificaAFcriado(pasta):

    time.sleep(1)
    path = os.path.join(pasta, 'AFCriado.txt')

    if not os.path.isfile(path):

        print('Arquivo AFCriado.txt não encontrado. Crie um AFD ou AFN.')
        return False
    
    return True


def pastasCriadas():

    time.sleep(1)
    if os.path.exists('AFD'):
        print("\n Há um AFD já criado\n")

    if os.path.exists('AFN'):
        print("\n Há um AFN já criado\n")

    else:
        print("\nCrie um AFD ou AFN\n")


def converter_para_lista_transicoes(transicoes_dict): #converte o AF para poder desenhar na outra funçao

    lista = []

    for (estado_origem, simbolo), estados_destinos in transicoes_dict.items():

        if estados_destinos is not None:  # Verifica se há transições válidas

            if isinstance(estados_destinos, list):

                for estado_destino in estados_destinos:
                    lista.append((estado_origem, simbolo, estado_destino))

            else:
                lista.append((estado_origem, simbolo, estados_destinos))

    return lista

def desenhar_automato(estado_inicial, estados_finais, func_transicao): #desenha o AF

    automato = Digraph() 
    automato.attr(rankdir='LR') 
    automato.attr('node', shape='circle')
    
    
    automato.node('->', shape='none', width='0', heigth='0',label='')
    automato.edge('->', estado_inicial)
    
    for estado_final in estados_finais: 

        automato.node(estado_final, shape='doublecircle', fontsize='17')

    for estado_origem, simbolo, estado_destino in func_transicao:
        
        automato.edge(estado_origem,estado_destino,label=simbolo) 

    return automato



def gerar_palavras(alfabeto, tamPalavra):
    
    palavras = []

    for length in range(1, tamPalavra + 1):

        for palavra in itertools.product(alfabeto, repeat=length):
            
            palavras.append(''.join(palavra))
    return palavras



def testar_multiplas_linguagens_geradas(folAFN, folAFD, tamPalavra):

    # Extrair informações do AFN
    estado_inicial_AFN, estados_finais_AFN, alfabeto_AFN = extrairInfAF(folAFN, "", set(), set())
    transicoes_AFN = extrairDict(folAFN)

    # Extrair informações do AFD convertido
    estado_inicial_AFD, estados_finais_AFD, alfabeto_AFD = extrairInfAF(folAFD, "", set(), set())
    transicoes_AFD = extrairDict(folAFD)



    def simular_AFN(estado_atual, palavra):
        if not palavra:  # Se a palavra foi completamente consumida
            return estado_atual in estados_finais_AFN
        else:
            simbolo = palavra[0]
            proximo_simbolo = palavra[1:]
            proximos_estados = transicoes_AFN.get((estado_atual, simbolo), [])
            
            return any(simular_AFN(estado, proximo_simbolo) for estado in proximos_estados)



    def simular_AFD(estado_atual, palavra):

        if not palavra:  # Se a palavra foi completamente consumida
            return estado_atual in estados_finais_AFD
        
        else:

            simbolo = palavra[0]
            proximo_simbolo = palavra[1:]
            proximo_estado = transicoes_AFD.get((estado_atual, simbolo))
            
            if proximo_estado is None:
                return False
            
            return simular_AFD(proximo_estado, proximo_simbolo)


    palavras = gerar_palavras(alfabeto_AFN, tamPalavra)
    
    for palavra in palavras:
        # Testar a palavra no AFN
        aceita_AFN = simular_AFN(estado_inicial_AFN, palavra)
        
        # Testar a palavra no AFD convertido
        aceita_AFD = simular_AFD(estado_inicial_AFD, palavra)
        
        
        if aceita_AFN == aceita_AFD:
            resultado = "aceita" if aceita_AFN else "regeitada"
            print(f"A palavra '{palavra}' é {resultado} pelos dois autômatos.")
            print(f"")
        else:
            print(f"A palavra '{palavra}' é reconhecida de forma diferente pelos autômatos.")
            