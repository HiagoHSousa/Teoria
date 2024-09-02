import os
import functions

def criarAF():
    # Estruturas do autômato
    estados = []
    alfabeto = []
    func_transicao = {}
    estado_inicial = ""
    estados_finais = []

    base_folder = 'static/'
    folAFD = os.path.join(base_folder, 'AFD/')
    folAFN = os.path.join(base_folder, 'AFN/')

    while True:
        print("\nMenu")
        print("1. Criar um AFD")
        print("2. Criar um AFN")
        print("3. Voltar para o início")
        try:
            opcao = int(input("Escolha o que quer fazer: "))
            if opcao == 1:
                # Recebendo os dados do autômato
                print("Digite o conjunto dos estados: ", end="")
                estados = input().split()

                print("Digite o alfabeto do autômato: ", end="")
                alfabeto = input().split()

                print("Digite o estado inicial: ", end="")
                estado_inicial = input()

                print("Digite os estados finais: ", end="")
                estados_finais = input().split()

                print("Digite as funções de transição: ")
                for estado in estados:
                    for simbolo in alfabeto:
                        print(f"\t {simbolo}")
                        print(f"{estado}\t--->\t", end="")
                        proximo_estado = input()

                        if proximo_estado == "*":
                            func_transicao[(estado, simbolo)] = None  # símbolo que não leva para nenhum estado
                        else:
                            func_transicao[(estado, simbolo)] = proximo_estado

                # Criar pasta se não existir
                if not os.path.exists(folAFD):
                    os.makedirs(folAFD)

                # Salvar informações
                arquivoAFD = functions.arquivoAutomato(folAFD, func_transicao)  # Salva as funções de transição
                arquivoAFD.close()

                estadosAFD = functions.crEstados(folAFD, estados)  # Salva os estados
                estadosAFD.close()

                informacoesAFD = functions.informacaoAutomato(folAFD, estado_inicial, estados_finais, alfabeto)  # Salva o início, fins e alfabeto
                informacoesAFD.close()

                delta_lista = functions.converter_para_lista_transicoes(func_transicao)
                print(delta_lista)

                # Plotando
                AutomatoAFD = functions.desenhar_automato(estado_inicial, estados_finais, delta_lista)
                AutomatoAFD.render(folAFD + 'desenhoAFD', format='png', cleanup=True)

            elif opcao == 2:
                print("AFN")
                # Recebendo os dados do autômato
                print("Digite o conjunto dos estados: ", end="")
                estados = input().split()

                print("Digite o alfabeto do autômato: ", end="")
                alfabeto = input().split()

                print("Digite o estado inicial: ", end="")
                estado_inicial = input()

                print("Digite os estados finais: ", end="")
                estados_finais = input().split()

                print("Digite as funções de transição: ")
                for estado in estados:
                    for simbolo in alfabeto:
                        print(f"\t {simbolo}")
                        print(f"{estado}\t--->\t", end="")
                        proximo_estado = [prox for prox in input().split()]

                        if proximo_estado == "*":
                            func_transicao[(estado, simbolo)] = None  # símbolo que não leva para nenhum estado
                        else:
                            func_transicao[(estado, simbolo)] = proximo_estado

                # Criar pasta se não existir
                if not os.path.exists(folAFN):
                    os.makedirs(folAFN)

                # Salvar informações
                arquivoAFN = functions.arquivoAutomato(folAFN, func_transicao)  # Salva as funções de transição
                arquivoAFN.close()

                estadosAFN = functions.crEstados(folAFN, estados)  # Salva os estados
                estadosAFN.close()

                informacoesAFN = functions.informacaoAutomato(folAFN, estado_inicial, estados_finais, alfabeto)  # Salva o início, fins e alfabeto
                informacoesAFN.close()

                delta_lista = functions.converter_para_lista_transicoes(func_transicao)
                print(delta_lista)

                # Plotando
                AutomatoAFN = functions.desenhar_automato(estado_inicial, estados_finais, delta_lista)
                AutomatoAFN.render(folAFN + 'desenhoAFN', format='png', cleanup=True)

            elif opcao == 3:
                break

        except ValueError:
            print('Erro: Você deve entrar com um número inteiro.')
