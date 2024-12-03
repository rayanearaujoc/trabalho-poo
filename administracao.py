from funcionario import Funcionario
from extensions import db
import random

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
        
        if Funcionario.query.filter_by(email=email).first():
            print(f"O e-mail '{email}' já está cadastrado.")
            return False  

        funcionario_id = random.randint(1000, 9999)

        funcionario = Funcionario(id=funcionario_id, nome=nome, email=email)
        db.session.add(funcionario)
        db.session.commit()
        print(f"Funcionário {nome} (ID: {funcionario_id}) adicionado com sucesso.")
        return True  
    def remover_funcionario(id_funcionario):
        try:
            funcionario = Funcionario.query.get(int(id_funcionario))  
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