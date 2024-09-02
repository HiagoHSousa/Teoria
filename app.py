from flask import Flask, render_template, request, redirect, url_for
from turing import TuringMachine, spec, spec2, input_specification, carregar_especificacao
import criar
import ler
import os
import functions
import conversao
import minimiza
from graphviz import Digraph

folAFD = "static/AFD/"
folAFN = "static/AFN/"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criar_af', methods=['GET', 'POST'])
def criar_af():
    if request.method == 'POST':
        tipo_af = request.form.get('tipo_af')
        estados = request.form.get('estados', '').split()
        alfabeto = request.form.get('alfabeto', '').split()
        estado_inicial = request.form.get('estado_inicial', '')
        estados_finais = request.form.get('estados_finais', '').split()
        transicoes = request.form.get('transicoes', '').strip().split('\n')

        func_transicao = {}
        for transicao in transicoes:
            parts = transicao.split(',')
            if len(parts) == 3:
                estado, simbolo, proximo_estado = parts
                func_transicao[(estado.strip(), simbolo.strip())] = proximo_estado.strip().split()

        if tipo_af == 'AFD':
            fol = "static/AFD/"
            func_transicao = {k: v[0] for k, v in func_transicao.items() if v != ['*']}
        else:
            fol = "static/AFN/"

        if not os.path.exists(fol):
            os.makedirs(fol)

        arquivo = functions.arquivoAutomato(fol, func_transicao)
        arquivo.close()

        estados_arq = functions.crEstados(fol, estados)
        estados_arq.close()

        informacoes = functions.informacaoAutomato(fol, estado_inicial, estados_finais, alfabeto)
        informacoes.close()

        delta_lista = functions.converter_para_lista_transicoes(func_transicao)
        Automato = functions.desenhar_automato(estado_inicial, estados_finais, delta_lista)
        Automato.render(fol + 'desenhoAF', format='png', cleanup=True)

        return render_template('resultado.html', tipo=tipo_af, image_path=f"{tipo_af}/desenhoAF.png")

    return render_template('criar_af.html')

@app.route('/ler_af', methods=['GET', 'POST'])
def ler_af():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        entrada = request.form.get('entrada')
        
        if tipo == 'afd':
            estado_inicial, estados_finais, alfabeto = functions.extrairInfAF(folAFD, "", [], [])
            func_transicao = functions.extrairDict(folAFD)
            
            estado_atual = estado_inicial
            for simbolo in entrada:
                estado_atual = func_transicao.get((estado_atual, simbolo))
                if estado_atual is None:
                    mensagem = "O automato não reconheceu a linguagem"
                    break
            else:
                if estado_atual in estados_finais:
                    mensagem = "O automato reconheceu a linguagem"
                else:
                    mensagem = "O automato não reconheceu a linguagem"
        
        elif tipo == 'afn':
            estado_inicial, estados_finais, alfabeto = functions.extrairInfAF(folAFN, "", [], [])
            func_transicao = functions.extrairDict(folAFN)
            
            estados_atuais = [estado_inicial]
            for simbolo in entrada:
                novos_estados = []
                for estado_atual in estados_atuais:
                    prox_estados = func_transicao.get((estado_atual, simbolo), [])
                    novos_estados.extend(prox_estados)
                estados_atuais = novos_estados
            if any(estado in estados_finais for estado in estados_atuais):
                mensagem = "O automato reconheceu a linguagem"
            else:
                mensagem = "O automato não reconheceu a linguagem"
    
        # Definir o caminho da imagem com base no tipo
        imagem_automato = url_for('static', filename=f'{tipo}/desenhoAF.png')

        return render_template('resultado_ler.html', mensagem=mensagem, entrada=entrada, tipo=tipo, imagem_automato=imagem_automato)
    
    return render_template('ler_af.html')

@app.route('/conversao_afn_afd', methods=['GET', 'POST'])
def converter_afn_afd():
    if request.method == 'POST':
        try:
            tam_palavra = int(request.form['tam_palavra'])
        except KeyError:
            return "Erro: O campo 'tam_palavra' está faltando no formulário.", 400
        except ValueError:
            return "Erro: O valor do campo 'tam_palavra' não é válido.", 400

        # Continue com a lógica de conversão
        folAFN = "static/AFN/"
        folAFD = "static/AFD/"

        # Inicia a conversão de AFN para AFD
        func_transicaoAFN = functions.extrairDict(folAFN)
        estado_inicial, estados_finais, alfabeto = functions.extrairInfAF(folAFN, "", set(), set())

        estadoIniLista = [estado_inicial]  # Deixa como lista o estado inicial para fazer as transições posteriormente

        # Informações AFD
        estadosAFD = []
        tabTranAFD = {}
        estados_finaisAFD = []

        fila = [estadoIniLista]  # Vai armazenar os estados

        while fila:
            estado_atual = fila.pop(0)
            estadoAtualStr = "".join(estado_atual)

            # Adiciona o estado atual à lista de estados do AFD
            if estadoAtualStr not in ["" .join(e) for e in estadosAFD]:
                estadosAFD.append(estado_atual)

            for simbolo in alfabeto:
                estado_seguinte = []  # Armazena os estados que virão a partir do atual

                for estado in estado_atual:
                    if (estado, simbolo) in func_transicaoAFN:
                        for novoEstado in func_transicaoAFN[(estado, simbolo)]:
                            if novoEstado not in estado_seguinte:
                                estado_seguinte.append(novoEstado)  # Adiciona um estado na lista de seguinte caso ele não exista

                if estado_seguinte:
                    estadoSegStr = "".join(estado_seguinte)
                    tabTranAFD[(estadoAtualStr, simbolo)] = estadoSegStr

                    if estado_seguinte not in estadosAFD:
                        fila.append(estado_seguinte)

            if any(estado in estados_finais for estado in estado_atual):
                estados_finaisAFD.append(estadoAtualStr)

        # Salva o AFD em um arquivo
        functions.arquivoAutomato(folAFD, tabTranAFD).close()
        functions.informacaoAutomato(folAFD, estado_inicial, estados_finaisAFD, alfabeto).close()
        functions.crEstados(folAFD, ["".join(e) for e in estadosAFD]).close()

        # Desenhar o AFD convertido
        automato = Digraph()
        automato.attr(rankdir='LR')
        automato.attr('node', shape='circle')

        automato.node('->', shape='none', width='0', height='0', label='')
        automato.edge('->', estado_inicial)

        for estado_final in estados_finaisAFD:
            automato.node(estado_final, shape='doublecircle', fontsize='17')

        for (estado, simbolo) in tabTranAFD:
            destino = tabTranAFD[(estado, simbolo)]
            automato.edge(estado, destino, label=simbolo)

        caminho_imagem = folAFD + 'AFDConvertido.png'
        automato.render(folAFD + 'AFDConvertido', format='png', cleanup=True)

        return render_template('resultado_conversao.html', entrada=tam_palavra, mensagem="Conversão concluída com sucesso!", imagem_automato=url_for('static', filename='AFD/AFDConvertido.png'))

    return render_template('conversao_afn_afd.html')


@app.route('/resultado_conversao')
def resultado_conversao():
    return render_template('resultado_conversao.html')

@app.route('/minimizar', methods=['GET', 'POST'])
def minimizar_afd():
    if request.method == 'POST':
        minimiza.minizacaoAFD()
        return redirect(url_for('index'))
    return render_template('minimizar.html')

@app.route('/turing', methods=['GET', 'POST'])
def maquina_turing():
    return render_template('turing.html')

@app.route('/sair')
def sair():
    return "Saindo do sistema"


@app.route('/linguagem', methods=['POST'])
def linguagem():
    cadeia = request.form['cadeia']
    turing = TuringMachine(spec)
    resultado, fitas = turing.linguagemRegular(cadeia)
    return render_template('turing.html', resultado=resultado, fita=fitas, tab="linguagem")

@app.route('/palindromo', methods=['POST'])
def palindromo():
    cadeia = request.form['cadeia_palindromo']
    turing = TuringMachine(spec2)
    resultado, fitas = turing.linguagemRegular(cadeia)
    return render_template('turing.html', resultado_palindromo=resultado, fita=fitas, tab="palindromo")

@app.route('/definir', methods=['POST'])
def definir():
    estados = request.form['estados']
    alfabeto = request.form['alfabeto']
    alfabeto_fita = request.form['alfabeto_fita']
    estado_inicial = request.form['estado_inicial']
    estado_rejeicao = request.form['estado_rejeicao']
    estados_finais = request.form['estados_finais']
    transicoes = request.form['transicoes']

    specification = {
        "E": estados.split(','),
        "Σ": alfabeto.split(','),
        "Γ": alfabeto_fita.split(','),
        "x": estado_inicial,
        "y": estado_rejeicao,
        "δ": {},
        "F": estados_finais.split(',')
    }

    for transicao in transicoes.split('\n'):
        if transicao:
            chave, valor = transicao.split(') -> (')
            chave = tuple(chave.strip('(').strip(')').split(', '))
            valor = tuple(valor.strip(')').split(', '))
            specification['δ'][chave] = (valor[0], valor[1], valor[2])

    turing = TuringMachine(specification)
    turing.salvar_especificacao('maquina_turing.txt')
    return render_template('turing.html', resultado_definir="Especificação salva com sucesso!", tab="definir")

@app.route('/testar', methods=['POST'])
def testar():
    cadeia = request.form['entrada']
    specification = carregar_especificacao('maquina_turing.txt')
    turing = TuringMachine(specification)
    resultado, fitas = turing.linguagemRegular(cadeia)
    return render_template('turing.html', resultado_testar=resultado, fita=fitas, tab="testar")

if __name__ == '__main__':
    app.run(debug=True)
