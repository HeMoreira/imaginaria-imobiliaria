from flask import Flask, render_template, request
from models import db
from models import Imovel, ImagensImovel, PlantasImovel
from utils import salvar_imagens, salvar_instancias_no_banco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imaginariaimobiliaria.db'
db.init_app(app)

@app.route("/", methods=['GET'])
def index():
    imoveis = Imovel.query.all()
    return render_template('index.html', imoveis=imoveis)

@app.route("/admin", methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':

        lista_de_imagens = [
            request.form.get('caminho_da_imagem_principal'),
            request.form.get('caminho_da_imagem_de_fachada1'),
            request.form.get('caminho_da_imagem_de_fachada2'),
            request.form.get('caminho_da_imagem_de_area_comum1'),
            request.form.get('caminho_da_imagem_de_area_comum2'),
            request.form.get('caminho_da_imagem_de_area_comum3'),
            request.form.get('caminho_da_imagem_de_area_comum4'),
            request.form.get('caminho_da_imagem_de_area_comum5'),
            request.form.get('caminho_da_imagem_de_area_comum6'),
            request.form.get('caminho_da_imagem_de_area_comum7'),
            request.form.get('caminho_da_imagem_de_area_comum8'),
            request.form.get('caminho_da_imagem_de_area_comum9'),
            request.form.get('caminho_da_imagem_de_area_comum10'),
        ]
        lista_de_plantas = [
            request.form.get('caminho_da_imagem_da_planta1'),
            request.form.get('caminho_da_imagem_da_planta2'),
            request.form.get('caminho_da_imagem_da_planta3'),
            request.form.get('caminho_da_imagem_da_planta4'),
            request.form.get('caminho_da_imagem_da_planta5'),
            request.form.get('caminho_da_imagem_da_planta6'),
            request.form.get('caminho_da_imagem_da_planta7'),
            request.form.get('caminho_da_imagem_da_planta8'),
            request.form.get('caminho_da_imagem_da_planta9'),
            request.form.get('caminho_da_imagem_da_planta10')
        ]
        lista_de_caminhos_das_imagens = salvar_imagens('static/imagens', lista_de_imagens)
        lista_de_caminhos_das_plantas = salvar_imagens('static/plantas', lista_de_plantas)

        imagens_novo_imovel = ImagensImovel(
            caminho_da_imagem_principal=lista_de_caminhos_das_imagens[0],
            caminho_da_imagem_de_fachada1=lista_de_caminhos_das_imagens[1],
            caminho_da_imagem_de_fachada2=lista_de_caminhos_das_imagens[2],
            caminho_da_imagem_de_area_comum1=lista_de_caminhos_das_imagens[3],
            descricao_da_area_comum1=request.form.get('descricao_da_area_comum1'),
            caminho_da_imagem_de_area_comum2=lista_de_caminhos_das_imagens[4],
            descricao_da_area_comum2=request.form.get('descricao_da_area_comum2'),
            caminho_da_imagem_de_area_comum3=lista_de_caminhos_das_imagens[5],
            descricao_da_area_comum3=request.form.get('descricao_da_area_comum3'),
            caminho_da_imagem_de_area_comum4=lista_de_caminhos_das_imagens[6],
            descricao_da_area_comum4=request.form.get('descricao_da_area_comum4'),
            caminho_da_imagem_de_area_comum5=lista_de_caminhos_das_imagens[7],
            descricao_da_area_comum5=request.form.get('descricao_da_area_comum5'),
            caminho_da_imagem_de_area_comum6=lista_de_caminhos_das_imagens[8],
            descricao_da_area_comum6=request.form.get('descricao_da_area_comum6'),
            caminho_da_imagem_de_area_comum7=lista_de_caminhos_das_imagens[9],
            descricao_da_area_comum7=request.form.get('descricao_da_area_comum7'),
            caminho_da_imagem_de_area_comum8=lista_de_caminhos_das_imagens[10],
            descricao_da_area_comum8=request.form.get('descricao_da_area_comum8'),
            caminho_da_imagem_de_area_comum9=lista_de_caminhos_das_imagens[11],
            descricao_da_area_comum9=request.form.get('descricao_da_area_comum9'),
            caminho_da_imagem_de_area_comum10=lista_de_caminhos_das_imagens[12],
            descricao_da_area_comum10=request.form.get('descricao_da_area_comum10')
        )
        plantas_novo_imovel = PlantasImovel(
            caminho_da_imagem_da_planta1=lista_de_caminhos_das_plantas[0],
            descricao_da_planta1=request.form.get('descricao_da_planta1'),
            caminho_da_imagem_da_planta2=lista_de_caminhos_das_plantas[1],
            descricao_da_planta2=request.form.get('descricao_da_planta2'),
            caminho_da_imagem_da_planta3=lista_de_caminhos_das_plantas[2],
            descricao_da_planta3=request.form.get('descricao_da_planta3'),
            caminho_da_imagem_da_planta4=lista_de_caminhos_das_plantas[3],
            descricao_da_planta4=request.form.get('descricao_da_planta4'),
            caminho_da_imagem_da_planta5=lista_de_caminhos_das_plantas[4],
            descricao_da_planta5=request.form.get('descricao_da_planta5'),
            caminho_da_imagem_da_planta6=lista_de_caminhos_das_plantas[5],
            descricao_da_planta6=request.form.get('descricao_da_planta6'),
            caminho_da_imagem_da_planta7=lista_de_caminhos_das_plantas[6],
            descricao_da_planta7=request.form.get('descricao_da_planta7'),
            caminho_da_imagem_da_planta8=lista_de_caminhos_das_plantas[7],
            descricao_da_planta8=request.form.get('descricao_da_planta8'),
            caminho_da_imagem_da_planta9=lista_de_caminhos_das_plantas[8],
            descricao_da_planta9=request.form.get('descricao_da_planta9'),
            caminho_da_imagem_da_planta10=lista_de_caminhos_das_plantas[9],
            descricao_da_planta10=request.form.get('descricao_da_planta10')
        )
        novo_imovel = Imovel(
            nome=request.form.get('nome'),
            descricao=request.form.get('descricao'),
            tipo_de_produto=request.form.get('tipo_de_produto'),
            status=request.form.get('status'),
            esta_visivel=bool(request.form.get('esta_visivel')),
            preco_compra=float(request.form.get('preco_compra') or 0),
            preco_aluguel=float(request.form.get('preco_aluguel') or 0),
            condominio=float(request.form.get('condominio') or 0),
            iptu=float(request.form.get('iptu') or 0),
            menor_area_em_metros_quadrados=float(request.form.get('menor_area_em_metros_quadrados') or 0),
            maior_area_em_metros_quadrados=float(request.form.get('maior_area_em_metros_quadrados') or 0),
            menor_quantidade_de_dormitorios=int(request.form.get('menor_quantidade_de_dormitorios') or 0),
            maior_quantidade_de_dormitorios=int(request.form.get('maior_quantidade_de_dormitorios') or 0),
            cidade=request.form.get('cidade'),
            bairro=request.form.get('bairro'),
            endereco=request.form.get('endereco'),
            cep=request.form.get('cep'),
        )
        novo_imovel.imagens_do_produto.append(imagens_novo_imovel)
        novo_imovel.plantas_do_produto.append(plantas_novo_imovel)
        print(db.Model.metadata.tables.keys())
        try:
            print(f"Sucesso ao adicionar imóvel")
            db.session.add(novo_imovel)
            db.session.commit()
            return render_template('admin.html', mensagem="Imóvel adicionado com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar imóvel: {str(e)}")
            db.session.rollback()
            return render_template('admin.html', mensagem=f"Erro ao adicionar imóvel: {str(e)}")
    else:
        imoveis = Imovel.query.all()
        return render_template('admin.html', imoveis=imoveis)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
