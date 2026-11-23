# Guia de Contribuição

Este documento apresenta as orientações para contribuir com o desenvolvimento do Sistema de Biblioteca, organizando o fluxo de trabalho com Git, GitHub e testes automatizados.

## 1. Organização do trabalho

As alterações no projeto devem ser realizadas em branches individuais, evitando modificações diretamente na branch principal (`main`).

## 2. Atualizando o projeto

Antes de iniciar uma nova tarefa, atualize sua versão local:

```bash
git switch main
git pull origin main
```

## 3. Criando uma branch

Crie uma nova branch para cada tarefa:

```bash
git switch -c tipo/descricao-da-tarefa
```

Exemplos:

- `fix/corrige-cadastro-livros`
- `feat/adiciona-funcionalidade`
- `docs/atualiza-documentacao`
- `ci/configura-pipeline`

## 4. Realizando alterações e commits

Após modificar os arquivos, verifique as alterações:

```bash
git status
```

Adicione os arquivos e registre um commit:

```bash
git add .
git commit -m "tipo: descrição da alteração"
```

Exemplos de mensagens:

- `fix: corrige validação de cadastro`
- `test: adiciona testes de empréstimos`
- `docs: atualiza documentação`
- `ci: configura integração contínua`

## 5. Enviando alterações

Envie sua branch para o repositório remoto:

```bash
git push -u origin nome-da-branch
```

Em seguida, abra um Pull Request no GitHub, direcionando sua branch para `main`.

As alterações devem ser revisadas antes de serem integradas à branch principal.

## 6. Executando os testes

O projeto utiliza Pytest para executar os testes automatizados.

Para executar localmente:

```bash
python -m pytest -v
```

Os testes estão organizados no diretório `tests/`.

## 7. Integração contínua (GitHub Actions)

O projeto utiliza GitHub Actions para automatizar a execução dos testes.

A pipeline está configurada em:

`.github/workflows/tests.yml`

A execução acontece automaticamente quando:

- Há um push diretamente na branch `main`.
- Um Pull Request é aberto ou atualizado com destino à `main`.

A pipeline configura o ambiente Python, instala o Pytest e executa os testes automatizados.

Os resultados podem ser acompanhados pela aba **Actions** do GitHub.

Pull Requests com falhas nos testes devem ser analisados e corrigidos antes da integração.

## 8. Resolução de conflitos

Quando houver conflitos entre branches, as alterações devem ser analisadas antes da resolução, preservando as funcionalidades e os testes existentes.

Após resolver os conflitos, os testes automatizados devem ser executados novamente.