import pytest
import livros

def test_nao_permite_numeros_no_nome_do_autor():
    with pytest.raises(ValueError, match="O nome do autor nao pode conter numeros"):
        livros.cadastrar_livro("Dom Casmurro", "Machado 123", 1899)