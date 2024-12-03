from flask import Flask, render_template, request, redirect, url_for, session, flash 

class Pessoas:
    def __init__(self, nome, cpf, cnpj, email, celular, endereco, nascimento, atribuicao):
        self.nome = nome
        self.__cpf = cpf
        self.__cnpj = cnpj
        self.__email = email
        self.__celular = celular
        self.__endereco = endereco
        self.__nascimento = nascimento
        self.atribuicao = atribuicao
        self.cadastro = []

    @property
    def cpf(self):
     return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
     self.__cpf = cpf

    @property
    def cnpj(self):
     return self.__cnpj

    @cnpj.setter
    def cnpj(self, cnpj):
     self.__cnpj = cnpj

    @property
    def email(self):
     return self.__email

    @email.setter
    def email(self, email):
     self.__email = email

    @property
    def celular(self):
     return self.__celular

    @celular.setter
    def celular(self, celular):
     self.__celular = celular

    @property
    def endereco(self):
      return self.__endereco

    @endereco.setter
    def endereco(self, endereco):
      self.__endereco = endereco

    @property
    def nascimento(self):
      return self.__nascimento

    @nascimento.setter
    def nascimento(self, nascimento):
     self.__nascimento = nascimento

    def registrar(self):
        self.cadastro.append({
            "nome": self.nome,
            "cpf": self.__cpf,
            "cnpj": self.__cnpj,
            "email": self.__email,
            "celular": self.__celular,
            "endereco": self.__endereco,
            "nascimento": self.__nascimento,
            "atribuicao": self.atribuicao
        })
        print(f"Pessoa {self.nome} registrada com sucesso!")

class Funcionarios(Pessoas):
    def __init__(self, nome, cpf, cnpj, email, celular, endereco, nascimento, atribuicao, cargo, salario, ocupacao, modelo_de_trabalho):
        super().__init__( nome, cpf, cnpj, email, celular, endereco, nascimento, atribuicao)
        self.cargo = cargo
        self.__salario = salario
        self.ocupacao = ocupacao
        self.__modelo_de_trabalho = modelo_de_trabalho
        self.__funcionarios = []

    @property
    def salario(self):
        return self.__salario

    @salario.setter
    def alterar_salario(self, salario):
        self.__salario = salario

    @property
    def modelo_de_trabalho(self):
        return self.__modelo_de_trabalho

    @modelo_de_trabalho.setter
    def modelo_de_trabalho(self, modelo_de_trabalho):
        self.__modelo_de_trabalho = modelo_de_trabalho

    def admitir_funcionario(self, funcionario):
        if not isinstance(funcionario, Funcionarios):
            raise TypeError("O objeto deve ser uma instância da classe Funcionarios.")
        self.__funcionarios.append(funcionario)
        print(f"Funcionário {funcionario.nome} admitido com sucesso!")
