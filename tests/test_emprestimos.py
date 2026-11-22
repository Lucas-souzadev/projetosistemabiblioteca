
import pytest
from datetime import date

import emprestimos
import livros
import usuarios


@pytest.fixture(autouse=True)
def limpar_dados():
    emprestimos.EMPRESTIMOS.clear()
    livros.LIVROS.clear()
    usuarios.USUARIOS.clear()


def test_usuario_pode_realizar_tres_emprestimos():
    usuario = usuarios.cadastrar_usuario("Joao", "joao@email.com")

    livro1 = livros.cadastrar_livro("Livro 1", "Autor Um", 2020)
    livro2 = livros.cadastrar_livro("Livro 2", "Autor Dois", 2021)
    livro3 = livros.cadastrar_livro("Livro 3", "Autor Três", 2022)

    emprestimos.emprestar(usuario["id"], livro1["id"], date.today())
    emprestimos.emprestar(usuario["id"], livro2["id"], date.today())
    emprestimos.emprestar(usuario["id"], livro3["id"], date.today())

    assert len(emprestimos.emprestimos_ativos_do_usuario(usuario["id"])) == 3


def test_usuario_nao_pode_realizar_quarto_emprestimo():
    usuario = usuarios.cadastrar_usuario("Joao", "joao@email.com")

    livro1 = livros.cadastrar_livro("Livro 1", "Autor Um", 2020)
    livro2 = livros.cadastrar_livro("Livro 2", "Autor Dois", 2021)
    livro3 = livros.cadastrar_livro("Livro 3", "Autor Três", 2022)
    livro4 = livros.cadastrar_livro("Livro 4", "Autor Quatro", 2023)

    emprestimos.emprestar(usuario["id"], livro1["id"], date.today())
    emprestimos.emprestar(usuario["id"], livro2["id"], date.today())
    emprestimos.emprestar(usuario["id"], livro3["id"], date.today())

    with pytest.raises(ValueError, match="Limite de emprestimos atingido"):
        emprestimos.emprestar(usuario["id"], livro4["id"], date.today())

def test_nao_pode_emprestar_livro_sem_estoque():
    usuario = usuarios.cadastrar_usuario("Carlos", "carlos@email.com")
    livro = livros.cadastrar_livro("Harry Potter", "J.K. Rowling", 1997, copias=0)

    with pytest.raises(ValueError, match="Livro indisponivel para emprestimo"):
        emprestimos.emprestar(usuario["id"], livro["id"], date.today())

    assert livro["disponiveis"] == 0
    assert len(emprestimos.EMPRESTIMOS) == 0
