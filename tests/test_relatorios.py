import pytest

import livros
import relatorios


@pytest.fixture(autouse=True)
def limpar_livros():
    livros.LIVROS.clear()


def test_taxa_ocupacao_sem_livros():
    assert relatorios.taxa_ocupacao() == 0.0