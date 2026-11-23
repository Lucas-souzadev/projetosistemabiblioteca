import pytest
import usuarios


def test_nao_permite_numeros_no_nome_do_usuario():
    with pytest.raises(ValueError, match="O nome do usuario nao pode conter numeros"):
        usuarios.cadastrar_usuario("Joao123", "joao@email.com")