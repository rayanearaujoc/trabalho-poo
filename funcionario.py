from extensions import db

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Sem autoincrement
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
