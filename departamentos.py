from extensions import db

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


class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_do_projeto = db.Column(db.String(100), nullable=False)
    objetivos = db.Column(db.String(200), nullable=False)
    membros = db.Column(db.String(200), nullable=False)
    data_termino = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Projeto {self.nome_do_projeto}>"
