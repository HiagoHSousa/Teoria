import os
import ler
import criar
import functions
import conversao
import minimiza

folAFD = "AFD/"
folAFN = "AFN/"

if not os.path.exists(folAFD):
    
    os.mkdir(folAFD)


if not os.path.exists(folAFN):
            
    os.mkdir(folAFN)


while True:

        print("Menu")
        print("1. Criar AFD e AFN")
        print("2. Ler AFD e AFN")
        print("3. Converter AFN em AFD")
        print("4. Minimizar AFD")
        print("5. Sair")
        try:

            opcao = int(input("Escolha o que quer fazer: "))

            if opcao == 1:
                criar.criarAF()
                continue

            elif opcao == 2:
                ler.lerAF()
                continue

            elif opcao == 3:
                conversao.conversaoAFNAFN()
                continue

            elif opcao == 4:
                minimiza.minizacaoAFD()
                continue

            elif opcao == 5:
                break

            else:
                print("Opção inválida")

        except ValueError:
            print('Erro: Você deve entrar com um número inteiro.')
