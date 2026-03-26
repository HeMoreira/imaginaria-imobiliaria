from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DecimalField, IntegerField, PasswordField, SubmitField, validators
from models import Status, TipoDeProduto

class AdminForm(FlaskForm):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.Length(min=4, max=25), 
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=4, max=30),
        validators.EqualTo('password2', message='Passwords must match'),
    ])
    password2 = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.Length(min=4, max=30),
    ])
    submit = SubmitField("Confirmar")

class ImovelForm(FlaskForm):
    nome = StringField('Nome do Imóvel', [validators.DataRequired(), validators.Length(min=5, max=50)])
    descricao = TextAreaField('Descrição do Imóvel', [validators.DataRequired(), validators.Length(min=1, max=500)], render_kw={"rows":5})
    tipo_de_produto = SelectField('Tipo de Produto', choices=[("", "Selecione o Tipo do Imóvel")] + [(tipo.name, tipo.value) for tipo in TipoDeProduto], validators=[validators.DataRequired()])
    status = SelectField('Status', choices=[("", "Selecione o Status do Imóvel")] + [(status.name, status.value) for status in Status], validators=[validators.DataRequired()])
    esta_visivel = BooleanField('O produto deve ser visível para o usuário?', default=True)
    preco_compra = DecimalField('Preço de Compra', [validators.Optional()], places=2)
    preco_aluguel = DecimalField('Preço de Aluguel', [validators.Optional()], places=2)
    condominio = DecimalField('Condomínio', [validators.Optional()], places=2)
    iptu = DecimalField('IPTU', [validators.Optional()], places=2)
    menor_area_em_metros_quadrados = IntegerField('Menor Área (m²)', [
        validators.DataRequired(),
    ])
    maior_area_em_metros_quadrados = IntegerField('Maior Área (m²)', [
        validators.DataRequired(),
    ])
    menor_quantidade_de_dormitorios = IntegerField('Menor Quantidade de Dormitórios', [
        validators.DataRequired(),
    ])
    maior_quantidade_de_dormitorios = IntegerField('Maior Quantidade de Dormitórios', [
        validators.DataRequired(),
    ])
    cidade = StringField('Cidade', [validators.DataRequired(), validators.Length(max=100)])
    bairro = StringField('Bairro', [validators.DataRequired(), validators.Length(max=100)])
    endereco = StringField('Endereço', [validators.DataRequired(), validators.Length(max=255)])
    cep = StringField('CEP', [validators.DataRequired(), validators.Length(max=10)])

    caminho_da_imagem_principal = FileField('Imagem Principal', [FileRequired()])
    caminho_da_imagem_de_fachada1 = FileField('Imagem de Fachada 1', [FileRequired()])
    caminho_da_imagem_de_fachada2 = FileField('Imagem de Fachada 2', [FileRequired()])

    caminho_da_imagem_de_area_comum1 = FileField('Área Comum de Destaque 1 (opcional)')
    descricao_da_area_comum1 = StringField('Descrição da Área Comum 1')
    caminho_da_imagem_de_area_comum2 = FileField('Área Comum de Destaque 2 (opcional)')
    descricao_da_area_comum2 = StringField('Descrição da Área Comum 2')
    caminho_da_imagem_de_area_comum3 = FileField('Área Comum de Destaque 3 (opcional)')
    descricao_da_area_comum3 = StringField('Descrição da Área Comum 3')
    caminho_da_imagem_de_area_comum4 = FileField('Área Comum de Destaque 4 (opcional)')
    descricao_da_area_comum4 = StringField('Descrição da Área Comum 4')
    caminho_da_imagem_de_area_comum5 = FileField('Área Comum de Destaque 5 (opcional)')
    descricao_da_area_comum5 = StringField('Descrição da Área Comum 5')
    caminho_da_imagem_de_area_comum6 = FileField('Área Comum de Destaque 6 (opcional)')
    descricao_da_area_comum6 = StringField('Descrição da Área Comum 6')
    caminho_da_imagem_de_area_comum7 = FileField('Área Comum de Destaque 7 (opcional)')
    descricao_da_area_comum7 = StringField('Descrição da Área Comum 7')
    caminho_da_imagem_de_area_comum8 = FileField('Área Comum de Destaque 8 (opcional)')
    descricao_da_area_comum8 = StringField('Descrição da Área Comum 8')
    caminho_da_imagem_de_area_comum9 = FileField('Área Comum de Destaque 9 (opcional)')
    descricao_da_area_comum9 = StringField('Descrição da Área Comum 9')
    caminho_da_imagem_de_area_comum10 = FileField('Área Comum de Destaque 10 (opcional)')
    descricao_da_area_comum10 = StringField('Descrição da Área Comum 10')

    caminho_da_imagem_da_planta1 = FileField('Planta baixa do imóvel ou área comum 1 (opcional)')
    descricao_da_planta1 = StringField('Descrição da Planta 1')
    caminho_da_imagem_da_planta2 = FileField('Planta baixa do imóvel ou área comum 2 (opcional)')
    descricao_da_planta2 = StringField('Descrição da Planta 2')
    caminho_da_imagem_da_planta3 = FileField('Planta baixa do imóvel ou área comum 3 (opcional)')
    descricao_da_planta3 = StringField('Descrição da Planta 3')
    caminho_da_imagem_da_planta4 = FileField('Planta baixa do imóvel ou área comum 4 (opcional)')
    descricao_da_planta4 = StringField('Descrição da Planta 4')
    caminho_da_imagem_da_planta5 = FileField('Planta baixa do imóvel ou área comum 5 (opcional)')
    descricao_da_planta5 = StringField('Descrição da Planta 5')
    caminho_da_imagem_da_planta6 = FileField('Planta baixa do imóvel ou área comum 6 (opcional)')
    descricao_da_planta6 = StringField('Descrição da Planta 6')
    caminho_da_imagem_da_planta7 = FileField('Planta baixa do imóvel ou área comum 7 (opcional)')
    descricao_da_planta7 = StringField('Descrição da Planta 7')
    caminho_da_imagem_da_planta8 = FileField('Planta baixa do imóvel ou área comum 8 (opcional)')
    descricao_da_planta8 = StringField('Descrição da Planta 8')
    caminho_da_imagem_da_planta9 = FileField('Planta baixa do imóvel ou área comum 9 (opcional)')
    descricao_da_planta9 = StringField('Descrição da Planta 9')
    caminho_da_imagem_da_planta10 = FileField('Planta baixa do imóvel ou área comum 10 (opcional)')
    descricao_da_planta10 = StringField('Descrição da Planta 10')

    submit = SubmitField("Adicionar imóvel")