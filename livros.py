LIVROS = []


def cadastrar_livro(titulo, autor, ano, copias=1):
    if any(caractere.isdigit() for caractere in autor):
        raise ValueError("O nome do autor nao pode conter numeros")

    if ano <= 0:
        raise ValueError("O ano de publicacao deve ser maior que zero")

    novo_id = max([l["id"] for l in LIVROS], default=0) + 1
    livro = {
        "id": novo_id,
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "copias": copias,
        "disponiveis": copias,
    }
    LIVROS.append(livro)
    return livro    


def buscar_por_id(livro_id):
    for l in LIVROS:
        if l["id"] == livro_id:
            return l
    return None


def buscar_por_titulo(termo):
    resultado = []
    for l in LIVROS:
        if termo in l["titulo"]:
            resultado.append(l)
    return resultado


def listar_livros():
    return list(LIVROS)


def remover_livro(livro_id):
    livro = buscar_por_id(livro_id)
    if livro is None:
        raise ValueError("Livro nao encontrado")
    LIVROS.remove(livro)
