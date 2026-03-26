SECRET_KEY = 'incrediblekeythatwilldefinitelybechangedbeforerunningintoproduction'

CSP_CONFIG = {
    'default-src': '\'self\'',
    #  TODO: remover assim que imagem do hero definitiva estiver definida
    'img-src': [
        '\'self\'',
        '*',  # Permite imagens de qualquer lugar
    ],
    'script-src': [
        '\'self\'',
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

