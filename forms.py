from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DecimalField, IntegerField, FieldList, FormField, PasswordField, SubmitField, validators
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

class ImagemComContexto(FlaskForm):
    imagem = FileField('Imagem Adicional', [
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens (.jpg, .png, .jpeg)')
    ])
    descricao = StringField('Descrição Curta', [validators.Length(max=50)])
class PlantaComContexto(FlaskForm):
    imagem = FileField('Planta Baixa', [
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens (.jpg, .png, .jpeg)')
    ])
    descricao = StringField('Descrição Curta', [validators.Length(max=50)])

class ImovelForm(FlaskForm):
    nome = StringField('Nome do Imóvel', [validators.DataRequired(), validators.Length(min=5, max=50)])
    descricao = TextAreaField('Descrição do Imóvel', [validators.DataRequired(), validators.Length(min=1, max=500)], render_kw={"rows":5})
    tipo_de_produto = SelectField('Tipo de Produto', choices=[("", "Selecione o Tipo do Imóvel")] + [(tipo.name, tipo.value) for tipo in TipoDeProduto], validators=[validators.DataRequired()])
    status = SelectField('Status', choices=[("", "Selecione o Status do Imóvel")] + [(status.name, status.value) for status in Status], validators=[validators.DataRequired()])
    esta_visivel = BooleanField('O produto deve ser visível para o usuário?', default=True)
    esta_em_destaque = BooleanField('Deseja classificar o produto como destaque?', default=False)
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

    lista_de_caminhos_de_imagens_adicionais = FieldList(FormField(ImagemComContexto), min_entries=50)
    lista_de_caminhos_de_imagens_de_plantas = FieldList(FormField(PlantaComContexto), min_entries=50)

    submit = SubmitField("Adicionar imóvel")