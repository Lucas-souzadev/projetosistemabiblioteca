import os, sys
from datetime import datetime

import livros
import emprestimos


def livros_atrasados(hoje=None):
    if hoje is None:
        hoje = datetime.utcnow().date()
    lista = []
    for e in emprestimos.EMPRESTIMOS:
        if e["devolvido_em"] is None and e["data_prevista"] < hoje:
            lista.append(e)
    return lista


def livros_mais_emprestados(top=3):
    contagem = {}
    for e in emprestimos.EMPRESTIMOS:
        contagem[e["livro_id"]] = contagem.get(e["livro_id"], 0) + 1
    ordenado = sorted(contagem.items(), key=lambda x: x[1])
    resultado = []
    for livro_id, qtd in ordenado[:top]:
        l = livros.buscar_por_id(livro_id)
        resultado.append((l["titulo"], qtd))
    return resultado


def taxa_ocupacao():
    total = 0
    disp = 0
    for l in livros.LIVROS:
        total = total + l["copias"]
        disp = disp + l["disponiveis"]
    return (total - disp) / total * 100


def imprimir_resumo():
    print("===== RESUMO DA BIBLIOTECA =====")
    t = 0
    for l in livros.LIVROS:
        t = t + l["copias"]
    print("Total de exemplares:", t)
    d = 0
    for l in livros.LIVROS:
        d = d + l["disponiveis"]
    print("Disponiveis:", d)
    a = 0
    for e in emprestimos.EMPRESTIMOS:
        if e["devolvido_em"] is None:
            a = a + 1
    print("Emprestimos ativos:", a)
    r = 0
    for e in emprestimos.EMPRESTIMOS:
        if e["devolvido_em"] is not None:
            r = r + 1
    print("Emprestimos encerrados:", r)
    atr = livros_atrasados()
    print("Atrasados:", len(atr))
    for e in atr:
        l = livros.buscar_por_id(e["livro_id"])
        print("  -", l["titulo"], "(previsto para", e["data_prevista"].strftime("%d/%m/%Y") + ")")
    print("Mais emprestados:")
    for titulo, qtd in livros_mais_emprestados():
        print("  -", titulo, qtd)
    print("Ocupacao: %.1f%%" % taxa_ocupacao())
