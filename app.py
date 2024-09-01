from flask import Flask, render_template, request, redirect, url_for
from turing import TuringMachine, spec, spec2, input_specification, carregar_especificacao

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/linguagem', methods=['POST'])
def linguagem():
    cadeia = request.form['cadeia']
    turing = TuringMachine(spec)
    resultado, fitas = turing.linguagemRegular(cadeia)
    return render_template('index.html', resultado=resultado, fita=fitas, tab="linguagem")

@app.route('/palindromo', methods=['POST'])
def palindromo():
    cadeia = request.form['cadeia_palindromo']
    turing = TuringMachine(spec2)
    resultado, fitas = turing.linguagemRegular(cadeia)
    return render_template('index.html', resultado_palindromo=resultado, fita=fitas, tab="palindromo")

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
    return render_template('index.html', resultado_definir="Especificação salva com sucesso!", tab="definir")

@app.route('/testar', methods=['POST'])
def testar():
    cadeia = request.form['entrada']
    specification = carregar_especificacao('maquina_turing.txt')
    turing = TuringMachine(specification)
    resultado, fitas = turing.linguagemRegular(cadeia)
    return render_template('index.html', resultado_testar=resultado, fita=fitas, tab="testar")

if __name__ == '__main__':
    app.run(debug=True)
