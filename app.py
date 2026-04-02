from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, current_user
from flask_talisman import Talisman
from models import db
from models import Imovel, ImagensImovel, Admin, ImagemComDescricao, PlantaComDescricao
from utils import obter_tentativas_de_login, salvar_imagens_de_novo_imovel, esta_bloqueado, aumentar_contador_de_tentativas_de_login, zerar_contador_de_tentativas_de_login, deletar_imagens, instanciar_novas_imagens_com_descricao, instanciar_novas_plantas_com_descricao
from flask_migrate import Migrate
from logging_utils import init_app_logging
from forms import AdminForm, ImovelForm
from forms import TipoDeProduto, Status
from werkzeug.datastructures import CombinedMultiDict
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from slugify import slugify
# from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config


app = Flask(__name__)
init_app_logging(app)
app.config.from_object(Config)
csrf = CSRFProtect(app)

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

@app.route("/lo_11gin_k", methods=['POST', 'GET'])
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

@app.route("/ad_11min_k/imoveis/<slug_imovel>", methods=['GET'])
def mostrar_imovel_admin(slug_imovel):
    imovel = Imovel.query.filter_by(slug=slug_imovel).first_or_404()
    return render_template('info_imovel_admin.html', imovel=imovel)

@app.route("/ad_11min_k/edit/<id_imovel>", methods=['GET', 'POST'])
@limiter.limit("6/minute")
def editar_imovel(id_imovel):
    imovel = Imovel.query.get_or_404(id_imovel)
    if request.method == 'POST':
        app.logger.warning(f'^ O imóvel *{imovel.nome}* começou a ser editado pelo painél de admin')
        form = ImovelForm(CombinedMultiDict((request.form, request.files)))
        form.tipo_de_produto.choices = [(tipo.name, tipo.value) for tipo in TipoDeProduto]
        form.status.choices = [(status.name, status.value) for status in Status]
        if form.validate():
            try:
                caminhos_antigos_imagens_principais = []
                for campo in imovel.imagens_principais_do_produto:
                    caminhos_antigos_imagens_principais.extend([
                        campo.caminho_da_imagem_principal,
                        campo.caminho_da_imagem_de_fachada1,
                        campo.caminho_da_imagem_de_fachada2,
                    ])
                lista_de_caminhos_das_imagens_principais, _, _ = salvar_imagens_de_novo_imovel(form)
                
                imovel.nome = form.nome.data
                imovel.descricao = form.descricao.data
                imovel.tipo_de_produto = TipoDeProduto[form.tipo_de_produto.data]
                imovel.status = Status[form.status.data]
                imovel.esta_visivel = form.esta_visivel.data
                imovel.esta_em_destaque = form.esta_em_destaque.data
                imovel.preco_compra = form.preco_compra.data
                imovel.preco_aluguel = form.preco_aluguel.data
                imovel.condominio = form.condominio.data
                imovel.iptu = form.iptu.data
                imovel.menor_area_em_metros_quadrados = form.menor_area_em_metros_quadrados.data
                imovel.maior_area_em_metros_quadrados = form.maior_area_em_metros_quadrados.data
                imovel.menor_quantidade_de_dormitorios = form.menor_quantidade_de_dormitorios.data
                imovel.maior_quantidade_de_dormitorios = form.maior_quantidade_de_dormitorios.data
                imovel.cidade = form.cidade.data
                imovel.bairro = form.bairro.data
                imovel.endereco = form.endereco.data
                imovel.cep = form.cep.data
                # Atualizar slug se o nome mudou
                imovel.slug = slugify(form.nome.data)

                if imovel.imagens_principais_do_produto:
                    imagem_existente = imovel.imagens_principais_do_produto[0]
                    imagem_existente.caminho_da_imagem_principal = lista_de_caminhos_das_imagens_principais[0]
                    imagem_existente.caminho_da_imagem_de_fachada1 = lista_de_caminhos_das_imagens_principais[1]
                    imagem_existente.caminho_da_imagem_de_fachada2 = lista_de_caminhos_das_imagens_principais[2]
                else:
                    imagens_principais_novo_imovel = ImagensImovel(
                        caminho_da_imagem_principal=lista_de_caminhos_das_imagens_principais[0],
                        caminho_da_imagem_de_fachada1=lista_de_caminhos_das_imagens_principais[1],
                        caminho_da_imagem_de_fachada2=lista_de_caminhos_das_imagens_principais[2],
                    )
                    imovel.imagens_principais_do_produto.append(imagens_principais_novo_imovel)
                
                db.session.flush()
                db.session.commit()
                deletar_imagens(caminhos_antigos_imagens_principais)
                flash("Imóvel editado com sucesso!", "success")
                app.logger.warning(f'^ O imóvel *{imovel.nome}* foi editado com sucesso pelo painél de admin')
                return redirect(url_for('mostrar_imovel_admin', slug_imovel=imovel.slug))
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'^ Erro ao editar imóvel: {str(e)}')
                flash("Erro ao editar o imóvel. Tente novamente.", "error")
                form = ImovelForm(obj=imovel)
                form.tipo_de_produto.choices = [(tipo.name, tipo.value) for tipo in TipoDeProduto]
                form.status.choices = [(status.name, status.value) for status in Status]
                return render_template('editar_imovel.html', form=form, imovel=imovel)
        else:
            app.logger.info(f'^ Erros de validação ao editar imóvel: {form.errors}')
            flash("Erro de validação. Verifique os campos com informações inválidas.", "error")
            return render_template('editar_imovel.html', form=form, imovel=imovel)
    elif request.method == 'GET':
        form = ImovelForm(obj=imovel)
        form.tipo_de_produto.choices = [(tipo.name, tipo.value) for tipo in TipoDeProduto]
        form.status.choices = [(status.name, status.value) for status in Status]
        form.tipo_de_produto.data = imovel.tipo_de_produto.name
        form.status.data = imovel.status.name
        for index, imagem in enumerate(imovel.imagens_do_produto):
            if index < len(form.lista_de_caminhos_de_imagens_adicionais):
                form.lista_de_caminhos_de_imagens_adicionais[index].descricao.data = imagem.descricao
        for index, planta in enumerate(imovel.plantas_do_produto):
            if index < len(form.lista_de_caminhos_de_imagens_de_plantas):
                form.lista_de_caminhos_de_imagens_de_plantas[index].descricao.data = planta.descricao
        return render_template('editar_imovel.html', form=form, imovel=imovel)


@app.route("/ad_11min_k", methods=['POST', 'GET'])
@limiter.limit("6/minute")
def admin():
    form = ImovelForm(CombinedMultiDict((request.form, request.files)))
    if request.method == 'POST':
        if form.validate():
            lista_de_caminhos_das_imagens_principais, lista_de_caminhos_das_imagens, lista_de_caminhos_das_plantas = salvar_imagens_de_novo_imovel(form)

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
            imagens_principais_novo_imovel = ImagensImovel(
                caminho_da_imagem_principal=lista_de_caminhos_das_imagens_principais[0],
                caminho_da_imagem_de_fachada1=lista_de_caminhos_das_imagens_principais[1],
                caminho_da_imagem_de_fachada2=lista_de_caminhos_das_imagens_principais[2],
            )
            novo_imovel.imagens_principais_do_produto.append(imagens_principais_novo_imovel)
            db.session.add(novo_imovel)
            db.session.flush()
            instanciar_novas_imagens_com_descricao(form, lista_de_caminhos_das_imagens, novo_imovel.id, db)
            instanciar_novas_plantas_com_descricao(form, lista_de_caminhos_das_plantas, novo_imovel.id, db)
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

@app.route("/ad_11min_k/delete/<slug_imovel>", methods=['GET', 'POST'])
@limiter.limit("1/minute")
def deletar_imovel(slug_imovel):
    imovel = Imovel.query.filter_by(slug=slug_imovel).first_or_404()
    if request.method == 'POST':
        app.logger.warning(f'^ O imóvel *{imovel.nome}* começou a ser deletado do banco de dados pelo painél de admin')
        lista_de_caminhos = []
        for campo in imovel.imagens_principais_do_produto:
            lista_de_caminhos.append(campo.caminho_da_imagem_principal)
            lista_de_caminhos.append(campo.caminho_da_imagem_de_fachada1)
            lista_de_caminhos.append(campo.caminho_da_imagem_de_fachada2)
        for campo in imovel.imagens_do_produto:
            lista_de_caminhos.append(campo.caminho)
        for campo in imovel.plantas_do_produto:
            lista_de_caminhos.append(campo.caminho)
        deletar_imagens(lista_de_caminhos)
        try:
            db.session.delete(imovel)
            db.session.commit()
            flash("Imóvel deletado com sucesso!", "success")
            app.logger.warning(f'^ O imóvel citado foi deletado do banco de dados pelo painél de admin com sucesso')
            return redirect(url_for('admin'))
        except:
            flash("Falha ao deletar o imóvel... Verifique se o nome do mesmo foi escrito corretamente.", "error")
            return redirect(url_for('admin'))
    else:
        return render_template('confirmar_acao.html', imovel=imovel)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
