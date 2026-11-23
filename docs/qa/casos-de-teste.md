# Casos de Teste — Sistema Biblioteca

## 1. Apresentação

Este documento reúne os casos de teste realizados no Sistema Biblioteca, com o objetivo de verificar o funcionamento das funcionalidades disponíveis, identificar comportamentos incorretos e avaliar se os resultados apresentados correspondem aos resultados esperados.

## 2. Identificação dos Casos de Teste

Os testes serão identificados por códigos sequenciais, de CT-01 até CT-08.

Cada caso de teste apresentará sua funcionalidade, objetivo, dados utilizados, passos para execução, resultado esperado, resultado obtido e status.

## 3. Casos de Teste

Os casos de teste serão documentados individualmente a seguir.

---

### CT-01 — Inserir números ou caracteres especiais no campo Autor

**Funcionalidade:** Cadastro de livros — campo Autor.

**Objetivo:** Verificar se o campo Autor impede a inserção de números e caracteres especiais.

**Tipo:** Negativo.

**Pré-condições:** Estar na página de cadastro de livros.

**Dados utilizados:** Exemplo: "(João004?!?)". Escrever o nome do autor exatamente assim.

**Passos para execução:**
1. Acessar a página de cadastro de livros.
2. Inserir números ou caracteres especiais no campo Autor.
3. Preencher os demais campos obrigatórios.
4. Tentar cadastrar o livro.

**Resultado esperado:** O sistema deve impedir o cadastro quando o campo Autor apresentar caracteres não permitidos pela regra de validação.

**Resultado obtido:** O sistema permite cadastrar livros mesmo quando o campo Autor contém números e caracteres especiais.

**Status:** Reprovado.

**Bug relacionado:** A confirmar.

---

### CT-02 — Inserir valores numéricos inválidos no campo Ano

**Funcionalidade:** Cadastro de livros — campo Ano.

**Objetivo:** Verificar se o campo Ano valida corretamente os valores numéricos informados durante o cadastro de livros.

**Tipo:** Negativo.

**Pré-condições:** Estar na página de cadastro de livros.

**Dados utilizados:** Ano negativo: -2020. Ano zero: 0. Valores altos: 1000000.

**Passos para execução:**
1. Acessar a página de cadastro de livros.
2. Preencher os campos obrigatórios do cadastro.
3. Inserir um valor negativo, zero ou valores absurdamente altos no campo Ano.
4. Tentar cadastrar o livro.
5. Repetir o procedimento com outros valores numéricos, se necessário.

**Resultado esperado:** O sistema deve validar o ano informado e impedir o cadastro quando o valor estiver fora dos critérios aceitos.

**Resultado obtido:** O sistema permite inserir valores numéricos positivos, negativos e zero no campo Ano, sem validar adequadamente se o valor informado é válido.

**Status:** Reprovado.

**Bug relacionado:** A confirmar.

---

### CT-03 — Inserir números no campo Nome

**Funcionalidade:** Cadastro de usuários — campo Nome.

**Objetivo:** Verificar se o campo Nome valida corretamente as informações inseridas durante o cadastro de usuários.

**Tipo:** Negativo.

**Pré-condições:** Estar na página de cadastro de usuários.

**Dados utilizados:** Nome contendo números: 666denilson ou 2008

**Passos para execução:**
1. Acessar a página de cadastro de usuários.
2. Inserir números no campo Nome.
3. Preencher os demais campos obrigatórios.
4. Tentar concluir o cadastro.

**Resultado esperado:** O sistema deve validar o nome informado e impedir o cadastro caso o valor não atenda aos critérios estabelecidos.

**Resultado obtido:** O sistema permite inserir números no campo Nome durante o cadastro de usuários.

**Status:** Reprovado

**Bug relacionado:** A confirmar.

---

### CT-04 — Cadastrar usuário com e-mail inválido

**Funcionalidade:** Cadastro de usuários — campo E-mail.

**Objetivo:** Verificar se o sistema valida corretamente o formato do endereço de e-mail informado.

**Tipo:** Negativo.

**Pré-condições:** Estar na página de cadastro de usuários.

**Dados utilizados:**
- usuario@gmail
- @gmail.com
- usuario@

**Passos para execução:**
1. Acessar a página de cadastro de usuários.
2. Preencher os campos obrigatórios.
3. Inserir um dos formatos de e-mail inválidos.
4. Tentar concluir o cadastro.
5. Repetir o procedimento com os demais formatos.

**Resultado esperado:** O sistema deve rejeitar endereços de e-mail com formatos inválidos e apresentar uma mensagem de validação.

**Resultado obtido:** O sistema permite cadastrar usuários utilizando endereços de e-mail inválidos, aparentemente verificando apenas a presença do caractere @.

**Status:** Reprovado.

**Bug relacionado:** A confirmar.

---

### CT-05 — Realizar empréstimo acima do estoque disponível

**Funcionalidade:** Empréstimos — controle de estoque.

**Objetivo:** Verificar se o sistema impede a realização de empréstimos quando a quantidade solicitada ultrapassa o estoque disponível.

**Tipo:** Negativo.

**Pré-condições:** Ter um livro cadastrado com apenas um exemplar disponível.

**Dados utilizados:** Livro com estoque de 1 exemplar.

**Passos para execução:**
1. Acessar a área de empréstimos.
2. Selecionar um livro com apenas um exemplar disponível.
3. Realizar o primeiro empréstimo.
4. Tentar realizar um segundo empréstimo do mesmo livro.
5. Verificar a quantidade disponível no estoque.

**Resultado esperado:** O sistema deve impedir o segundo empréstimo, pois não existem exemplares disponíveis.

**Resultado obtido:** O sistema permite realizar o segundo empréstimo, fazendo com que a quantidade disponível fique negativa.

**Status:** Reprovado.

**Bug relacionado:** A confirmar.

---

### CT-06 — Verificar atualização do estoque após devolução

**Funcionalidade:** Devoluções — controle de estoque.

**Objetivo:** Verificar se a quantidade disponível de livros é atualizada corretamente após a realização de uma devolução.

**Tipo:** Negativo.

**Pré-condições:** Possuir um livro cadastrado e um empréstimo registrado.

**Dados utilizados:** Livro emprestado com quantidade disponível reduzida.

**Passos para execução:**
1. Acessar a área de empréstimos.
2. Registrar um empréstimo de determinado livro.
3. Acessar a área de devoluções.
4. Realizar a devolução do livro.
5. Consultar novamente a quantidade disponível no estoque.

**Resultado esperado:** Após a devolução, o sistema deve acrescentar o exemplar devolvido à quantidade disponível.

**Resultado obtido:** A quantidade disponível permanece inalterada após a devolução, não restaurando corretamente o estoque.

**Status:** Reprovado.

**Bug relacionado:** A confirmar.

---

### CT-07 — Verificar cálculo do total disponível no resumo

**Funcionalidade:** Resumo — total de livros disponíveis.

**Objetivo:** Verificar se o sistema calcula corretamente o total de exemplares disponíveis no estoque.

**Tipo:** Negativo.

**Pré-condições:** Possuir livros cadastrados com quantidades disponíveis positivas e registros com quantidades negativas.

**Dados utilizados:** 
- Livro A: 9 exemplares.
- Livro B: 4 exemplares.
- Livro C: -1 exemplar.
- Livro D: -2 exemplares.

**Passos para execução:**
1. Acessar o sistema.
2. Garantir que os livros estejam cadastrados com as quantidades informadas.
3. Acessar a área de resumo.
4. Consultar o total de exemplares disponíveis.
5. Comparar o resultado apresentado com as quantidades dos livros.

**Resultado esperado:** O resumo deve apresentar um total de estoque coerente com as quantidades efetivamente disponíveis, sem permitir que registros inválidos distorçam o cálculo.

**Resultado obtido:** O sistema considera as quantidades negativas no cálculo, apresentando o total de 10 exemplares em vez de 13 exemplares positivos.

**Status:** Reprovado.

**Bug relacionado:** A confirmar.

---

### CT-08 — Verificar possibilidade de excluir usuário cadastrado

**Funcionalidade:** Gerenciamento de usuários.

**Objetivo:** Verificar se o sistema disponibiliza uma opção para excluir usuários cadastrados.

**Tipo:** A confirmar — possível teste de funcionalidade ausente.

**Pré-condições:** Possuir pelo menos um usuário cadastrado no sistema.

**Dados utilizados:** Conta de usuário previamente cadastrada.

**Passos para execução:**
1. Acessar a área de gerenciamento de usuários.
2. Localizar um usuário cadastrado.
3. Verificar se existe uma opção para excluir a conta.
4. Caso exista, tentar realizar a exclusão.
5. Verificar se o usuário foi removido do sistema.

**Resultado esperado:** Caso a exclusão de usuários seja uma funcionalidade prevista, o sistema deve disponibilizar uma opção para remover a conta cadastrada.

**Resultado obtido:** Não foi localizada uma opção para excluir usuários cadastrados.

**Status:** A confirmar.

**Bug relacionado:** A confirmar.