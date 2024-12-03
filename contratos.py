from extensions import db
from datetime import datetime

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