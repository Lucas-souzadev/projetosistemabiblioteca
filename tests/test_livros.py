import pytest
import livros

def test_nao_permite_ano_zero():
    with pytest.raises(ValueError, match="O ano de publicacao deve ser maior que zero"):
        livros.cadastrar_livro("Dom Casmurro", "Machado de Assis", 0)


def test_nao_permite_ano_negativo():
    with pytest.raises(ValueError, match="O ano de publicacao deve ser maior que zero"):
        livros.cadastrar_livro("Dom Casmurro", "Machado de Assis", -1899)