import pytest
import livros


def test_nao_permite_ano_zero():
    with pytest.raises(ValueError, match="O ano de publicacao deve ser maior que zero"):
        livros.cadastrar_livro("Dom Casmurro", "Machado de Assis", 0)


def test_nao_permite_ano_negativo():
    with pytest.raises(ValueError, match="O ano de publicacao deve ser maior que zero"):
        livros.cadastrar_livro("Dom Casmurro", "Machado de Assis", -1899)


def test_nao_permite_numeros_no_nome_do_autor():
    with pytest.raises(ValueError, match="O nome do autor nao pode conter numeros"):
        livros.cadastrar_livro("Dom Casmurro", "Machado 123", 1899)