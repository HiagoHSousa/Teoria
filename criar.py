import os
import functions


def criarAF():
    #estruturas do automato
    estados = []
    alfabeto = []
    func_transicao = {}
    estado_inicial = ""
    estados_finais = []

    folAFD = "AFD/"
    folAFN = "AFN/"


    while True:

        print("\nMenu")
        print("1. Criar um AFD")
        print("2. Criar um AFN")
        print("3. Voltar para o inicio")
        try:

            opcao = int(input("Escolha o que quer fazer: "))
            if opcao == 1:
                # recebendos os dados do automato
                print("Digite o conjunto dos estados: ", end="")
                estados = input().split()


                print("Digite o alfabeto do automato: ", end="")
                alfabeto = input().split()


                print("Digite o estado inicial: ", end="")
                estado_inicial = input()

                print("Digite os estados finais: ", end="")
                estados_finais = input().split()


                print("Digite as funçôes de transiçâo: ")
                for estado in estados:
                    for simbolo in alfabeto:
                        print(f"\t {simbolo}")
                        print(f"{estado}\t--->\t", end="")
                        proximo_estado = input()

                        if proximo_estado == "*":
                            func_transicao[(estado, simbolo)] = None #simbolo que nao leva para nenhum estado
                        else:
                            func_transicao[(estado, simbolo)] = proximo_estado

                #salvar informaçoes para ler

                arquivoAFD = functions.arquivoAutomato(folAFD, func_transicao) #salva as funçoes de transicao
                arquivoAFD.close()
            
                estadosAFD = functions.crEstados(folAFD, estados) #salva os estados
                estadosAFD.close()

                informacoesAFD = functions.informacaoAutomato(folAFD, estado_inicial, estados_finais, alfabeto) # salva o inicio, fins e alfabeto
                informacoesAFD.close()

                #delta_lista = functions.dict_lista(func_transicao)

            elif opcao == 2:
                print("AFN")
                # recebendos os dados do automato
                print("Digite o conjunto dos estados: ", end="")
                estados = input().split()


                print("Digite o alfabeto do automato: ", end="")
                alfabeto = input().split()


                print("Digite o estado inicial: ", end="")
                estado_inicial = input()

                print("Digite os estados finais: ", end="")
                estados_finais = input().split()


                print("Digite as funçôes de transiçâo: ")
                for estado in estados:
                    for simbolo in alfabeto:
                        print(f"\t {simbolo}")
                        print(f"{estado}\t--->\t", end="")
                        proximo_estado = [prox for prox in input().split()]

                        if proximo_estado == "*":
                            func_transicao[(estado, simbolo)] = None #simbolo que nao leva para nenhum estado
                        else:
                            func_transicao[(estado, simbolo)] = proximo_estado

                #salvar informaçoes para ler

                arquivoAFN = functions.arquivoAutomato(folAFN, func_transicao) #salva as funçoes de transicao
                arquivoAFN.close()
            
                estadosAFN = functions.crEstados(folAFN, estados) #salva os estados
                estadosAFN.close()

                informacoesAFN = functions.informacaoAutomato(folAFN, estado_inicial, estados_finais, alfabeto) # salva o inicio, fins e alfabeto
                informacoesAFN.close()



            elif opcao == 3:
                break    

        except ValueError:
            print('Erro: Você deve entrar com um número inteiro.')

    