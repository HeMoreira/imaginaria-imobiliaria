# Imaginária Imobiliária

Uma aplicação web desenvolvida em Flask para anúncio e gerenciamento de imóveis, contando com um robusto painel administrativo (CRUD completo) e camadas rigorosas de segurança cibernética orientadas para produção.

## Tecnologias Utilizadas

- Core: Flask (Python)
- Banco de dados e Migrações: SQLAlchemy (ORM), Flask-SQLAlchemy e Flask-Migrate (Alembic)
- Validação e Formularios: WTForms & Flask-WTF (com proteção CSRF nativa)
- Autenticação: Flask-Login
- Segurança: Flask-Talisman, Flask-Limiter e Werkzeug

## Configuração

### 1. Clone o repositório e acesse o diretório principal
```bash
git clone https://github.com/HeMoreira/imaginaria-imobiliaria.git
cd imaginaria-imobiliaria
```
> Lembre-se de definir um ambiente virtual caso queira

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
```bash
# Defina SECRET_KEY, DEBUG e SQLALCHEMY_DATABASE_URI em um arquivo .env
```
> Exemplo (recomendado):
> ```bash
> SECRET_KEY=sua_chave_secreta
> SQLALCHEMY_DATABASE_URI=sqlite:///nome_do_seu_banco_de_dados.db
> DEBUG=True
> ```

### 4. Certifique-se de que o direerório logs/ existe
```bash
# Caso não exista, rode:
mkdir logs
```

### 5. Criar banco de dados e usuário administrador
```bash
flask shell
# No terminal do flask, crie o banco de dados...
from models import db
db.create_all()
# ...E o seu usuário administrador.
from models import Admin
admin = Admin(username='username_do_admin')
admin.set_password('senha_do_admin')
db.session.add(admin)
db.session.commit()
exit()
```
> Contas de admin só podem ser criadas via terminal.

### 6. Rodar o servidor
```bash
python app.py
```

Acesse: http://127.0.0.1:8000 ou http://localhost:8000
---

## Funcionalidades Principais

| Página | Responsabilidade |
|--------|------------------|
| `/`          | Página inicial e visualização de imóveis |
| `/imoveis`   | Listagem e detalhes de imóveis disponíveis |
| `/lo_11gin_k`| Página de login para administradores |
| `/ad_11min_k`| Página de admin + gerenciamento (CRUD) de imóveis |
> OBS: você NÃO será redirecionado para a página de login ao acessar /ad_11min_k. Acesse /lo_11gin_k diretamente.

## Segurança

- Bloqueio de IP (Anti Brute-Force): Integração de rate limit (Flask-Limiter) e bloqueio temporário de IP por 15 minutos após 3 tentativas falhas de login.
- Content Security Policy (CSP): Configurações rígidas via Talisman para impedir ataques de Cross-Site Scripting (XSS) e injeção de dados.
- Autenticação Restrita: Decoradores de login global impedem acessos não autorizados por padrão em qualquer rota que não seja explicitamente pública (deny by default).
- Cookies Seguros: Cookies de sessão configurados estritamente como HTTPOnly, política SameSite=Lax e Secure (ativado automaticamente sob ambiente de produção).
- Auditoria por Log Rotativo: Registro estruturado contendo método HTTP, URL acessada, IP de origem e alertas especiais salvos em arquivos rotativos (logs/security.log) para ações críticas.