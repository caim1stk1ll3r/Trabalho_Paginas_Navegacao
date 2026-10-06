from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'chave-secreta-fatec-2026'

@app.route('/')
def pagina_inicial():
    return render_template ('index.html')

@app.route('/produtos')
def produtos():
    return render_template ('produtos.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':

        nome   = request.form.get('nome', '').strip()
        email  = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        nascimento = request.form.get('nascimento', '')
        perfil = request.form.get('perfil', 'usuario')
        termos = request.form.get('termos')

        erros = []

        if not nome:
            erros.append('O nome é obrigatório.')
        elif len(nome) < 3:
            erros.append('O nome deve ter pelo menos 3 caracteres.')

        if not email:
            erros.append('O e-mail é obrigatório.')
        elif '@' not in email or '.' not in email:
            erros.append('Digite um e-mail válido.')

        if not nascimento:
            erros.append('Informe sua data de nascimento.')

        if not termos:
            erros.append('Você deve aceitar os termos de uso.')

        # ===== PROCESSAMENTO OU EXIBIÇÃO DE ERROS =====
        if erros:
            for erro in erros:
                flash(erro, 'danger')
            return render_template('cadastro.html',
                                nome=nome,
                                email=email,
                                nascimento=nascimento,
                                termos=termos,
                                perfil=perfil)

        print(f'✅ Cadastro válido: {nome} | {email} | {nascimento} | {perfil}')
        flash(f'Cadastro de {nome} realizado com sucesso!', 'success')

        return redirect(url_for('pagina_inicial'))

    return render_template('cadastro.html')

@app.route('/usuarios')
def usuarios():
    return render_template ('usuarios.html')

@app.route('/processar', methods=['POST'])
def processar():
    nome = request.form['nome']
    username = request.form.get('username')
    perfil = request.form.get('perfil', 'usuario')
    aceito_termos = request.form.get('termos', 'nao')
    nascimento_str = request.form['nascimento']

    idade = datetime - nascimento_str 

    return f'Dados recebidos: {nome}, {username}, {perfil}, termos: {aceito_termos}, {idade}'














































if __name__ == '__main__':
    app.run(debug=True)