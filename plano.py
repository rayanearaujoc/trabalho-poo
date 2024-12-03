from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Planos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)  # Referência ao serviço
    plano_atual = db.Column(db.String(100), nullable=False)
    preco_plano = db.Column(db.Float, nullable=False)
    desconto = db.Column(db.Float, default=0.0)

    servico = db.relationship('Servico', backref=db.backref('planos', lazy=True))

    def __init__(self, servico_id: int, plano_atual: str, preco_plano: float, desconto: float = 0.0):
        self.servico_id = servico_id 
        self.plano_atual = plano_atual
        self.preco_plano = preco_plano
        self.desconto = desconto

    def mudar_plano(self, novo_plano: str, novo_preco: float) -> None:
        self.plano_atual = novo_plano
        self.preco_plano = novo_preco
        print(f"Plano alterado para {novo_plano}. Novo preço: R${novo_preco:.2f}")

    def calcular_preco_final(self) -> float:
        desconto_percentual = self.desconto / 100  
        preco_final = self.preco_plano * (1 - desconto_percentual)
        return preco_final