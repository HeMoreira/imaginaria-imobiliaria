import os
from datetime import datetime, timedelta

failed_login_attempts = {}
ip_block_duration = timedelta(minutes=15)
caminho_base = 'static/images'

def salvar_imagens(lista_de_imagens:list):
    lista_de_caminhos_das_imagens = []
    if lista_de_imagens != []:
        for imagem in lista_de_imagens:
            if imagem is not None and imagem.filename != '':
                caminho_da_nova_imagem = os.path.join(caminho_base, imagem.filename)
                if os.path.exists(caminho_da_nova_imagem):
                    caminho_da_nova_imagem = renomear_para_um_nome_unico(imagem.filename, 1)
                imagem.save(caminho_da_nova_imagem)
                lista_de_caminhos_das_imagens.append(caminho_da_nova_imagem)
            else:
                lista_de_caminhos_das_imagens.append("imagem não encontrada")
        return lista_de_caminhos_das_imagens
    else:
        return ["imagem não encontrada"] * len(lista_de_imagens)
            

def renomear_para_um_nome_unico(filename:str, contagem:int):
    new_filename = filename
    if filename.endswith(".png"):
        new_filename = filename[:-4] + f"({contagem}).png"
    elif filename.endswith(".jpg"):
        new_filename = filename[:-4] + f"({contagem}).jpg"
    elif filename.endswith(".jpeg"):
        new_filename = filename[:-5] + f"({contagem}).jpeg"
    caminho_da_nova_imagem = os.path.join(caminho_base, new_filename)
    if os.path.exists(caminho_da_nova_imagem):
        return renomear_para_um_nome_unico(filename, contagem + 1)
    else:
        return caminho_da_nova_imagem
    
def esta_bloqueado(ip):
    ip_number_of_tries = obter_tentativas_de_login(ip)
    if ip_number_of_tries < 3:
        return False
    else:
        if datetime.now() > failed_login_attempts[ip].get("last_try") + ip_block_duration:
            return False
    return True

def obter_tentativas_de_login(ip):
    ip_failed_login_attempts = failed_login_attempts.get(ip, None)
    if ip_failed_login_attempts == None:
        return 0
    else:
        return ip_failed_login_attempts.get("attempts")

def aumentar_contador_de_tentativas_de_login(ip):
    failed_login_attempts[ip] = {
        "attempts":obter_tentativas_de_login(ip) + 1,
        "last_try":datetime.now(),
    }

def zerar_contador_de_tentativas_de_login(ip):
    del failed_login_attempts[ip]