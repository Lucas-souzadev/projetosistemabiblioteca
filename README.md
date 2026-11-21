# Sistema de Biblioteca

Sistema simples de biblioteca em Python, usado como base do projeto final de Teste e Manutenção de Software.

## O que o sistema faz

- Cadastra livros (com número de cópias) e busca por título.
- Cadastra usuários.
- Registra empréstimos (prazo de 14 dias, limite por usuário) e devoluções, com multa por atraso.
- Gera um resumo com livros atrasados, mais emprestados e taxa de ocupação do acervo.

## Estrutura

- `livros.py`: cadastro e busca de livros
- `usuarios.py`: cadastro de usuários
- `emprestimos.py`: empréstimos, devoluções e multas
- `relatorios.py`: relatórios
- `storage.py`: salva e carrega os dados em JSON
- `main.py`: menu principal (terminal)
- `web.py`: servidor web com API JSON e interface no navegador
- `static/`: front-end (HTML, CSS e JavaScript puro)

## Como executar

Requer Python 3.10 ou superior. Não há dependências externas.

Pelo terminal:

```bash
python main.py
```

Pelo navegador:

```bash
python web.py          # abre em http://localhost:8000
python web.py 8080     # porta personalizada
```

Na interface web os dados são gravados em `dados/` após cada alteração.

### API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/livros?q=termo` | Lista livros (filtra por título se `q` for informado) |
| POST | `/api/livros` | Cadastra livro `{titulo, autor, ano, copias}` |
| DELETE | `/api/livros/<id>` | Remove livro |
| GET | `/api/usuarios` | Lista usuários |
| POST | `/api/usuarios` | Cadastra usuário `{nome, email}` |
| GET | `/api/emprestimos` | Lista empréstimos |
| POST | `/api/emprestimos` | Empresta `{usuario_id, livro_id}` |
| POST | `/api/emprestimos/<id>/devolucao` | Devolve e retorna `{multa}` |
| GET | `/api/resumo` | Totais, atrasados, mais emprestados e ocupação |

## Situação atual

O sistema não tem testes automatizados e a documentação é mínima. Os dados ficam em memória enquanto o programa roda e são gravados em `dados/` ao sair.

## test