from flask import Flask, render_template, request, redirect, url_for, session, flash 
from sqlalchemy import func 
from flask import Flask, render_template
from servico import Servico
from plano import Planos
from administracao import Administracao
from extensions import db
from funcionario import Funcionario
from contratos import Contrato
from pessoas import Pessoas
from departamentos import Projeto
from entidadeexterna import EntidadeExterna

app = Flask(__name__)
app.secret_key = 'amoprogramar'

usuarios = {
    'rayane@datasphere.com': 'senha123',
    'Giulio@datasphere.com': 'senha123',
    'Igor@datasphere.com': 'senha123',
    'Wallisson@datasphere.com': 'senha123',
    'Christian@datasphere.com': 'senha123',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['password']

    if email in usuarios and usuarios[email] == senha:
        session['usuario'] = email
        return redirect(url_for('home'))
    else:
        flash('E-mail ou senha inválidos. Tente novamente.')
        return redirect(url_for('index'))
    
@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        email_cadastro = request.form['email_cadastro']
        senha = request.form['password']
        confirmar_senha = request.form['confirm_password']

        if email_cadastro in usuarios:
            flash('E-mail já cadastrado. Faça login ou use outro e-mail.')
            return redirect(url_for('cadastro'))

        if senha != confirmar_senha:
            flash('As senhas não coincidem. Tente novamente.')
            return redirect(url_for('cadastro'))

        usuarios[email_cadastro] = senha
        flash('Cadastro realizado com sucesso! Faça login.')
        return redirect(url_for('home'))
    
    return render_template('cadastro.html')
    
@app.route('/home')
def home():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    
    numero_servicos = Servico.query.count()
    numero_planos = Planos.query.count()
    numero_contratos = Contrato.query.count()
    numero_funcionario= Funcionario.query.count()
    numero_entidade=EntidadeExterna.query.count()
    total_arrecadado = db.session.query(
        func.sum(Planos.preco_plano * (1 - Planos.desconto / 100))
    ).scalar() or 0  
    
    return render_template(
        'home.html',
        numero_servicos=numero_servicos,
        numero_planos=numero_planos,numero_contratos=numero_contratos, 
        total_arrecadado=total_arrecadado, numero_funcionario=numero_funcionario,numero_entidade=numero_entidade
    )

@app.route('/servicos', methods=['GET', 'POST'])
def servicos():
    if request.method == 'POST':
        nome_solucao = request.form['nome_solucao']
        descricao_solucao = request.form['descricao_solucao']
        horario = request.form['horario']
        data= request.form['data']

        print(f"Horário recebido: {horario}") 
        
        consultor_disponivel = Servico.horario_disponivel(horario) 
        servico = Servico(consultor_disponivel=consultor_disponivel, nome_solucao=nome_solucao, 
                          descricao_solucao=descricao_solucao, data=data, horario=horario)

        if servico.agendar_servico():
            flash(f"Serviço '{servico.nome_solucao}' agendado para {data} às {horario}.", 'success')
        else:
            flash("Consultor não disponível para essa data.", 'danger')

        return redirect('/servicos')

    servicos_agendados = Servico.query.all() 
    return render_template('servicos.html', servicos=servicos_agendados)

@app.route('/planos', methods=['GET','POST'])
def planos():
    if request.method == 'POST':
        try:
            servico_id = request.form['servico_id']
            plano_atual = request.form['plano_atual']
            preco_plano = float(request.form['preco_plano'])
            desconto = float(request.form['desconto'])  
        except KeyError as e:
            flash(f"Campo ausente: {str(e)}", 'danger')
            return redirect('/planos')
        except ValueError:
            flash("Erro ao converter preços ou desconto. Verifique os valores.", 'danger')
            return redirect('/planos')

        plano = Planos(servico_id=servico_id, plano_atual=plano_atual, preco_plano=preco_plano, desconto=desconto)
        db.session.add(plano)
        db.session.commit()

        flash(f"Plano '{plano.plano_atual}' cadastrado com sucesso.", 'success')
        return redirect('/planos')

    planos_cadastrados = Planos.query.all() 
    servicos = Servico.query.all()  
    return render_template('planos.html', planos=planos_cadastrados, servicos=servicos)

@app.route('/alterar_plano/<int:plano_id>', methods=['POST'])
def alterar_plano(plano_id):
    plano = Planos.query.get(plano_id)  
    if plano:
        db.session.delete(plano)  
        db.session.commit()  
        flash(f"Plano '{plano.plano_atual}' excluído com sucesso.", 'success')
    else:
        flash("Plano não encontrado.", 'danger')
    
    return redirect('/planos') 

@app.route('/admin',methods=['GET'])
def admin_dashboard():
    if 'usuario' not in session:
        return redirect(url_for('index')) 
    
    funcionarios = Funcionario.query.all()  
    return render_template('administracao.html', funcionarios=funcionarios, mensagem="")

@app.route("/gerar_relatorio", methods=["POST"])
def gerar_relatorio():
    return render_template("administracao.html", funcionarios=Funcionario.query.all(), mensagem="Relatório Gerado!")

@app.route("/planejar_reuniao", methods=["POST"])
def planejar_reuniao():
    return render_template("administracao.html", funcionarios=Funcionario.query.all(), mensagem="Reunião Planejada com Sucesso!")

@app.route("/atualizar_orcamento", methods=["POST"])
def atualizar_orcamento():
    return render_template("administracao.html", funcionarios=Funcionario.query.all(), mensagem="Orçamento Atualizado!")

@app.route('/adicionar_funcionario', methods=['POST'])
def adicionar_funcionario():
    nome = request.form.get('nome_funcionario')
    email = request.form.get('email_funcionario')

    admin = Administracao(None, None, None, None, None, None, None, None)
    if not admin.adicionar_funcionario(nome, email):
        flash(f"O e-mail '{email}' já está cadastrado. Tente outro.", 'danger')
    else:
        flash(f"Funcionário '{nome}' adicionado com sucesso!", 'success')

    return redirect(url_for('funcionarios_view'))

@app.route('/remover_funcionario', methods=['POST'])
def remover_funcionario():
    id_funcionario = request.form.get('id_funcionario')  
    
    if id_funcionario:  
        Administracao.remover_funcionario(id_funcionario)
        flash(f"Funcionário com ID {id_funcionario} removido com sucesso!", 'success')
    else:
        flash("ID do funcionário não foi informado.", 'danger')
    
    return redirect(url_for('funcionarios_view'))

@app.route('/funcionarios', methods=['GET', 'POST'])
def funcionarios_view():
    funcionarios = Funcionario.query.all()
    return render_template('administracao.html', funcionarios=funcionarios)

@app.route('/admin')
def admin():
    return render_template('administracao.html')

@app.route('/contratos')
def contratos():
    contratos = Contrato.query.all()
    return render_template('contratos.html', contratos=contratos)

@app.route('/adicionar_contrato', methods=['POST'])
def adicionar_contrato():
    numero_contrato = request.form.get('numero_contrato')
    data_inicio = request.form.get('data_inicio')
    data_fim = request.form.get('data_fim')
    descricao_contrato = request.form.get('descricao_contrato')
    
    novo_contrato = Contrato(
        numero_contrato=numero_contrato,
        data_inicio=data_inicio,
        data_fim=data_fim,
        descricao_contrato=descricao_contrato
    )
    db.session.add(novo_contrato)
    db.session.commit()
    return redirect(url_for('contratos'))

@app.route('/assinar/<int:id>', methods=['POST'])
def assinar(id):
    contrato = Contrato.query.get(id)
    assinatura = request.form.get('assinatura')
    contrato.assinar_contrato(assinatura)
    db.session.commit()
    return redirect(url_for('contratos'))

@app.route('/rescindir/<int:id>', methods=['POST'])
def rescindir(id):
    contrato = Contrato.query.get(id)
    contrato.rescindir_contrato()
    db.session.commit()
    return redirect(url_for('contratos'))

@app.route('/renovar/<int:id>', methods=['POST'])
def renovar(id):
    contrato = Contrato.query.get(id)
    nova_data_fim = request.form.get('nova_data_fim')
    contrato.renovar_contrato(nova_data_fim)
    db.session.commit()
    return redirect(url_for('contratos'))

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    contrato = Contrato.query.get(id)
    nova_descricao = request.form.get('nova_descricao')
    contrato.atualizar_contrato(nova_descricao)
    db.session.commit()
    return redirect(url_for('contratos'))

@app.route('/projetos', methods=['GET', 'POST'])
def gerenciar_projetos():
    if request.method == 'POST':
        nome_do_projeto = request.form.get('nome_do_projeto')
        objetivos = request.form.get('obj_met')
        membros = request.form.get('membros')
        data_termino = request.form.get('dt')


        novo_projeto = Projeto(
            nome_do_projeto=nome_do_projeto,
            objetivos=objetivos,
            membros=membros,
            data_termino=data_termino
        )
        db.session.add(novo_projeto)
        db.session.commit()

        flash(f"Projeto '{nome_do_projeto}' cadastrado com sucesso!", 'success')
        return redirect(url_for('gerenciar_projetos'))


    projetos = Projeto.query.all()
    return render_template('departamentos.html', projetos=projetos)

@app.route('/concluir_projeto/<int:id>', methods=['POST'])
def concluir_projeto(id):
    projeto = Projeto.query.get(id)
    if projeto:
        db.session.delete(projeto)
        db.session.commit()
        flash(f"Projeto '{projeto.nome_do_projeto}' concluído e removido!", 'success')
    else:
        flash("Projeto não encontrado.", 'danger')
    return redirect(url_for('gerenciar_projetos'))

@app.route('/departamentos')
def departamentos():
    return render_template('departamentos.html')

@app.route('/entidade_externa')
def entidade_externa():
    entidades = EntidadeExterna.query.all()
    if not entidades:
        flash("Nenhuma entidade cadastrada ainda.", 'info')
    return render_template('entidade-externa.html', entidades=entidades)

@app.route('/empresaparceira')
def empresaparceira():
    return render_template('empresaparceira.html')

@app.route('/empresacliente')
def empresacliente():
    return render_template('empresacliente.html')

@app.route('/entidades')
def entidades():
    entidades = EntidadeExterna.query.all()
    if not entidades:
        flash("Nenhuma entidade cadastrada ainda.", 'info')
    return render_template('entidade-externa.html', entidades=entidades)

@app.route('/adicionar_entidade', methods=['POST'])
def adicionar_entidade():
    try:
        razao_social = request.form.get('razao_social')
        cnpj = request.form.get('cnpj')
        faturamento = float(request.form.get('faturamento'))
        recorrencia = request.form.get('recorrencia')

        nova_entidade = EntidadeExterna(
            razao_social=razao_social,
            cnpj=cnpj,
            faturamento=faturamento,
            recorrencia=recorrencia
        )
        db.session.add(nova_entidade)
        db.session.commit()
        flash("Entidade adicionada com sucesso!", 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao adicionar entidade: {e}", 'danger')
    return redirect(url_for('entidades'))

@app.route('/editar_entidade/<int:id>', methods=['POST'])
def editar_entidade(id):
    entidade = EntidadeExterna.query.get(id)
    if entidade:
        try:
            razao_social = request.form.get('razao_social')
            cnpj = request.form.get('cnpj')
            faturamento = float(request.form.get('faturamento'))
            recorrencia = request.form.get('recorrencia')

            entidade.editar_entidade(razao_social, cnpj, faturamento, recorrencia)
            db.session.commit()
            flash("Entidade editada com sucesso!", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao editar entidade: {e}", 'danger')
    else:
        flash("Entidade não encontrada.", 'danger')
    return redirect(url_for('entidades'))

@app.route('/excluir_entidade/<int:id>', methods=['POST'])
def excluir_entidade(id):
    entidade = EntidadeExterna.query.get(id)
    if entidade:
        try:
            db.session.delete(entidade)
            db.session.commit()
            flash("Entidade excluída com sucesso!", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao excluir entidade: {e}", 'danger')
    else:
        flash("Entidade não encontrada.", 'danger')
    return redirect(url_for('entidades'))

@app.route('/excluir_projeto/<int:id>', methods=['POST'])
def excluir_projeto(id):
    projeto = Projeto.query.get(id)
    if projeto:
        db.session.delete(projeto)
        db.session.commit()
        flash(f"Projeto '{projeto.nome_do_projeto}' excluído com sucesso!", 'success')
    else:
        flash("Projeto não encontrado.", 'danger')
    return redirect(url_for('gerenciar_projetos'))

@app.route('/pessoas', methods=['GET', 'POST'])
def cadastrar_pessoas():
    if request.method == 'POST':
        nome = request.form.get('nome_pessoa')
        cpf = request.form.get('cpf_pessoa')
        cnpj = request.form.get('cnpj_pessoa')
        email = request.form.get('email_pessoa')
        celular = request.form.get('celular_pessoa')
        endereco = request.form.get('endereco_pessoa')
        nascimento = request.form.get('nascimento_pessoa')
        atribuicao = request.form.get('atribuicao_pessoa')

        if not all([nome, cpf, cnpj, email, celular, endereco, nascimento, atribuicao]):
            flash("Todos os campos são obrigatórios!", "danger")
            return render_template('pessoas.html')

        pessoa = Pessoas(nome, cpf, cnpj, email, celular, endereco, nascimento, atribuicao)
        pessoa.registrar()

 
        flash(f"Pessoa {nome} registrada com sucesso!", "success")
        return render_template('pessoas.html')

    return render_template('pessoas.html')

@app.route('/employee', methods=['GET', 'POST'])
def employee():
    if request.method == 'POST':
        nome = request.form.get('nome_funcionario')
        cpf = request.form.get('cpf_funcionario')
        cnpj = request.form.get('cnpj_funcionario')
        email = request.form.get('email_funcionario')
        celular = request.form.get('celular_funcionario')
        endereco = request.form.get('endereco_funcionario')
        nascimento = request.form.get('nascimento_funcionario')
        atribuicao = request.form.get('atribuicao_funcionario')
        cargo = request.form.get('cargo_funcionario')
        salario = request.form.get('salario_funcionario')
        ocupacao = request.form.get('ocupacao_funcionario')
        modelo_de_trabalho = request.form.get('modelo_de_trabalho_funcionario')

        if not all([nome, cpf, email, celular, endereco, nascimento, atribuicao, cargo, salario, ocupacao, modelo_de_trabalho]):
            flash("Todos os campos obrigatórios devem ser preenchidos!", "danger")
            return redirect(url_for('employee'))
        try:
            funcionario = Funcionario(
                nome=nome,
                cpf=cpf,
                cnpj=cnpj,
                email=email,
                celular=celular,
                endereco=endereco,
                nascimento=nascimento,
                atribuicao=atribuicao,
                cargo=cargo,
                salario=float(salario),
                ocupacao=ocupacao,
                modelo_de_trabalho=modelo_de_trabalho
            )
            funcionario.admitir_funcionario(funcionario)
            flash(f"Funcionário {nome} cadastrado com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao cadastrar funcionário: {str(e)}", "danger")

        return redirect(url_for('employee'))

    return render_template('funcionarios.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True, host='0.0.0.0', port=5000)