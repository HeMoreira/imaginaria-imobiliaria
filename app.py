from flask import Flask, render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import LoginManager, login_required, login_user, current_user
from flask_talisman import Talisman
from models import db
from models import Imovel, ImagensImovel, ImagemComDescricao, PlantaComDescricao, Admin
from utils import obter_tentativas_de_login, salvar_imagens, esta_bloqueado, aumentar_contador_de_tentativas_de_login, zerar_contador_de_tentativas_de_login
from flask_migrate import Migrate
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

migrate = Migrate(app, db)
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
    public_endpoints = ['login', 'index', 'mostrar_imovel', 'static']
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

@app.route("/imoveis/<slug_imovel>", methods=['GET'])
def mostrar_imovel(slug_imovel):
    imovel = Imovel.query.filter_by(slug=slug_imovel).first_or_404()
    return render_template('info_imovel.html', imovel=imovel)

@app.route("/11_damin_k", methods=['POST', 'GET'])
def admin():
    form = ImovelForm(CombinedMultiDict((request.form, request.files)))
    if request.method == 'POST':
        if form.validate():
            lista_de_imagens_principais = [
                form.caminho_da_imagem_principal.data,
                form.caminho_da_imagem_de_fachada1.data,
                form.caminho_da_imagem_de_fachada2.data,
            ]
            lista_de_imagens = []
            lista_de_plantas = []
            for item in form.lista_de_caminhos_de_imagens_adicionais:
                if item.imagem.data != None:
                    lista_de_imagens.append(item.imagem.data)
            for item in form.lista_de_caminhos_de_imagens_de_plantas:
                if item.imagem.data != None:
                    lista_de_plantas.append(item.imagem.data)
            lista_de_caminhos_das_imagens_principais = salvar_imagens(lista_de_imagens_principais)
            lista_de_caminhos_das_imagens = salvar_imagens(lista_de_imagens)
            lista_de_caminhos_das_plantas = salvar_imagens(lista_de_plantas)

            imagens_principais_novo_imovel = ImagensImovel(
                caminho_da_imagem_principal=lista_de_caminhos_das_imagens_principais[0],
                caminho_da_imagem_de_fachada1=lista_de_caminhos_das_imagens_principais[1],
                caminho_da_imagem_de_fachada2=lista_de_caminhos_das_imagens_principais[2],
            )
            novo_imovel = Imovel(
                nome=form.nome.data,
                descricao=form.descricao.data,
                tipo_de_produto=form.tipo_de_produto.data,
                status=form.status.data,
                esta_visivel=form.esta_visivel.data,
                esta_em_destaque = form.esta_em_destaque.data,
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
            novo_imovel.imagens_principais_do_produto.append(imagens_principais_novo_imovel)
            db.session.add(novo_imovel)
            db.session.flush()
            index_caminho_imagem = 0
            for item in form.lista_de_caminhos_de_imagens_adicionais:
                if item.imagem.data != None:
                    nova_img = ImagemComDescricao(
                        caminho=lista_de_caminhos_das_imagens[index_caminho_imagem],
                        descricao=item.descricao.data,
                        imovel_id=novo_imovel.id,
                    )
                    db.session.add(nova_img)
                    index_caminho_imagem+=1
            index_caminho_imagem = 0
            for item in form.lista_de_caminhos_de_imagens_de_plantas:
                if item.imagem.data != None:
                    nova_img = PlantaComDescricao(
                        caminho=lista_de_caminhos_das_plantas[index_caminho_imagem],
                        descricao=item.descricao.data,
                        imovel_id=novo_imovel.id,
                    )
                    db.session.add(nova_img)
                    index_caminho_imagem+=1
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
            app.logger.info('^ adição de imóvel mal sucedido')
            flash("O Imóvel não foi adicionado! Verifique e corrija os campos com informações inválidas", "error")
            print(f"Erros de validação: {form.errors}")
            imoveis = Imovel.query.all()
            return render_template('admin.html', mensagem="Erro ao adicionar imóvel", imoveis=imoveis, form=form)
    else:
        app.logger.info('^ painel de admin foi acessado')
        imoveis = Imovel.query.all()
        return render_template('admin.html', imoveis=imoveis, form=form)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
