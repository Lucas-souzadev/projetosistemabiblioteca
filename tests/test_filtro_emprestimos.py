
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


def test_filtrar_emprestimos_por_periodo():
    usuario = usuarios.cadastrar_usuario("Joao", "joao@email.com")

    livro1 = livros.cadastrar_livro("Livro 1", "Autor 1", 2020)
    livro2 = livros.cadastrar_livro("Livro 2", "Autor 2", 2021)
    livro3 = livros.cadastrar_livro("Livro 3", "Autor 3", 2022)

    emprestimos.emprestar(usuario["id"], livro1["id"], date(2026, 11, 10))
    emprestimos.emprestar(usuario["id"], livro2["id"], date(2026, 11, 15))
    emprestimos.emprestar(usuario["id"], livro3["id"], date(2026, 11, 20))

    resultado = emprestimos.buscar_emprestimos_por_periodo(
        date(2026, 11, 10),
        date(2026, 11, 15)
    )

    assert len(resultado) == 2


def test_periodo_invertido_deve_gerar_erro():
    with pytest.raises(ValueError, match="A data inicial nao pode ser maior que a data final"):
        emprestimos.buscar_emprestimos_por_periodo(
            date(2026, 11, 20),
            date(2026, 11, 10)
        )
