import pytest

import livros
import relatorios
import emprestimos


@pytest.fixture(autouse=True)
def limpar_dados():
    livros.LIVROS.clear()
    emprestimos.EMPRESTIMOS.clear()

def test_livros_mais_emprestados_ordena_do_maior_para_o_menor():
    livro1 = livros.cadastrar_livro("Livro A", "Autor A", 2020)
    livro2 = livros.cadastrar_livro("Livro B", "Autor B", 2021)

    emprestimos.EMPRESTIMOS.extend([
        {"livro_id": livro1["id"]},
        {"livro_id": livro2["id"]},
        {"livro_id": livro2["id"]},
        {"livro_id": livro2["id"]},
    ])

    resultado = relatorios.livros_mais_emprestados()

    assert resultado[0] == ("Livro B", 3)
    assert resultado[1] == ("Livro A", 1)