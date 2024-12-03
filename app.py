from flask import Flask, render_template, request, redirect, url_for, session, flash 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import func 
import random
from flask import Flask, render_template
from datetime import datetime
from servico import db, Servico
from plano import db, Planos


app = Flask(__name__)
app.secret_key = 'amoprogramar:)'

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

    
with app.app_context():
    db.create_all()


class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_do_projeto = db.Column(db.String(100), nullable=False)
    objetivos = db.Column(db.String(200), nullable=False)
    membros = db.Column(db.String(200), nullable=False)
    data_termino = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Projeto {self.nome_do_projeto}>"






@app.route('/servicos', methods=['GET', 'POST'])
def servicos():
    if request.method == 'POST':
        nome_solucao = request.form['nome_solucao']
        descricao_solucao = request.form['descricao_solucao']
        horario = request.form['horario']
        data= request.form['data']

        print(f"Horário recebido: {horario}") 
        
        consultor_disponivel = Servico.horario_disponivel(horario)  # Verifica se o horário é permitido
        servico = Servico(consultor_disponivel=consultor_disponivel, nome_solucao=nome_solucao, 
                          descricao_solucao=descricao_solucao, data=data, horario=horario)

        if servico.agendar_servico():
            flash(f"Serviço '{servico.nome_solucao}' agendado para {data} às {horario}.", 'success')
        else:
            flash("Consultor não disponível para essa data.", 'danger')

        return redirect('/servicos')

    servicos_agendados = Servico.query.all() 
    return render_template('servicos.html', servicos=servicos_agendados)

@app.route('/planos', methods=['GET', 'POST'])
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

class Administracao:
    def __init__(self, id, nome, email, telefone, endereco, data_contratacao, setor, orcamento):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__telefone = telefone
        self.__endereco = endereco
        self.__orcamento = orcamento
        self.funcionarios = []

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
      if len(str(id)) > 10:
         print("O ID não pode ter mais de 10 dígitos.")
      self.__id = id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        self.__telefone = telefone

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, endereco):
        self.__endereco = endereco

    @property
    def orcamento(self):
        return self.__orcamento

    @orcamento.setter
    def orcamento(self, orcamento):
        self.__orcamento = orcamento

    def adicionar_funcionario(self, nome, email):
        # Verifica se o e-mail já está cadastrado
        if Funcionario.query.filter_by(email=email).first():
            print(f"O e-mail '{email}' já está cadastrado.")
            return False  # Indica falha na adição

    # Gera um ID aleatório de 4 dígitos
        funcionario_id = random.randint(1000, 9999)

        funcionario = Funcionario(id=funcionario_id, nome=nome, email=email)
        db.session.add(funcionario)
        db.session.commit()
        print(f"Funcionário {nome} (ID: {funcionario_id}) adicionado com sucesso.")
        return True  # Indica sucesso na adição
    def remover_funcionario(id_funcionario):
        try:
            funcionario = Funcionario.query.get(int(id_funcionario))  # Converte para inteiro
            if funcionario:
                db.session.delete(funcionario)
                db.session.commit()
                print(f"Funcionário com ID {id_funcionario} removido com sucesso.")
            else:
                print(f"Funcionário com ID {id_funcionario} não encontrado.")
        except ValueError:
            print("ID do funcionário inválido. Certifique-se de enviar um número inteiro.")



    def atualizar_orcamento(self, novo_orcamento):
        self.orcamento = novo_orcamento
        print(f"Orçamento atualizado para {novo_orcamento:.2f}.")

    def gerar_relatorio(self):
        relatorio = (f"ID: {self.id}\n"
                     f"Nome: {self.nome}\n"
                     f"Email: {self.email}\n"
                     f"Telefone: {self.telefone}\n"
                     f"Endereço: {self.endereco}\n"
                     f"Orçamento: {self.orcamento:.2f}\n"
                     f"Funcionários: {', '.join(self.funcionarios) if self.funcionarios else 'Nenhum funcionário cadastrado.'}")
        return relatorio

    def consultar_funcionario(self, funcionario):
        if funcionario in self.funcionarios:
            print(f"Funcionário {funcionario} está no setor {self.setor}.")
        else:
            print(f"Funcionário {funcionario} não encontrado.")

    def enviar_email(self, destinatario, assunto, mensagem):
        print(f"Enviando email para {destinatario}...\nAssunto: {assunto}\nMensagem: {mensagem}\nEmail enviado com sucesso.")

    def planejar_reuniao(self, data, hora, local):
        print(f"Reunião planejada para {data} às {hora} no local: {local}.")


class Departamento:
    def __init__(self, nome, setor, email, telefone):
        self.nome = nome
        self.setor = setor
        self.email = email
        self.telefone = telefone
        self.funcionarios = []
        self.projetos = []
        self.gerente = None

    def adicionar_funcionario(self, funcionario):
        self.funcionarios.append(funcionario)
        print(f"Funcionário {funcionario} adicionado ao departamento {self.nome}.")

    def remover_funcionario(self, funcionario):
        if funcionario in self.funcionarios:
            self.funcionarios.remove(funcionario)
            print(f"Funcionário {funcionario} removido do departamento {self.nome}.")
        else:
            print(f"Funcionário {funcionario} não encontrado no departamento {self.nome}.")

    def atribuir_gerente(self, gerente):
        self.gerente = gerente
        print(f"Gerente {gerente} atribuído ao departamento {self.nome}.")

    def iniciar_projeto(self, nome_projeto):
        self.projetos.append({'nome': nome_projeto, 'status': 'em andamento'})
        print(f"Projeto '{nome_projeto}' iniciado no departamento {self.nome}.")

    def concluir_projeto(self, nome_projeto):
        for projeto in self.projetos:
            if projeto['nome'] == nome_projeto and projeto['status'] == 'em andamento':
                projeto['status'] = 'concluído'
                print(f"Projeto '{nome_projeto}' concluído no departamento {self.nome}.")
                return
        print(f"Projeto '{nome_projeto}' não encontrado ou já concluído.")

@app.route('/admin', methods=['GET', 'POST'])
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


class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Sem autoincrement
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

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
    id_funcionario = request.form.get('id_funcionario')  # Obtém o ID do formulário
    
    if id_funcionario:  # Verifica se o ID foi fornecido
        Administracao.remover_funcionario(id_funcionario)
        flash(f"Funcionário com ID {id_funcionario} removido com sucesso!", 'success')
    else:
        flash("ID do funcionário não foi informado.", 'danger')
    
    return redirect(url_for('funcionarios_view'))

@app.route('/funcionarios', methods=['GET', 'POST'])
def funcionarios_view():
    funcionarios = Funcionario.query.all()
    return render_template('administracao.html', funcionarios=funcionarios)

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

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    return render_template('administracao.html')

class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_contrato = db.Column(db.String(50), nullable=False)
    data_inicio = db.Column(db.String(10), nullable=False)
    data_fim = db.Column(db.String(10), nullable=False)
    assinaturas = db.Column(db.String(100), nullable=True)
    status_contrato = db.Column(db.Boolean, default=False)
    descricao_contrato = db.Column(db.Text, nullable=True)

    def _init_(self, numero_contrato, data_inicio, data_fim, descricao_contrato):
        self.numero_contrato = numero_contrato
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.descricao_contrato = descricao_contrato

    def rescindir_contrato(self):
        if self.status_contrato:
            self.status_contrato = False
        else:
            return "O contrato já está rescindido."

    def assinar_contrato(self, assinatura):
        if not self.assinaturas:
            self.assinaturas = assinatura
            self.status_contrato = True
        else:
            return "O contrato já foi assinado."

    def atualizar_contrato(self, nova_descricao):
        self.descricao_contrato = nova_descricao

    def renovar_contrato(self, nova_data_fim):
        data_atual = datetime.strptime(self.data_fim, "%Y-%m-%d")
        nova_data = datetime.strptime(nova_data_fim, "%Y-%m-%d")
        if nova_data > data_atual:
            self.data_fim = nova_data_fim
        else:
            return "A nova data de fim deve ser posterior à data atual."

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
        # Captura os dados do formulário
        nome_do_projeto = request.form.get('nome_do_projeto')
        objetivos = request.form.get('obj_met')
        membros = request.form.get('membros')
        data_termino = request.form.get('dt')

        # Adiciona o projeto ao banco de dados
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

    # Exibe todos os projetos cadastrados
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

@app.route('/pessoas')
def pessoas():
    return render_template('pessoas.html')

@app.route('/employee')
def employee():
    return render_template('funcionarios.html')

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

class EntidadeExterna(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    faturamento = db.Column(db.Float, nullable=False)
    recorrencia = db.Column(db.String(50), nullable=False)

    def __init__(self, razao_social, cnpj, faturamento, recorrencia):
        self.razao_social = razao_social
        self.cnpj = cnpj
        self.faturamento = faturamento
        self.recorrencia = recorrencia

    def editar_entidade(self, nova_razao_social=None, novo_cnpj=None, novo_faturamento=None, nova_recorrencia=None):
        if nova_razao_social:
            self.razao_social = nova_razao_social
        if novo_cnpj:
            self.cnpj = novo_cnpj
        if novo_faturamento is not None:
            self.faturamento = novo_faturamento
        if nova_recorrencia:
            self.recorrencia = nova_recorrencia

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True, host='0.0.0.0', port=5000)