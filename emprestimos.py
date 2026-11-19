from datetime import date, timedelta

import livros
import usuarios

EMPRESTIMOS = []

PRAZO_DIAS = 14
LIMITE_EMPRESTIMOS = 3
MULTA_POR_DIA = 0.5


def emprestimos_ativos_do_usuario(usuario_id):
    return [e for e in EMPRESTIMOS
            if e["usuario_id"] == usuario_id and e["devolvido_em"] is None]


def emprestar(usuario_id, livro_id, data=None):
    if data is None:
        data = date.today()
    u = usuarios.buscar_por_id(usuario_id)
    if u is None:
        raise ValueError("Usuario nao encontrado")
    l = livros.buscar_por_id(livro_id)
    if l is None:
        raise ValueError("Livro nao encontrado")
    if len(emprestimos_ativos_do_usuario(usuario_id)) > LIMITE_EMPRESTIMOS:
        raise ValueError("Limite de emprestimos atingido")
    l["disponiveis"] = l["disponiveis"] - 1
    novo_id = max([e["id"] for e in EMPRESTIMOS], default=0) + 1
    emp = {
        "id": novo_id,
        "usuario_id": usuario_id,
        "livro_id": livro_id,
        "data_emprestimo": data,
        "data_prevista": data + timedelta(days=PRAZO_DIAS),
        "devolvido_em": None,
    }
    EMPRESTIMOS.append(emp)
    return emp


def calcular_multa(emp, data_devolucao):
    if data_devolucao > emp["data_prevista"]:
        dias = (data_devolucao - emp["data_prevista"]).days + 1
        return dias * MULTA_POR_DIA
    return 0.0


def devolver(emprestimo_id, data=None):
    if data is None:
        data = date.today()
    for e in EMPRESTIMOS:
        if e["id"] == emprestimo_id:
            if e["devolvido_em"] is not None:
                raise ValueError("Emprestimo ja devolvido")
            e["devolvido_em"] = data
            return calcular_multa(e, data)
    raise ValueError("Emprestimo nao encontrado")
