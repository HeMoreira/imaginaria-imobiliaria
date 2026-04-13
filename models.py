from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from slugify import slugify

db = SQLAlchemy()

class Status(Enum):
    ENTREGUE = "ENTREGUE"
    DISPONIVEL = "DISPONÍVEL"
    LANCAMENTO = "LANÇAMENTO"
    FUTURO_LANCAMENTO = "FUTURO LANÇAMENTO"
    EM_CONSTRUCAO = "EM CONSTRUÇÃO"

class TipoDeProduto(Enum):
    APARTAMENTO = "APARTAMENTO"
    CASA = "CASA"
    TERRENO = "TERRENO"

class Imovel(db.Model):
    __tablename__ = 'imoveis'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=True)
    descricao = db.Column(db.String(500), nullable=False)
    tipo_de_produto = db.Column(db.Enum(TipoDeProduto), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)
    esta_visivel = db.Column(db.Boolean, default=True)
    esta_em_destaque = db.Column(db.Boolean, default=False)

    preco_compra = db.Column(db.Numeric(15, 2), nullable=True)
    preco_aluguel = db.Column(db.Numeric(12, 2), nullable=True)
    condominio = db.Column(db.Numeric(12, 2), default=0.0, nullable=True)
    iptu = db.Column(db.Numeric(12, 2), default=0.0, nullable=True)

    menor_area_em_metros_quadrados = db.Column(db.SmallInteger, nullable=False)
    maior_area_em_metros_quadrados = db.Column(db.SmallInteger, nullable=False)
    menor_quantidade_de_dormitorios = db.Column(db.SmallInteger , nullable=False)
    maior_quantidade_de_dormitorios = db.Column(db.SmallInteger, nullable=False)

    cidade = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    metros_ate_o_metro_mais_proximo = db.Column(db.Integer, default=10000)

    imagens_principais_do_produto = db.relationship('ImagensImovel', backref="imovel", lazy=True, cascade="all, delete-orphan")
    imagens_do_produto = db.relationship('ImagemComDescricao', back_populates='imovel_rel_imagem', lazy=True, cascade="all, delete-orphan")
    plantas_do_produto = db.relationship('PlantaComDescricao', back_populates='imovel_rel_planta', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Imóvel(nome='{self.nome}', status='{self.status}')"
    
    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('nome', ''))
        super().__init__(*args, **kwargs)

class ImagensImovel(db.Model):
    __tablename__ = 'imagens_imovel'
    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imoveis.id'), nullable=False)
    caminho_da_imagem_principal = db.Column(db.String(255), nullable=False)
    caminho_da_imagem_de_fachada1 = db.Column(db.String(255), nullable=False)
    caminho_da_imagem_de_fachada2 = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"id: {self.id} - id_imovel: {self.imovel_id}"
    
class ImagemComDescricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imoveis.id'), nullable=False)
    imovel_rel_imagem = db.relationship('Imovel', back_populates='imagens_do_produto')
    caminho = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(50))

class PlantaComDescricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imoveis.id'), nullable=False)
    imovel_rel_planta = db.relationship('Imovel', back_populates='plantas_do_produto')
    caminho = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(50))

class Admin(db.Model, UserMixin):
    __tablename__ = 'administradores'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.id}_{self.username}"
    
