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
        'https://code.jquery.com'
    ],
    'style-src': [
        '\'self\'',
        'https://fonts.googleapis.com',
        'https://cdn.jsdelivr.net'
    ],
    'font-src': [
        '\'self\'',
        'https://fonts.gstatic.com',
        'https://cdn.jsdelivr.net'
    ]
}

