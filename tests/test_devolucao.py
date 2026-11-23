
import pytest

import emprestimos
import livros
import usuarios


@pytest.fixture(autouse=True)
def limpar_dados():
    emprestimos.EMPRESTIMOS.clear()
    livros.LIVROS.clear()
    usuarios.USUARIOS.clear()


def test_devolucao_restaura_copia_disponivel():
    usuario = usuarios.cadastrar_usuario("Joao", "joao@email.com")
    livro = livros.cadastrar_livro("Livro 1", "Autor Um", 2020, copias=2)

    emprestimo = emprestimos.emprestar(usuario["id"], livro["id"])

    assert livro["disponiveis"] == 1

    emprestimos.devolver(emprestimo["id"])

    assert livro["disponiveis"] == 2


def test_devolucao_nao_restaura_estoque_duas_vezes():
    usuario = usuarios.cadastrar_usuario("Joao", "joao@email.com")
    livro = livros.cadastrar_livro("Livro 1", "Autor Um", 2020, copias=2)

    emprestimo = emprestimos.emprestar(usuario["id"], livro["id"])
    emprestimos.devolver(emprestimo["id"])

    with pytest.raises(ValueError, match="Emprestimo ja devolvido"):
        emprestimos.devolver(emprestimo["id"])

    assert livro["disponiveis"] == 2
