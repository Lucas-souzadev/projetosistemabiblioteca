# Registro de Bugs — Sistema Biblioteca

## 1. Apresentação

Este documento reúne os defeitos identificados durante a análise e execução dos testes do Sistema Biblioteca.

Os problemas confirmados serão registrados como Issues no GitHub, permitindo acompanhar sua investigação, correção e validação.

## 2. Classificação dos Defeitos

Os defeitos serão classificados conforme sua severidade:

- **Baixa:** problema que causa pouco impacto no funcionamento.
- **Média:** problema que prejudica uma funcionalidade, mas possui alternativa de utilização.
- **Alta:** problema que compromete uma funcionalidade importante.
- **Crítica:** problema que impede o funcionamento de uma parte essencial ou compromete gravemente o sistema.

## 3. Bugs Identificados

Os defeitos confirmados serão documentados individualmente a seguir.

---

### BUG-01 — Validação inadequada do campo Ano

**Issue no GitHub:** A definir.

**Funcionalidade afetada:** Cadastro de livros — campo Ano.

**Descrição:** O sistema permite inserir valores numéricos negativos e zero no campo Ano, sem realizar uma validação adequada dos valores informados.

**Passos para reproduzir:**
1. Acessar o cadastro de livros.
2. Preencher os campos obrigatórios.
3. Inserir um ano negativo ou zero.
4. Tentar concluir o cadastro.

**Resultado esperado:** O sistema deve validar o ano informado conforme os critérios estabelecidos para o cadastro de livros.

**Resultado obtido:** O sistema permite cadastrar livros utilizando valores negativos e zero no campo Ano.

**Severidade:** Média

**Tipo de manutenção:** Corretiva.

**Caso de teste relacionado:** CT-02.

**Status da correção:** Aberto.

---

### BUG-02 — Validação inadequada do campo E-mail

**Issue no GitHub:** A definir.

**Funcionalidade afetada:** Cadastro de usuários — campo E-mail.

**Descrição:** O sistema permite cadastrar usuários utilizando endereços de e-mail com formatos inválidos, aparentemente verificando apenas a presença do caractere @.

**Passos para reproduzir:**
1. Acessar o cadastro de usuários.
2. Preencher os campos obrigatórios.
3. Inserir um e-mail inválido, como usuario@gmail.
4. Tentar concluir o cadastro.

**Resultado esperado:** O sistema deve rejeitar endereços de e-mail com formatos inválidos e apresentar uma mensagem de validação.

**Resultado obtido:** O sistema permite concluir o cadastro utilizando um endereço de e-mail inválido.

**Severidade:** Média (provisório).

**Tipo de manutenção:** Corretiva.

**Caso de teste relacionado:** CT-04.

**Status da correção:** Aberto.

---

### BUG-03 — Empréstimo acima da quantidade disponível

**Issue no GitHub:** A definir.

**Funcionalidade afetada:** Empréstimos — controle de estoque.

**Descrição:** O sistema permite realizar empréstimos mesmo quando a quantidade solicitada ultrapassa o estoque disponível, fazendo com que a quantidade de exemplares fique negativa.

**Passos para reproduzir:**
1. Cadastrar um livro com apenas um exemplar disponível.
2. Realizar um empréstimo desse livro.
3. Tentar realizar outro empréstimo do mesmo livro.
4. Consultar a quantidade disponível.

**Resultado esperado:** O sistema deve impedir novos empréstimos quando não houver exemplares disponíveis.

**Resultado obtido:** O sistema permite realizar o empréstimo e apresenta quantidade negativa no estoque.

**Severidade:** Alta.

**Tipo de manutenção:** Corretiva.

**Caso de teste relacionado:** CT-05.

**Status da correção:** Aberto.

---

### BUG-04 — Estoque não atualizado após devolução

**Issue no GitHub:** A definir.

**Funcionalidade afetada:** Devoluções — controle de estoque.

**Descrição:** Após a devolução de um livro, a quantidade disponível não é atualizada corretamente, impedindo que o exemplar retorne ao estoque.

**Passos para reproduzir:**
1. Acessar a área de empréstimos.
2. Registrar um empréstimo de determinado livro.
3. Acessar a área de devoluções.
4. Realizar a devolução.
5. Consultar novamente a quantidade disponível.

**Resultado esperado:** O sistema deve acrescentar o exemplar devolvido à quantidade disponível no estoque.

**Resultado obtido:** A quantidade disponível permanece inalterada após a devolução.

**Severidade:** Alta.

**Tipo de manutenção:** Corretiva.

**Caso de teste relacionado:** CT-06.

**Status da correção:** Aberto.

---

## 3. Observações adicionais

- As severidades apresentadas são classificações iniciais e poderão ser ajustadas pelo grupo.
- Os defeitos serão acompanhados pelas respectivas Issues no GitHub.
- Após as correções, os casos de teste relacionados serão executados novamente para validar as alterações.
- O problema identificado no resumo do estoque (CT-07) será acompanhado junto aos defeitos de controle de estoque, pois pode ser uma consequência das quantidades negativas.
