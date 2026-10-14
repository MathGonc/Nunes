# Integração da Folha — Como era × Como vai ficar
### Domínio ⇄ RP Info por arquivos (hoje) → TOTVS RM ⇄ RP Info por API (futuro)

> **Diagramas desta pasta** — `.drawio` para editar (draw.io) e `.png` para apresentar:
>
> | Diagrama | Para quem |
> |---|---|
> | [COMO_ERA](COMO_ERA.png) | Todos: o processo de hoje, com os 15 retrabalhos numerados |
> | [COMO_VAI_(SIMPLES)](<COMO_VAI_(SIMPLES).png>) | Público geral: como vai ficar, sem termos técnicos |
> | [COMO_VAI_(API)](<COMO_VAI_(API).png>) | Equipe técnica: arquitetura da integração e caminhos de API |
>
> Os números são do fechamento de **agosto/2026**, contados nos arquivos do próprio fechamento.
> Os passos vêm do POP da folha e do POP de fechamento do convênio.

---

## Em uma frase

Hoje a folha sai do Domínio e chega ao RP Info **passando por planilhas, cerca de 43 arquivos e
15 retrabalhos manuais por mês**. Com o TOTVS RM, os dois sistemas passam a **conversar direto por
API**: sem arquivo intermediário, sem planilha e sem redigitação.

---

## Lado a lado

| | Como era · Domínio ⇄ RP Info | Como vai ficar · TOTVS RM ⇄ RP Info |
|---|---|---|
| **Como a informação passa** | Exporta arquivo → trata em planilha → importa à mão | Por API, direto entre os sistemas |
| **Arquivos manipulados por mês** | ~43 | **0** |
| **Retrabalhos manuais** | 15, sendo 4 repetidos loja a loja (até 17×) | **0** |
| **Regras de negócio** | Escondidas em 11 consultas Power Query, em 2 planilhas | Escritas em código e testadas |
| **Identificação do colaborador** | Pelo nome; código digitado à mão quando não bate | Pelo **CPF** |
| **Dados pessoais** | Base inteira (5.682 pessoas, 76 campos) baixada todo mês para pasta de rede | Consulta só a pessoa necessária, nada fica salvo |
| **Pendências de convênio** | 17 arquivos, 17 importações, 1 usuário com acesso | 1 execução para as 17 lojas |
| **Conferência** | No olho, em várias telas; nenhuma trava contra erro | Automática; erro **trava o envio** |
| **Dependência** | 1 pessoa | O sistema executa; a pessoa aprova |

---

## Como era

Três trocas de informação, todas feitas à mão:

```
1. FOLHA          Domínio ──TXT──► planilha Excel ──CSV──► RP Info
2. FUNCIONÁRIOS   RP Info ──base inteira──► pasta de rede ──► planilha   (para saber quem é quem, pelo nome)
3. PENDÊNCIAS     RP Info ──17 TXT, 1 loja por vez──► Domínio            (convênio vira desconto na folha)
```

### Os 15 retrabalhos

Numerados como nas bolinhas vermelhas do diagrama [COMO_ERA](COMO_ERA.png).

| # | Retrabalho | Onde | Frequência |
|:---:|---|---|---|
| 1 | Configurar rubrica nova **loja por loja** | Domínio | até 17× quando surge |
| 2 | Exportar 2 relatórios e conferir no olho na planilha Análise (total e sem FGTS) | Domínio → Excel | mensal |
| 3 | Baixar a base **inteira** de funcionários e sobrescrever o `dfunc.txt` | RP Info → pasta de rede | mensal |
| 4 | Atualizar a planilha e **digitar à mão** o código de quem tem nome divergente | Excel | mensal (6 lançamentos em 08/2026) |
| 5 | Salvar o CSV, reabrir e **apagar o cabeçalho à mão** | Excel | mensal |
| 6 | Importar (Ctrl+D) e **conferir de novo** os totais na tela | RP Info | mensal |
| 7 | Agrupar líquidos por banco, redigitando o valor de cada banco (doc 3607) | RP Info | mensal |
| 8 | Pensão: trocar o portador e digitar os dados bancários na observação | RP Info | mensal |
| 9 | Baixar pendências de 4 contas totalizadoras e conferir no razão (F5) | RP Info | mensal |
| 10 | Conferir vencimentos e totalizar convênio, quebra de caixa e vale café (doc 2005) | RP Info | mensal |
| 11 | Gerar o TXT de pendências **1 loja por vez** | RP Info | **17×** |
| 12 | Importar o TXT no Domínio **1 loja por vez** | Domínio | **17×** |
| 13 | Erro “código do empregado inválido”: abrir o TXT, achar a pessoa pelo ponto, corrigir e reimportar | Domínio ⇄ RP Info | quando ocorre |
| 14 | Salvar relatório **por loja** com subtotal por funcionário | RP Info | **17×** |
| 15 | Baixar o convênio (doc 3535) e os adiantamentos, invertendo até zerar | RP Info | mensal |

Retrabalhos 1 a 9: POP da folha. Retrabalhos 10 a 15: POP de fechamento do convênio.

### Os ~43 arquivos do mês

| Fluxo | Arquivo | Qtd. |
|---|---|---:|
| Folha | Relatórios Integração Contábil e Resumo Mensal (Excel) | 2 |
| Folha | Planilha Análise (conferência) | 1 |
| Folha | TXT da folha exportado do Domínio | 1 |
| Funcionários | `dfunc.txt`, base inteira de funcionários | 1 |
| Folha | Planilha de tratamento (8 consultas Power Query) | 1 |
| Folha | CSV para importar no RP Info | 1 |
| Pendências | Relatório de pendentes do mês | 1 |
| Pendências | TXT por loja para o Domínio | 17 |
| Pendências | Relatório de convênio por loja | 17 |
| Pendências | Relatório de adiantamentos (auditoria) | 1 |
| | **Total** | **43** |

O `Plano Gerencial RP.txt` também é lido pela planilha, mas não entra na conta porque não é
refeito todo mês.

### O que os arquivos mostram

- O arquivo importado no RP Info **não é igual** ao que a planilha gerou: uma coluna a mais, zeros
  perdidos e valores em formatos diferentes. **O RP Info aceitou mesmo assim**, ou seja, não há trava contra erro.
- O arquivo de agosto tem **95 lançamentos de setembro** (R$ 123 mil) misturados.
- A documentação do layout de pendências **não bate com o arquivo real** em 6 dos 8 campos.
- Há **3 pares de pessoas diferentes com o mesmo nome** no cadastro. Como a ligação é pelo nome,
  se uma delas entrar na folha o lançamento sai duplicado.

---

## Como vai ficar

```
   TOTVS RM  ◄─────────── API ───────────►  RP Info
             (confere, trava se houver erro, guarda histórico)
```

| Fluxo | Como era | Como vai ficar |
|---|---|---|
| **1. Folha** | Domínio → TXT → planilha → CSV → importação à mão | O RM fecha a folha e a integração confere e grava os lançamentos no RP Info por API |
| **2. Funcionários** | Base inteira baixada para pasta de rede, cruzada pelo nome | **Deixa de existir.** Consulta por CPF, só de quem está na folha |
| **3. Pendências** | 17 TXT gerados e importados no Domínio, um por loja | RP Info → RM por API, as 17 lojas numa execução |

### O que acontece com cada retrabalho

| # | Retrabalho de hoje | Como vai ficar |
|:---:|---|---|
| 1 | Rubrica nova configurada loja por loja | A integração detecta sozinha; a classificação é feita **uma vez**, no cadastro |
| 2 | Conferência no olho na planilha Análise | Conferência automática: débito = crédito, loja por loja |
| 3 | Baixar a base inteira de funcionários | **Deixa de existir**: consulta por CPF |
| 4 | Digitar código de quem tem nome divergente | **Deixa de existir**: identificação pelo CPF |
| 5 | Apagar o cabeçalho do CSV | **Deixa de existir**: não há arquivo |
| 6 | Conferir os totais na tela | A integração lê o que foi gravado e compara com o que enviou |
| 7–9 | Pós-importação (bancos, pensão, baixas) | Por API *(a depender do escopo contratado)* |
| 10 | Totalizar convênio, quebra de caixa e vale café | Feito pela integração ao ler as pendências *(a depender do RM receber os descontos via API)* |
| 11 | Gerar 17 TXT | **Deixa de existir**: 1 execução, sem arquivo |
| 12 | Importar 17× no Domínio | Lançado direto no RM por API *(a depender do RM receber os descontos via API)* |
| 13 | Corrigir erro e reimportar | O erro **trava antes do envio** e aparece com nome e motivo |
| 14 | Salvar 17 relatórios por loja | Histórico automático de cada envio, por loja |
| 15 | Baixar convênio e adiantamentos | Por API *(a depender do escopo contratado)* |

### O que continua com pessoas

- **Aprovar** o envio do mês.
- **Classificar uma rubrica nova**, uma única vez, no cadastro (hoje são até 17 configurações).
- **Manter as tabelas** que dizem “esta loja/conta do RM é aquela do RP Info”. Elas são montadas
  uma vez para o RM, junto com a Controladoria.

---

## Arquitetura da integração

Detalhe no diagrama [COMO_VAI_(API)](<COMO_VAI_(API).png>).

- **Servidor de Integração** dedicado, com API REST em `/api/v1`.
- **RP Info:** RP Services API v2.0.89 (REST, autenticação por token).
- **TOTVS RM:** wsDataServer (SOAP, usuário de serviço).

| Fluxo | Caminho do Servidor de Integração | Chamada | Situação |
|---|---|---|---|
| Acesso | cofre de credenciais | RP Info `POST /v1.2/auth` · usuário de serviço no RM | fluxo principal |
| Folha | `POST /eventos/rm/folha-fechada` | recebe o evento de folha fechada do RM | ❓ a depender do RM enviar o aviso de fechamento |
| Folha | `POST /folha/{competencia}/iniciar` | RM `/wsDataServer/IwsDataServer` · `ReadView` | fluxo principal |
| Folha | `POST /folha/{competencia}/validar` | usa os caminhos de funcionários e cadastros | fluxo principal |
| Folha | `POST /folha/{competencia}/aprovar` | — aprovação do responsável | fluxo principal |
| Folha | `POST /folha/{competencia}/enviar` | RP Info `POST /v1.0/fde` | ❓ a depender do RP Info aceitar a folha via API |
| Folha | `GET /folha/{competencia}/arquivo` | — gera o arquivo de importação pronto | ❓ contingência, a depender do RP Info não aceitar a folha via API |
| Folha | `GET /folha/{competencia}/conferencia` | RP Info `GET /v1.0/contabil/movimentos` | fluxo principal |
| Folha | `POST /folha/{competencia}/estornar` | RP Info `PUT /v1.0/documento/cancelar` | ❓ a depender do RP Info permitir cancelar o lote |
| Folha | `POST /folha/{competencia}/pos-importacao` | RP Info `POST /v2.0/financeiro/pendenciasFinanceiras/baixarPendenciaFin` | ❓ a depender do escopo contratado |
| Funcionários | `GET /colaboradores/{cpf}` | RP Info `GET /v1.2/funcionario/codcpf/{codcpf}` | fluxo principal |
| Funcionários | `POST /colaboradores` | RP Info `POST /v1.0/funcionario` | ❓ a depender da regra para colaborador novo: cadastrar ou bloquear |
| Cadastros | `GET · PUT /cadastros/de-para/{lojas\|contas}` | RP Info `GET /v1.1/financeiro/planocontas` | fluxo principal |
| Pendências | `POST /pendencias/{competencia}/sincronizar` | RP Info `GET /v1.6/financeiro/pendenciasFinanceiras` → RM `SaveRecord` · `FopLancExternoData` | ❓ a depender do RM receber os descontos via API |
| Pendências | `POST /pendencias/{competencia}/baixar` | RP Info `POST /v2.0/financeiro/pendenciasFinanceiras/baixarPendenciaFin` | ❓ a depender do escopo contratado |
| Auditoria | `GET /execucoes/{id}` · `GET /saude` | — histórico de cada execução | fluxo principal |

### Caminhos a depender de definição

Os caminhos marcados com ❓ dependem da definição indicada ao lado. O arquivo de contingência só entra
em uso se o RP Info não aceitar a folha via API, e mesmo assim continua sem planilha e sem digitação.
