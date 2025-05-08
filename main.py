from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)
livros = []

@app.route('/')
def index():
    return render_template('index.html', livros=livros, hoje=datetime.now())

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        livros.append({
            'id': len(livros),
            'titulo': titulo,
            'autor': autor,
            'emprestado': False,
            'data_devolucao': None
        })
        return redirect(url_for('index'))
    return render_template('adicionar.html')

@app.route('/editar/<int:livro_id>', methods=['GET', 'POST'])
def editar(livro_id):
    livro = livros[livro_id]
    if request.method == 'POST':
        livro['titulo'] = request.form['titulo']
        livro['autor'] = request.form['autor']
        return redirect(url_for('index'))
    return render_template('editar.html', livro=livro)

@app.route('/excluir/<int:livro_id>')
def excluir(livro_id):
    livros.pop(livro_id)
    return redirect(url_for('index'))

@app.route('/emprestar/<int:livro_id>')
def emprestar(livro_id):
    livro = livros[livro_id]
    livro['emprestado'] = True
    livro['data_devolucao'] = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    return redirect(url_for('index'))

@app.route('/devolver/<int:livro_id>')
def devolver(livro_id):
    livro = livros[livro_id]
    if livro['data_devolucao']:
        data_devolucao = datetime.strptime(livro['data_devolucao'], '%Y-%m-%d')
        dias_atraso = (datetime.now() - data_devolucao).days
        if dias_atraso > 0:
            multa = 10 + (dias_atraso * 0.10)
            livro['multa'] = round(multa, 2)
        else:
            livro['multa'] = 0
    livro['emprestado'] = False
    livro['data_devolucao'] = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)