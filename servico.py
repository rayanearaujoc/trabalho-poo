from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consultor_disponivel = db.Column(db.Boolean, nullable=False)
    nome_solucao = db.Column(db.String(100), nullable=False)
    descricao_solucao = db.Column(db.String(200), nullable=False)
    data = db.Column(db.String(10), nullable=False)  
    horario = db.Column(db.String(5), nullable=False)  

    def agendar_servico(self) -> bool:
        if self.verificar_disponibilidade():
            db.session.add(self)  
            db.session.commit()  
            return True
        return False

    def verificar_disponibilidade(self) -> bool:
        return self.consultor_disponivel

    @staticmethod
    def horario_disponivel(horario: str) -> bool:
        try:
            hora = int(horario.split(':')[0])
            return 14 <= hora < 18  
        except ValueError:
            return False  
