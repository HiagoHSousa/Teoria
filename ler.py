import os
import functions

folAFD = "static/AFD/"
folAFN = "static/AFN/"


 
def lerAF():
    
    while True:

        print("\nMenu")
        print("1. Ler um AFD")
        print("2. Ler um AFN")
        print("3. Voltar para o inicio")
        try:

            opcao = int(input("Escolha o que quer fazer: "))
            if opcao == 1:
                #reconhecendo a linguagem
                print("Digite a linguagem que você quer que seja reconhecida: ", end="")
                entrada= input()

                alfabeto = []
                func_transicao = {}
                estado_inicial = ""
                estados_finais = []

                estado_inicial, estados_finais, alfabeto = functions.extrairInfAF(folAFD, estado_inicial, estados_finais, alfabeto) 

                func_transicao = functions.extrairDict(folAFD)

                estado_atual = estado_inicial

                for simbolo in entrada:
                    print(f"Estado atual: {estado_atual}")
                    print(f"Entrada atual: {simbolo}")

                    print(f"Próximo estado: {func_transicao[(estado_atual, simbolo)]}\n")

                    estado_atual = func_transicao.get((estado_atual, simbolo))

                    if estado_atual == None:
                        print("O automato nao reconheceu a linguagem")
                        break


                if estado_atual in estados_finais:
                    print("O automato reconheceu a linguagem")
                else:
                    print("O automato nao reconheceu a linguagem")
    
            elif opcao == 2:
                print("AFN")
                #reconhecendo a linguagem
                print("Digite a linguagem que você quer que seja reconhecida: ", end="")
                entrada= input()


                alfabeto = []
                func_transicao = {}
                estado_inicial = ""
                estados_finais = []

                estado_inicial, estados_finais, alfabeto = functions.extrairInfAF(folAFN, estado_inicial, estados_finais, alfabeto) 

                func_transicao = functions.extrairDict(folAFN)


                estados_atuais = [estado_inicial]
                for simbolo in entrada:
                    print(f"Estados atuais: {estados_atuais}")
                    novos_estados = []
                    
                    for estado_atual in estados_atuais:
                        prox_estados = func_transicao.get((estado_atual, simbolo), [])
                        novos_estados.extend(prox_estados)
                    
                    estados_atuais = novos_estados

                    print(f"Entrada atual: {simbolo}")
                    print(f"Próximos estados: {estados_atuais}")

                if any(estado in estados_finais for estado in estados_atuais):
                    print("O automato reconheceu a linguagem")
                else:
                    print("O automato não reconheceu a linguagem")


            elif opcao == 3:
                break    

        except ValueError:
            print('Erro: Você deve entrar com um número inteiro.')
     