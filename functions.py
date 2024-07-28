import os
import time


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


def extrairInfAF(folder, estado_inicial, estados_finais, alfabeto):
    filepath = os.path.join(folder, 'informacaoAF')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    
    with open(filepath, 'r') as file:
        linhas = file.readlines()
    
    estado_inicial = linhas[0].strip()
    estados_finais = linhas[1].strip().split()
    alfabeto = linhas[2].strip().split()
    
    return estado_inicial, estados_finais, alfabeto

def extrairDict(folder):
    filepath = os.path.join(folder, 'AFCriado.txt')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    
    with open(filepath, 'r') as file:
        conteudo = file.read()
    
    func_transicao = eval(conteudo)
    return func_transicao


def pastasCriadas():
    time.sleep(1)
    if os.path.exists('AFD'):
        print("\n Há um AFD já criado\n")

    if os.path.exists('AFN'):
        print("\n Há um AFN já criado\n")

    else:
        print("\nCrie um AFD ou AFN\n")



def dicionario(dict):
    lista = [(estado_atual, valor, estado_seguinte) for (estado_atual, valor), estados_seguintes in dict.items() for estado_seguinte in estados_seguintes]
    return lista