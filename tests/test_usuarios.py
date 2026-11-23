import pytest
import usuarios


def test_nao_permite_numeros_no_nome_do_usuario():
    with pytest.raises(ValueError, match="O nome do usuario nao pode conter numeros"):
        usuarios.cadastrar_usuario("Joao123", "joao@email.com")


def test_nao_permite_email_sem_dominio():
    with pytest.raises(ValueError, match="Email invalido"):
        usuarios.cadastrar_usuario("Joao", "joao@")


def test_nao_permite_email_sem_usuario():
    with pytest.raises(ValueError, match="Email invalido"):
        usuarios.cadastrar_usuario("Joao", "@email.com")


def test_nao_permite_email_sem_ponto_no_dominio():
    with pytest.raises(ValueError, match="Email invalido"):
        usuarios.cadastrar_usuario("Joao", "joao@email")


def test_nao_permite_email_com_espacos():
    with pytest.raises(ValueError, match="Email invalido"):
        usuarios.cadastrar_usuario("Joao", "joao email@email.com")  