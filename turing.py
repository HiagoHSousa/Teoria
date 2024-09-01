import json

class TuringMachine:
    def __init__(self, specification):
        self.estados = specification['E']
        self.alfabeto = specification['Σ']
        self.alfabeto_fita = specification['Γ']
        self.estado_inicial = specification['x']
        self.estado_rejeicao = specification['y']
        self.estado_final = specification['F']
        self.transicoes = specification['δ']
        self.fita = []
        self.cabeca = 0
        self.estado_atual = self.estado_inicial

    def salvar_especificacao(self, arquivo):
        with open(arquivo, 'w') as f:
            f.write(f"Estados: {','.join(self.estados)}\n")
            f.write(f"Alfabeto: {','.join(self.alfabeto)}\n")
            f.write(f"Alfabeto da Fita: {','.join(self.alfabeto_fita)}\n")
            f.write(f"Estado Inicial: {self.estado_inicial}\n")
            f.write(f"Estado de Rejeição: {self.estado_rejeicao}\n")
            f.write(f"Estados Finais: {','.join(self.estado_final)}\n")
            f.write("Transições:\n")
            for (estado_atual, simbolo_atual), (proximo_estado, simbolo_escrito, movimento) in self.transicoes.items():
                f.write(f"({estado_atual}, {simbolo_atual}) -> ({proximo_estado}, {simbolo_escrito}, {movimento})\n")


    def imprimir_fita(self):
        fita_str = ''.join(self.fita)
        return fita_str[:self.cabeca] + '|' + fita_str[self.cabeca:]

    def linguagemRegular(self, cadeia):
        self.cabeca = 0
        self.fita = list(cadeia) + ['_']
        self.estado_atual = self.estado_inicial

        print("Início da execução:")
        print("Estado: ", self.estado_atual)
        print("Fita:   ", self.imprimir_fita())

        while 0 <= self.cabeca < len(self.fita):
            simbolo_atual = self.fita[self.cabeca]
            if (self.estado_atual, simbolo_atual) in self.transicoes:
                proximo_estado, simbolo_escrito, movimento = self.transicoes[(self.estado_atual, simbolo_atual)]
                self.fita[self.cabeca] = simbolo_escrito
                self.estado_atual = proximo_estado
                if movimento == "R":
                    self.cabeca += 1
                elif movimento == "L":
                    self.cabeca -= 1

                print("Estado: ", self.estado_atual)
                print("Fita:   ", self.imprimir_fita())
            else:
                break
        
        return "Sim" if self.estado_atual in self.estado_final else "Não"

# Especificação da Máquina de Turing para Linguagem {a^n b^n | n > 0}
spec = {
    "E": ["q0", "q1", "q2", "q3", "q4", "q_accept", "q_reject"],
    "Σ": ["a", "b"],
    "Γ": ["a", "b", "A", "B", "_"],
    "x": "q0",
    "y": "q_reject",
    "δ": {
        ("q0", "a"): ("q1", "A", "R"),
        ("q0", "b"): ("q_reject", "b", "R"),
        ("q0", "_"): ("q0", "_", "R"),
        ("q0", "B"): ("q3", "B", "R"),

        ("q1", "a"): ("q1", "a", "R"),
        ("q1", "b"): ("q2", "B", "L"),
        ("q1", "B"): ("q1", "B", "R"),
        ("q1", "_"): ("q_reject", "_", "R"),

        ("q2", "a"): ("q2", "a", "L"),
        ("q2", "A"): ("q0", "A", "R"),
        ("q2", "B"): ("q2", "B", "L"),
        ("q2", "_"): ("q_reject", "_", "R"),

        ("q3", "B"): ("q3", "B", "R"),
        ("q3", "_"): ("q_accept", "_", "R"),
    },
    "F": ["q_accept"]
}

# Verificação de Palíndromos
spec2 = {
    "E": ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q_accept", "q_reject"],
    "Σ": ["a", "b"],
    "Γ": ["a", "b", "A", "B", "_"],
    "x": "q0",
    "y": "q_reject",
    "δ": {
        ("q0", "a"): ("q1", "_", "R"),
        ("q0", "b"): ("q2", "_", "R"),
        ("q0", "_"): ("q_accept", "_", "R"),

        ("q1", "a"): ("q3", "a", "R"),
        ("q1", "b"): ("q1", "b", "R"),
        ("q1", "_"): ("q_accept", "_", "R"),

        ("q2", "a"): ("q4", "a", "R"),
        ("q2", "b"): ("q4", "b", "R"),
        ("q2", "_"): ("q_accept", "_", "R"),

        ("q3", "a"): ("q3", "a", "R"),
        ("q3", "b"): ("q3", "b", "R"),
        ("q3", "_"): ("q5", "_", "L"),

        ("q4", "a"): ("q4", "a", "R"),
        ("q4", "b"): ("q4", "b", "R"),
        ("q4", "_"): ("q6", "_", "L"),
        
        ("q5", "a"): ("q7", "_", "L"),

        ("q6", "b"): ("q7", "_", "L"),

        ("q7", "a"): ("q7", "a", "L"),
        ("q7", "b"): ("q7", "b", "L"),
        ("q7", "_"): ("q0", "_", "R"),
    },
    "F": ["q_accept"]
}

def input_specification():
    print("Digite a especificação da Máquina de Turing.")
    
    estados = input("Estados (separados por vírgula): ").split(',')
    alfabeto = input("Alfabeto (separado por vírgula): ").split(',')
    alfabeto_fita = input("Alfabeto da fita (separado por vírgula): ").split(',')
    estado_inicial = input("Estado inicial: ")
    estado_rejeicao = input("Estado de rejeição: ")
    estados_finais = input("Estados finais (separados por vírgula): ").split(',')
    
    transicoes = {}
    print("Digite as transições no formato (estado_atual, simbolo_atual): (proximo_estado, simbolo_escrito, movimento)")
    print("Para finalizar, deixe a entrada em branco e pressione Enter.")
    
    while True:
        transicao = input("Transição: ")
        if transicao == "":
            break
        try:
            chave, valor = transicao.split(') -> (')
            chave = tuple(chave.strip('(').strip(')').split(', '))
            valor = tuple(valor.strip(')').split(', '))
            transicoes[chave] = (valor[0], valor[1], valor[2])
        except ValueError:
            print("Formato inválido. Tente novamente.")
    
    specification = {
        "E": estados,
        "Σ": alfabeto,
        "Γ": alfabeto_fita,
        "x": estado_inicial,
        "y": estado_rejeicao,
        "δ": transicoes,
        "F": estados_finais
    }
    return specification

def carregar_especificacao(arquivo):
    spec = {"E": [], "Σ": [], "Γ": [], "x": "", "y": "", "F": [], "δ": {}}
    
    try:
        with open(arquivo, 'r') as f:
            linhas = f.readlines()

            idx = 0

            # Processa cada seção do arquivo
            try:
                spec['E'] = linhas[idx].strip().split(':')[1].strip().split(',')
                idx += 1
            except IndexError:
                print("Erro ao processar estados.")
                return spec

            try:
                spec['Σ'] = linhas[idx].strip().split(':')[1].strip().split(',')
                idx += 1
            except IndexError:
                print("Erro ao processar alfabeto.")
                return spec

            try:
                spec['Γ'] = linhas[idx].strip().split(':')[1].strip().split(',')
                idx += 1
            except IndexError:
                print("Erro ao processar alfabeto da fita.")
                return spec

            try:
                spec['x'] = linhas[idx].strip().split(':')[1].strip()
                idx += 1
            except IndexError:
                print("Erro ao processar estado inicial.")
                return spec

            try:
                spec['y'] = linhas[idx].strip().split(':')[1].strip()
                idx += 1
            except IndexError:
                print("Erro ao processar estado de rejeição.")
                return spec

            try:
                spec['F'] = linhas[idx].strip().split(':')[1].strip().split(',')
                idx += 1
            except IndexError:
                print("Erro ao processar estados finais.")
                return spec

            # Processa as transições
            while idx < len(linhas):
                linha = linhas[idx].strip()
                if linha and '->' in linha:
                    try:
                        chave, valor = linha.split(') -> (')
                        chave = tuple(chave.strip('(').split(', '))
                        valor = tuple(valor.strip(')').split(', '))
                        if len(chave) == 2 and len(valor) == 3:
                            spec['δ'][chave] = (valor[0], valor[1], valor[2])
                        else:
                            print(f"Formato de transição inválido na linha: {linha}")
                    except ValueError as e:
                        print(f"Formato de transição inválido na linha: {linha}. Erro: {e}")
                idx += 1

    except FileNotFoundError:
        print("Arquivo de especificação não encontrado.")
    
    return spec

def MT():
    while True:

        print("Menu")
        print("1. Linguagem Regular a^n b^n | n > 0")
        print("2. Verificação de Palíndromos")
        print("3. Definir Especificação da Máquina de Turing")
        print("4. Testar máquina de Turing criada")
        print("5. Voltar")
        try:

            opcao = int(input("Opcao: "))

            if opcao == 1:
                turing = TuringMachine(spec)
                entrada = input("Digite a cadeia para a Máquina de Turing (composta por 'a' e 'b'): ")
                resultado = turing.linguagemRegular(entrada)
                print(resultado)
                continue

            elif opcao == 2:
                turing = TuringMachine(spec2)
                entrada = input("Digite a cadeia: ")
                resultado = turing.linguagemRegular(entrada)
                print(resultado)
                continue

            elif opcao == 3:
                spec_user = input_specification() #formato (estado_atual, simbolo) -> (estado_prox, escrita, movimento do cabeçote)
                turing = TuringMachine(spec_user)
                turing.salvar_especificacao("maquina_turing.txt")
                entrada = input("Digite a cadeia: ")
                resultado = turing.linguagemRegular(entrada)
                print(resultado)
                continue

            elif opcao == 4:
                spec_user = carregar_especificacao("maquina_turing.txt")  
                turing = TuringMachine(spec_user) 
                entrada = input("Digite a cadeia: ")
                resultado = turing.linguagemRegular(entrada) 
                print(resultado)
                continue

            elif opcao == 5:
                break

            else:
                print("Opção inválida")

        except ValueError:
            print('Erro: Você deve entrar com um número inteiro.')