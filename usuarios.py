USUARIOS = []


def cadastrar_usuario(nome, email):
    if not nome.strip():
        raise ValueError("Nome obrigatorio")
    if any(caractere.isdigit() for caractere in nome):
        raise ValueError("O nome do usuario nao pode conter numeros")
    if "@" not in email:
        raise ValueError("Email invalido")

    novo_id = max([u["id"] for u in USUARIOS], default=0) + 1
    usuario = {"id": novo_id, "nome": nome, "email": email}
    USUARIOS.append(usuario)
    return usuario


def buscar_por_id(usuario_id):
    for u in USUARIOS:
        if u["id"] == usuario_id:
            return u
    return None


def listar_usuarios():
    return list(USUARIOS)
