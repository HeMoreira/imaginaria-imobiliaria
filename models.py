from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Status(Enum):
    ENTREGUE = "ENTREGUE"
    DISPONIVEL = "DISPONIVEL"
    LANCAMENTO = "LANCAMENTO"
    FUTURO_LANCAMENTO = "FUTURO_LANCAMENTO"
    EM_CONSTRUCAO = "EM_CONSTRUCAO"

class TipoDeProduto(Enum):
    APARTAMENTO = "APARTAMENTO"
    CASA = "CASA"
    TERRENO = "TERRENO"

class Imovel(db.Model):
    __tablename__ = 'imoveis'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    tipo_de_produto = db.Column(db.Enum(TipoDeProduto), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)
    esta_visivel = db.Column(db.Boolean, default=True)

    preco_compra = db.Column(db.Numeric(15, 2), nullable=True)
    preco_aluguel = db.Column(db.Numeric(12, 2), nullable=True)
    condominio = db.Column(db.Numeric(12, 2), default=0.0, nullable=True)
    iptu = db.Column(db.Numeric(12, 2), default=0.0, nullable=True)

    menor_area_em_metros_quadrados = db.Column(db.SmallInteger, nullable=False)
    maior_area_em_metros_quadrados = db.Column(db.SmallInteger, nullable=False)
    menor_quantidade_de_dormitorios = db.Column(db.SmallInteger, default=0)
    maior_quantidade_de_dormitorios = db.Column(db.SmallInteger, default=0)

    cidade = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(10), nullable=False)

    imagens_do_produto = db.relationship('ImagensImovel', backref="imovel", lazy=True, cascade="all, delete-orphan")
    plantas_do_produto = db.relationship('PlantasImovel', backref="imovel", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Imóvel(nome='{self.nome}', status='{self.status}')"

class ImagensImovel(db.Model):
    __tablename__ = 'imagens_imovel'
    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imoveis.id'), nullable=False)
    caminho_da_imagem_principal = db.Column(db.String(100), nullable=False)
    caminho_da_imagem_de_fachada1 = db.Column(db.String(100), nullable=False)
    caminho_da_imagem_de_fachada2 = db.Column(db.String(100), nullable=False)
    caminho_da_imagem_de_area_comum1 = db.Column(db.String(100), nullable=True)
    descricao_da_area_comum1 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_de_area_comum2 = db.Column(db.String(100), nullable=True)
    descricao_da_area_comum2 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_de_area_comum3 = db.Column(db.String(100), nullable=True)
    descricao_da_area_comum3 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_de_area_comum4 = db.Column(db.String(100), nullable=True)
    descricao_da_area_comum4 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_de_area_comum5 = db.Column(db.String(100), nullable=True)
    descricao_da_area_comum5 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_de_area_comum6 = db.Column(db.String(100), nullable=True)
    descricao_da_area_comum6 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_de_area_comum7 = db.Column(db.String(100), nullable=True)
    descricao_da_area_comum7 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_de_area_comum8 = db.Column(db.String(100), nullable=True)
    descricao_da_area_comum8 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_de_area_comum9 = db.Column(db.String(100), nullable=True)
    descricao_da_area_comum9 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_de_area_comum10 = db.Column(db.String(100), nullable=True)
    descricao_da_area_comum10 = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"id: {self.id} - id_imovel: {self.imovel_id}"

class PlantasImovel(db.Model):
    __tablename__ = 'plantas_imovel'
    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imoveis.id'), nullable=False)
    caminho_da_imagem_da_planta1 = db.Column(db.String(100), nullable=True)
    descricao_da_planta1 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_da_planta2 = db.Column(db.String(100), nullable=True)
    descricao_da_planta2 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_da_planta3 = db.Column(db.String(100), nullable=True)
    descricao_da_planta3 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_da_planta4 = db.Column(db.String(100), nullable=True)
    descricao_da_planta4 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_da_planta5 = db.Column(db.String(100), nullable=True)
    descricao_da_planta5 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_da_planta6 = db.Column(db.String(100), nullable=True)
    descricao_da_planta6 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_da_planta7 = db.Column(db.String(100), nullable=True)
    descricao_da_planta7 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_da_planta8 = db.Column(db.String(100), nullable=True)
    descricao_da_planta8 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_da_planta9 = db.Column(db.String(100), nullable=True)
    descricao_da_planta9 = db.Column(db.String(500), nullable=True)
    caminho_da_imagem_da_planta10 = db.Column(db.String(100), nullable=True)
    descricao_da_planta10 = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"id: {self.id} - id_imovel: {self.imovel_id}"