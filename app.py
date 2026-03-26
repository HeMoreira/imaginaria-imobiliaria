from flask import Flask, render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import LoginManager, login_required, login_user, current_user
from flask_talisman import Talisman
from models import db
from models import Imovel, ImagensImovel, PlantasImovel, Admin
from utils import obter_tentativas_de_login, salvar_imagens, esta_bloqueado, aumentar_contador_de_tentativas_de_login, zerar_contador_de_tentativas_de_login
from logging_utils import init_app_logging
from forms import AdminForm, ImovelForm
from werkzeug.datastructures import CombinedMultiDict
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config


app = Flask(__name__)
init_app_logging(app)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)
talisman = Talisman(app, content_security_policy=Config.CSP_CONFIG)

db.init_app(app)

@login_manager.user_loader
def load_user(admin_id):
    return db.session.get(Admin, int(admin_id))

@login_manager.unauthorized_handler
def unauthorized():
    app.logger.warning('= tentativa de acessar painel de admin sem login =')
    return abort(404)
limiter = Limiter(get_remote_address, app=app)

@app.before_request
def enforce_login_globally():
    public_endpoints = ['login', 'index', 'static']
    if request.endpoint not in public_endpoints and not current_user.is_authenticated:
        return abort(404)

# TODO: implementar ProxyFix antes de colocar em produção
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)



@app.route("/", methods=['GET'])
def index():
    imoveis = Imovel.query.all()
    return render_template('index.html', imoveis=imoveis)

@app.route("/11_login_k", methods=['POST', 'GET'])
def login():
    ip = get_remote_address()
    if esta_bloqueado(ip):
        app.logger.warning('^ Ip foi bloqueado por 15 minutos após múltiplas tentativas de login')
        return abort(404)
    form = AdminForm(request.form)
    if request.method == 'POST':
        if form.validate():
            admin = Admin.query.filter_by(username=form.username.data).first()
            if admin and admin.check_password(form.password.data):
                login_user(admin)
                zerar_contador_de_tentativas_de_login(ip)
                app.logger.info('\n ^ login bem sucedido')
                flash("Logado com sucesso!", "success")
                return redirect(url_for('admin'))
        app.logger.warning('^ login mal sucedido')
        aumentar_contador_de_tentativas_de_login(ip)
        flash(f"Senha ou usuário incorretos. {3-obter_tentativas_de_login(ip)} tentativas restantes", "warning")
        return redirect(url_for('login'))
    else:
        app.logger.info('^ página de login foi acessada')
        return render_template('login.html', form=form)

@app.route("/11_damin_k", methods=['POST', 'GET'])
def admin():
    form = ImovelForm(CombinedMultiDict((request.form, request.files)))
    if request.method == 'POST' and form.validate():
        lista_de_imagens = [
            form.caminho_da_imagem_principal.data,
            form.caminho_da_imagem_de_fachada1.data,
            form.caminho_da_imagem_de_fachada2.data,
            form.caminho_da_imagem_de_area_comum1.data,
            form.caminho_da_imagem_de_area_comum2.data,
            form.caminho_da_imagem_de_area_comum3.data,
            form.caminho_da_imagem_de_area_comum4.data,
            form.caminho_da_imagem_de_area_comum5.data,
            form.caminho_da_imagem_de_area_comum6.data,
            form.caminho_da_imagem_de_area_comum7.data,
            form.caminho_da_imagem_de_area_comum8.data,
            form.caminho_da_imagem_de_area_comum9.data,
            form.caminho_da_imagem_de_area_comum10.data,
        ]
        lista_de_plantas = [
            form.caminho_da_imagem_da_planta1.data,
            form.caminho_da_imagem_da_planta2.data,
            form.caminho_da_imagem_da_planta3.data,
            form.caminho_da_imagem_da_planta4.data,
            form.caminho_da_imagem_da_planta5.data,
            form.caminho_da_imagem_da_planta6.data,
            form.caminho_da_imagem_da_planta7.data,
            form.caminho_da_imagem_da_planta8.data,
            form.caminho_da_imagem_da_planta9.data,
            form.caminho_da_imagem_da_planta10.data,
        ]
        lista_de_caminhos_das_imagens = salvar_imagens(lista_de_imagens)
        lista_de_caminhos_das_plantas = salvar_imagens(lista_de_plantas)

        imagens_novo_imovel = ImagensImovel(
            caminho_da_imagem_principal=lista_de_caminhos_das_imagens[0],
            caminho_da_imagem_de_fachada1=lista_de_caminhos_das_imagens[1],
            caminho_da_imagem_de_fachada2=lista_de_caminhos_das_imagens[2],
            caminho_da_imagem_de_area_comum1=lista_de_caminhos_das_imagens[3],
            descricao_da_area_comum1=form.descricao_da_area_comum1.data,
            caminho_da_imagem_de_area_comum2=lista_de_caminhos_das_imagens[4],
            descricao_da_area_comum2=form.descricao_da_area_comum2.data,
            caminho_da_imagem_de_area_comum3=lista_de_caminhos_das_imagens[5],
            descricao_da_area_comum3=form.descricao_da_area_comum3.data,
            caminho_da_imagem_de_area_comum4=lista_de_caminhos_das_imagens[6],
            descricao_da_area_comum4=form.descricao_da_area_comum4.data,
            caminho_da_imagem_de_area_comum5=lista_de_caminhos_das_imagens[7],
            descricao_da_area_comum5=form.descricao_da_area_comum5.data,
            caminho_da_imagem_de_area_comum6=lista_de_caminhos_das_imagens[8],
            descricao_da_area_comum6=form.descricao_da_area_comum6.data,
            caminho_da_imagem_de_area_comum7=lista_de_caminhos_das_imagens[9],
            descricao_da_area_comum7=form.descricao_da_area_comum7.data,
            caminho_da_imagem_de_area_comum8=lista_de_caminhos_das_imagens[10],
            descricao_da_area_comum8=form.descricao_da_area_comum8.data,
            caminho_da_imagem_de_area_comum9=lista_de_caminhos_das_imagens[11],
            descricao_da_area_comum9=form.descricao_da_area_comum9.data,
            caminho_da_imagem_de_area_comum10=lista_de_caminhos_das_imagens[12],
            descricao_da_area_comum10=form.descricao_da_area_comum10.data
        )
        plantas_novo_imovel = PlantasImovel(
            caminho_da_imagem_da_planta1=lista_de_caminhos_das_plantas[0],
            descricao_da_planta1=form.descricao_da_planta1.data,
            caminho_da_imagem_da_planta2=lista_de_caminhos_das_plantas[1],
            descricao_da_planta2=form.descricao_da_planta2.data,
            caminho_da_imagem_da_planta3=lista_de_caminhos_das_plantas[2],
            descricao_da_planta3=form.descricao_da_planta3.data,
            caminho_da_imagem_da_planta4=lista_de_caminhos_das_plantas[3],
            descricao_da_planta4=form.descricao_da_planta4.data,
            caminho_da_imagem_da_planta5=lista_de_caminhos_das_plantas[4],
            descricao_da_planta5=form.descricao_da_planta5.data,
            caminho_da_imagem_da_planta6=lista_de_caminhos_das_plantas[5],
            descricao_da_planta6=form.descricao_da_planta6.data,
            caminho_da_imagem_da_planta7=lista_de_caminhos_das_plantas[6],
            descricao_da_planta7=form.descricao_da_planta7.data,
            caminho_da_imagem_da_planta8=lista_de_caminhos_das_plantas[7],
            descricao_da_planta8=form.descricao_da_planta8.data,
            caminho_da_imagem_da_planta9=lista_de_caminhos_das_plantas[8],
            descricao_da_planta9=form.descricao_da_planta9.data,
            caminho_da_imagem_da_planta10=lista_de_caminhos_das_plantas[9],
            descricao_da_planta10=form.descricao_da_planta10.data
        )
        novo_imovel = Imovel(
            nome=form.nome.data,
            descricao=form.descricao.data,
            tipo_de_produto=form.tipo_de_produto.data,
            status=form.status.data,
            esta_visivel=form.esta_visivel.data,
            preco_compra=form.preco_compra.data,
            preco_aluguel=form.preco_aluguel.data,
            condominio=form.condominio.data,
            iptu=form.iptu.data,
            menor_area_em_metros_quadrados=form.menor_area_em_metros_quadrados.data,
            maior_area_em_metros_quadrados=form.maior_area_em_metros_quadrados.data,
            menor_quantidade_de_dormitorios=form.menor_quantidade_de_dormitorios.data,
            maior_quantidade_de_dormitorios=form.maior_quantidade_de_dormitorios.data,
            cidade=form.cidade.data,
            bairro=form.bairro.data,
            endereco=form.endereco.data,
            cep=form.cep.data,
        )
        novo_imovel.imagens_do_produto.append(imagens_novo_imovel)
        novo_imovel.plantas_do_produto.append(plantas_novo_imovel)
        try:
            db.session.add(novo_imovel)
            db.session.commit()
            app.logger.info('^ adição de imóvel bem sucedida')
            flash("Imóvel adicionado com sucesso!", "success")
            imoveis = Imovel.query.all()
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            app.logger.info('^ adição de imóvel mal sucedido')
            flash("O Imóvel não foi adicionado! Verifique e corrija os campos com informações inválidas", "error")
            imoveis = Imovel.query.all()
            return render_template('admin.html', mensagem="Erro ao adicionar imóvel", imoveis=imoveis, form=form)
    else:
        app.logger.info('^ painel de admin foi acessado')
        print(f"Erros de validação: {form.errors}")
        flash("O formulário não foi preenchido corretamente... Verifique e corrija os campos com informações inválidas", "error")
        imoveis = Imovel.query.all()
        return render_template('admin.html', imoveis=imoveis, form=form)

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
