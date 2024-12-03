from extensions import db

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