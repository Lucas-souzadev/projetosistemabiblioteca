import json
from datetime import datetime

import livros
import usuarios
import emprestimos

ARQUIVO = "dados\\biblioteca.json"
FORMATO_DATA = "%d/%m/%Y"


def _data_para_texto(d):
    if d is None:
        return None
    return d.strftime(FORMATO_DATA)


def _texto_para_data(t):
    if t is None:
        return None
    return datetime.strptime(t, FORMATO_DATA).date()


def salvar():
    dados = {
        "livros": livros.LIVROS,
        "usuarios": usuarios.USUARIOS,
        "emprestimos": [],
    }
    for e in emprestimos.EMPRESTIMOS:
        copia = dict(e)
        copia["data_emprestimo"] = _data_para_texto(e["data_emprestimo"])
        copia["data_prevista"] = _data_para_texto(e["data_prevista"])
        copia["devolvido_em"] = _data_para_texto(e["devolvido_em"])
        dados["emprestimos"].append(copia)
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)


def carregar():
    try:
        with open(ARQUIVO) as f:
            dados = json.load(f)
    except FileNotFoundError:
        return
    livros.LIVROS[:] = dados["livros"]
    usuarios.USUARIOS[:] = dados["usuarios"]
    emprestimos.EMPRESTIMOS.clear()
    for e in dados["emprestimos"]:
        e["data_emprestimo"] = _texto_para_data(e["data_emprestimo"])
        e["data_prevista"] = _texto_para_data(e["data_prevista"])
        e["devolvido_em"] = _texto_para_data(e["devolvido_em"])
        emprestimos.EMPRESTIMOS.append(e)
