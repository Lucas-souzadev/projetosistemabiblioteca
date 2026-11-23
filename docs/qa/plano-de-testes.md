# Plano de Testes — Sistema Biblioteca

## 1. Objetivo

O objetivo deste plano é avaliar a qualidade e o funcionamento do Sistema Biblioteca, identificando falhas nas funcionalidades existentes e verificando se o sistema apresenta os resultados esperados durante sua utilização.

## 2. Escopo dos Testes

Serão avaliadas as seguintes funcionalidades:

- Cadastro, consulta e remoção de livros.
- Cadastro e gerenciamento de usuários.
- Registro de empréstimos.
- Registro de devoluções.
- Consulta e resumo do estoque.

## 3. Estratégia de Testes

Serão utilizadas diferentes abordagens para avaliar o sistema:

- **Testes positivos:** verificam se as operações realizadas com informações válidas funcionam corretamente.
- **Testes negativos:** verificam se o sistema impede operações ou informações inválidas.
- **Testes de unidade:** avaliam partes individuais do código.
- **Testes de integração:** verificam a comunicação entre diferentes partes do sistema.
- **Caixa-preta:** avalia o comportamento do sistema por meio das entradas e saídas, sem analisar o código interno.
- **Caixa-branca:** avalia a estrutura e a lógica interna do código.

## 4. Ferramentas Utilizadas

- Python: linguagem utilizada no desenvolvimento e nos testes automatizados.
- PyTest: execução dos testes automatizados.
- Git e GitHub: controle de versão e acompanhamento das correções.
- Visual Studio Code: edição e organização dos arquivos.
- Thunder Client: realização de requisições HTTP, quando aplicável.

## 5. Critérios de Avaliação

Um teste será considerado aprovado quando o sistema apresentar o resultado esperado.

Um teste será considerado reprovado quando o comportamento apresentado for diferente do esperado, indicando a necessidade de investigação.

## 6. Registro e Acompanhamento de Defeitos

Os defeitos identificados durante os testes serão documentados e registrados como Issues no GitHub, contendo descrição, passos para reprodução, resultado esperado, resultado obtido, severidade e tipo de manutenção.

## 7. Regressão

Após as correções, os testes serão executados novamente para verificar se os problemas foram resolvidos e se as alterações não prejudicaram outras funcionalidades.