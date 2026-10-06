from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'chave-secreta-fatec-2026'


@app.route('/')
def pagina_inicial():
    # Dados enviados ao template (Aula 03: dicionário + **dados)
    dados = {
        'titulo': 'Tabacaria',
        'subtitulo': 'Fumos, sedas, isqueiros e acessórios em um só lugar',
    }
    return render_template('index.html', **dados)


@app.route('/produtos')
def produtos():
    # Lista de dicionários simulando os registros (Aula 03)
    lista = [
        {'id': 1, 'nome': 'Fumo de Corda',      'categoria': 'Fumos',      'preco': 12.50, 'estoque': 40, 'ativo': True},
        {'id': 2, 'nome': 'Seda Slim',          'categoria': 'Sedas',      'preco':  4.90, 'estoque': 85, 'ativo': True},
        {'id': 3, 'nome': 'Isqueiro Recarregável', 'categoria': 'Acessórios', 'preco': 9.90, 'estoque': 3, 'ativo': True},
        {'id': 4, 'nome': 'Piteira de Vidro',   'categoria': 'Acessórios', 'preco':  7.00, 'estoque': 0,  'ativo': False},
        {'id': 5, 'nome': 'Narguilé Médio',     'categoria': 'Narguilés',  'preco': 189.90, 'estoque': 6, 'ativo': True},
        {'id': 6, 'nome': 'Essência para Narguilé', 'categoria': 'Narguilés', 'preco': 15.00, 'estoque': 22, 'ativo': True},
    ]
    return render_template('produtos.html', produtos=lista, total=len(lista))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
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
            # Re-popula o formulário com o que o usuário já digitou (Aula 04)
            return render_template('cadastro.html',
                                   nome=nome,
                                   email=email,
                                   username=username,
                                   nascimento=nascimento,
                                   termos=termos,
                                   perfil=perfil)

        print(f'✅ Cadastro válido: {nome} | {email} | {username} | {nascimento} | {perfil}')
        flash(f'Cadastro de {nome} realizado com sucesso!', 'success')
        # Padrão PRG: redirect após POST bem-sucedido (Aula 04)
        return redirect(url_for('pagina_inicial'))

    return render_template('cadastro.html')


@app.route('/usuarios')
def usuarios():
    # Lista simulada de usuários (Aula 03)
    lista = [
        {'nome': 'Administrador',  'username': 'admin', 'email': 'admin@tabacaria.com', 'perfil': 'admin',   'ativo': True},
        {'nome': 'João Silva',     'username': 'joao',  'email': 'joao@email.com',      'perfil': 'editor',  'ativo': True},
        {'nome': 'Maria Souza',    'username': 'maria', 'email': 'maria@email.com',     'perfil': 'usuario', 'ativo': False},
    ]
    return render_template('usuarios.html', usuarios=lista, total=len(lista))


@app.route('/processar', methods=['POST'])
def processar():
    nome = request.form['nome']
    username = request.form.get('username')
    perfil = request.form.get('perfil', 'usuario')
    aceito_termos = request.form.get('termos', 'nao')
    nascimento_str = request.form['nascimento']

    # request.form sempre devolve string: converte para data antes de calcular
    try:
        nascimento = datetime.strptime(nascimento_str, '%Y-%m-%d')
    except ValueError:
        return 'Data de nascimento inválida.', 400

    hoje = datetime.today()
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))

    return f'Dados recebidos: {nome}, {username}, {perfil}, termos: {aceito_termos}, {idade} anos'


if __name__ == '__main__':
    app.run(debug=True)
