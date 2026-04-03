import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY não encontrada nas variáveis de ambiente.")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///imaginariaimobiliaria.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    # Só ativa Secure se não estiver em ambiente de desenvolvimento (evita quebrar o login no localhost)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    CSP_CONFIG = {
        'default-src': '\'self\'',
        #  TODO: remover assim que imagem do hero definitiva estiver definida
        'img-src': [
            '\'self\'',
            '*',  # Permite imagens de qualquer lugar
        ],
        'script-src': [
            '\'self\'',
            'unsafe-hashes'
            'https://cdn.jsdelivr.net',
            'https://code.jquery.com',
            'https://unpkg.com'
        ],
        'style-src': [
            '\'self\'',
            'https://fonts.googleapis.com',
            'https://cdn.jsdelivr.net',
            'https://unpkg.com'
        ],
        'font-src': [
            '\'self\'',
            'https://fonts.gstatic.com',
            'https://cdn.jsdelivr.net'
        ],
        'connect-src': [
            "\'self\'",
            "https://*.tile.openstreetmap.org",
            "https://unpkg.com"
        ]
    }

