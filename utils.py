from models import db


def salvar_imagens(caminho_base:str, lista_de_imagens:list):
    lista_de_caminhos_das_imagens = []
    if lista_de_imagens != []:
        for imagem in lista_de_imagens:
            if imagem is not None:
                caminho_da_nova_imagem = os.path.join(caminho_base, imagem.filename)
                imagem.save(caminho_da_nova_imagem)
                lista_de_caminhos_das_imagens.append(caminho_da_nova_imagem)
            else:
                lista_de_caminhos_das_imagens.append("imagem não encontrada")
        return lista_de_caminhos_das_imagens
    else:
        return ["imagem não encontrada"] * len(lista_de_imagens)