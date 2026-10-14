# Entendimento do Processo — como é hoje, como fica depois
### Integração Folha → RP Info


## Sumário

- [1. Hoje existem TRÊS movimentos de dados, não um](#1-hoje-existem-três-movimentos-de-dados-não-um)
- [2. Fluxo 1 — Folha de pagamento](#2-fluxo-1-folha-de-pagamento)
  - [2.1 Como é hoje](#21-como-é-hoje)
  - [2.2 Volumetria conferida (08/2026)](#22-volumetria-conferida-082026)
  - [2.3 Como fica depois](#23-como-fica-depois)
- [3. Fluxo 2 — Base de funcionários](#3-fluxo-2-base-de-funcionários)
  - [3.1 Como é hoje](#31-como-é-hoje)
  - [3.2 Como fica depois](#32-como-fica-depois)
- [4. Fluxo 3 — Pendências de convênio](#4-fluxo-3-pendências-de-convênio)
  - [4.1 Como é hoje](#41-como-é-hoje)
  - [4.2 O layout — divergência confirmada](#42-o-layout-divergência-confirmada)
  - [4.3 Como fica depois](#43-como-fica-depois)
- [5. O que sobrevive, o que muda, o que desaparece](#5-o-que-sobrevive-o-que-muda-o-que-desaparece)
- [6. O que ainda não está decidido](#6-o-que-ainda-não-está-decidido)
- [7. O que pedimos que vocês confirmem](#7-o-que-pedimos-que-vocês-confirmem)

---

**Propósito deste documento:** registrar o que entendemos do processo atual e do
desenho futuro, **para que vocês confirmem ou corrijam antes da reunião**.

Tudo aqui foi reconstruído a partir da documentação entregue e dos arquivos
reais da competência **08/2026**. Onde reconstruímos, mostramos a evidência.
Onde não sabemos, está marcado.

| Marca | Significado |
|:---:|---|
| **✅** | Verificado nos arquivos. Se estiver errado, o erro é nosso — queremos saber. |
| **❓ CONFIRMAR** | Nossa leitura. Precisa do aceite de vocês. |
| **⚠️ NÃO SABEMOS** | A documentação não diz, e não conseguimos deduzir. |

---

# 1. Hoje existem TRÊS movimentos de dados, não um

A conversa costuma girar em torno de "sair do Domínio e entrar no RP Info".
Esse é o fluxo principal — mas há outros dois pendurados nele, e os três
precisam de destino no desenho novo.

```
  ┌── FLUXO 1 · FOLHA ─────────────────────────────────────────────────┐
  │                                                                    │
  │   Domínio ──export TXT──► planilha Excel ──CSV──► RP Info          │
  │                              ▲                                     │
  └──────────────────────────────┼─────────────────────────────────────┘
                                 │
  ┌── FLUXO 2 · BASE DE FUNCIONÁRIOS (alimenta o fluxo 1) ─────────────┐
  │                                                                    │
  │   RP Info ──download dfunc.txt──► pasta de rede ──────────────┘    │
  │                                                                    │
  └────────────────────────────────────────────────────────────────────┘
  ┌── FLUXO 3 · PENDÊNCIAS DE CONVÊNIO (sentido inverso) ──────────────┐
  │                                                                    │
  │   RP Info ──TXT posicional, 1 loja por vez──► Domínio              │
  │                                                                    │
  └────────────────────────────────────────────────────────────────────┘
```

---

# 2. Fluxo 1 — Folha de pagamento

## 2.1 Como é hoje

**Periodicidade:** mensal · **Janela:** D+4 do fechamento contábil, limite no 5º dia útil

### Etapa A — Preparar (antes de qualquer extração)

1. Fechar a folha no Domínio.
2. Rodar relatório para descobrir **rubricas novas**, selecionando todas as lojas **exceto** a primeira linha ("Eder Luis de Oliveira").
3. Configurar cada rubrica nova **loja a loja** — *"tratar cada loja individual, não replicar para não desconfigurar"*.
4. Desconsiderar rubricas Informativas, INSS e FGTS de Rescisão, Adiantamento de 13º e a rubrica 980.

✅ **Com 17 lojas, uma rubrica nova significa 17 configurações manuais.**

### Etapa B — Extrair e conferir

5. Gerar no Domínio os relatórios **Integração Contábil** e **Resumo Mensal**, salvar em Excel sobrescrevendo os arquivos da pasta.
6. Atualizar a planilha **Análise** e conferir os valores visualmente.
7. Desmarcar o que for FGTS e ver se bate com a aba RESUMO.

✅ **O arquivo de origem:** CSV com vírgula, encoding CP-1252, 9 campos, valor em centavos sem separador (`000000000231550` = R$ 2.315,50). **6.849 linhas de dado** em 08/2026.

### Etapa C — Transformar

8. Baixar a base de funcionários do RP Info e sobrescrever o `dfunc.txt` *(este é o Fluxo 2 — ver seção 3)*.
9. Abrir a planilha de tratamento → **Dados → Atualizar Tudo** → habilitar conteúdo.
10. Conferir a aba de **nomes divergentes** e, onde houver, copiar o nome do Domínio e **digitar o código do funcionário à mão**.

✅ **A planilha contém 8 consultas Power Query**, que leem arquivos de `\\192.168.3.2\rh\Controller\01-Importação Folha\00-Banco de Dados\`. **É aí que mora a regra de negócio da empresa** — não no POP.

✅ **Onze regras de transformação** foram extraídas desse código. A mais delicada: linhas de FGTS chegam com débito **e** crédito na mesma linha; a leitura direta perderia **1.004 créditos** e quebraria a partida dobrada. A planilha resolve relendo o arquivo inteiro numa segunda consulta.

### Etapa D — Gerar o arquivo e importar

11. Salvar como **CSV UTF-8** na pasta "01-Histórico de Cargas (TXT)".
12. Reabrir o arquivo e **apagar o cabeçalho à mão**.
13. Importar no RP Info em **Lançar documentos (Ctrl+D)**, com a data do **último dia do mês** da competência.
14. Conferir os totais na tela contra a planilha Análise.

✅ **7.853 linhas** no arquivo final (6.849 + 1.004 créditos de FGTS recuperados).

### Etapa E — Pós-importação (tudo manual)

15. Agrupar os líquidos por banco: documento **3607**, conta **211301** (F12), incluindo uma pendência por banco.
16. Pensão: alterar o **portador** conforme o banco pagador e digitar os dados bancários na observação.
17. Baixar pendências das **contas totalizadoras**: adiantamento de férias, rescisão contratual, plano de saúde e sindicatos.
18. Conferir, com **F5**, que a conta totalizadora ficou zerada.

✅ **A Etapa E é aproximadamente metade do POP.**

## 2.2 Volumetria conferida (08/2026)

| Medida | Valor |
|---|---|
| Lançamentos lidos da origem | 6.849 |
| Créditos de FGTS recuperados | 1.004 |
| **Total importado** | **7.853** |
| Lojas com movimento | 17 |
| Colaboradores distintos | 1.078 |
| Contas contábeis | 23 |
| **Débito = Crédito** | **R$ 2.645.178,88** |

✅ **A partida dobrada fecha exatamente, e cada uma das 17 lojas fecha isoladamente, no centavo.**

## 2.3 Como fica depois

```
   TOTVS RM  ──► serviço de integração ──►  RP Info
                 ├─ adaptador de origem (RM)
                 ├─ regras + de-para (cadastro)
                 ├─ VALIDAÇÃO que bloqueia
                 ├─ trilha de auditoria
                 └─ adaptador de destino (API)
```

| Etapa de hoje | Depois |
|---|---|
| A · Rubricas novas, 17× manual | Detecção automática; **carga bloqueada** com a lista do que falta mapear |
| B · Extrair e conferir visualmente | Extração por API; conferência vira **asserção automática** |
| C · Planilha com 8 consultas | Regras em código versionado, com teste de regressão |
| C · Digitar código à mão | **Deixa de existir** — conciliação por CPF |
| D · Salvar CSV, apagar cabeçalho | **Deixa de existir** — entrega por API |
| E · Pós-importação manual | ❓ **Depende do escopo** — ver seção 6 |

❓ **CONFIRMAR:** o RM passa a ser o sistema de folha das **17 lojas**, ou de parte delas?

⚠️ **NÃO SABEMOS:** se o RM entregará a folha **já contabilizada** (lançamentos com conta, débito/crédito e valor) ou apenas as rubricas. Isso muda quanto da transformação continua necessária.

---

# 3. Fluxo 2 — Base de funcionários

## 3.1 Como é hoje

O POP instrui: *"fazer download da base de funcionários do MIX e substituir o arquivo txt `dfunc`"*.

✅ **O que esse arquivo contém:** **5.682 cadastros × 76 campos**, incluindo **CPF, PIS, RG, nome do pai e da mãe, endereço, salário contratual e banco/agência/conta**.

✅ **Onde ele fica:** `\\192.168.3.2\rh\Controller\01-Importação Folha\00-Banco de Dados\dfunc.txt`, sobrescrito todo mês.

✅ **Para que ele serve:** um único propósito — descobrir o **código do colaborador no RP Info** a partir do **nome** que veio do Domínio.

**O problema:** nome não é identificador. Por isso o processo tem uma etapa de correção de acentos e letras duplicadas, uma aba de nomes divergentes e uma tabela de códigos digitados à mão.

✅ **Três pares de homônimos no cadastro** — códigos `558`/`680`, `723`/`717`, `719`/`714`. Nenhum apareceu na folha de 08/2026, mas se aparecerem, o lançamento contábil **duplica**.

✅ **100% dos 5.682 cadastros têm CPF preenchido.** A chave correta já existe e não está sendo usada.

## 3.2 Como fica depois

**Este fluxo desaparece.**

A API do RP Info oferece `GET /v1.2/funcionario/codcpf/{codcpf}` — consulta de colaborador por CPF. Uma consulta pontual substitui o download mensal de 5.682 cadastros com 76 campos.

| | Hoje | Depois |
|---|---|---|
| Chave | Nome (texto) | **CPF** |
| Dado trafegado | Base completa, 76 campos | Só o CPF consultado |
| Onde repousa | Pasta de rede, sobrescrita | Em lugar nenhum |
| Falha de conciliação | Digitação manual | Bloqueia a carga |

✅ **É o ganho de LGPD mais barato do projeto** e não depende da migração para o RM — pode ser feito já.

❓ **CONFIRMAR:** o CPF cadastrado no RM será o mesmo cadastrado no RP Info?

---

# 4. Fluxo 3 — Pendências de convênio

> **Este é o fluxo que o direcionamento não menciona.**

## 4.1 Como é hoje

1. Acessar o relatório no sistema; ele pede **data** e depois **unidade**.
2. ✅ *"Mesmo que na tela das unidades selecione mais de uma, o relatório não irá gerar, porque o mesmo está travado a ser feito uma unidade por vez."*
3. ✅ *"Esse relatório está liberado para o usuário 11."*
4. Gerar o TXT e enviar para o Domínio, onde entra como rubrica na folha.

✅ **Com 17 lojas, são 17 arquivos gerados manualmente, todo mês, por uma pessoa. Sem redundância.**

## 4.2 O layout — divergência confirmada

O layout documentado **não corresponde** ao arquivo real. Conferido contra as 86 linhas do arquivo de exemplo:

| Campo | Documentação | Arquivo real | Desvio |
|---|---:|---:|---:|
| Máscara (fixo `10`) | 1–2 | 1–2 | — |
| Número do ponto | 3–12 | 3–12 | — |
| Ano | 14–17 | **13–16** | +1 |
| Mês | 19–20 | **17–18** | +2 |
| Rubrica | 21–24 | **19–22** | +2 |
| Máscara (fixo `11`) | 25–26 | **23–24** | +2 |
| Valor | 27–35 | **25–33** | +2 |
| Código da loja | 36–45 | **34–43** | +2 |
| **Tamanho total** | **45** | **43** | **−2** |

✅ **O layout real está provado:** lendo as 86 linhas com as posições corrigidas e reescrevendo-as, as 86 saem **idênticas ao original, byte a byte**.

✅ **Conteúdo do arquivo de exemplo:** competência `08/2026`, loja `762`, 43 pontos distintos, rubricas `0065` (14), `0295` (32), `0452` (40), total **R$ 11.906,03**.

⚠️ **NÃO SABEMOS:** como o arquivo chega ao Domínio (e-mail, pasta, portal, SFTP), nem se há confirmação de recebimento ou retorno de erro.

## 4.3 Como fica depois

⚠️ **Se o Domínio sai do fluxo, as pendências precisam passar a entrar no RM.**

Não é detalhe: é uma integração inteira. E há boa notícia — o RM expõe o DataServer `FopLancExternoData` para inclusão de eventos e verbas por webservice.

| | Hoje | Depois |
|---|---|---|
| Destino | Domínio | **TOTVS RM** |
| Formato | TXT posicional, 43 posições | Chamada de API |
| Granularidade | **1 loja por vez** | 17 lojas numa execução |
| Acesso | Um único usuário autorizado | Serviço, com trilha |
| Confirmação | ⚠️ desconhecida | Retorno da API |

❓ **CONFIRMAR:** é isso mesmo — as pendências passam a ir para o RM?

---

# 5. O que sobrevive, o que muda, o que desaparece

| | Situação |
|---|---|
| **Sobrevive** | As 11 regras de transformação, as validações de partida dobrada e fechamento por loja, o conceito de contas de terceiro (Receita Federal, Caixa), a remoção de acentos |
| **Muda** | Três de-paras precisam ser **refeitos** para o RM: lojas (coligada/filial ↔ unidade), plano de contas, e classificação gerencial (`NN`/`CP`/`TT`) |
| **Desaparece** | O download do `dfunc.txt`, a conciliação por nome, a digitação manual de códigos, o CSV, a remoção manual do cabeçalho, o descarte silencioso de linhas |

✅ **A reconstrução dos três de-paras é o maior item de esforço novo que a migração introduz.**

❓ **CONFIRMAR — e esta pode reduzir o trabalho pela metade:** o plano de contas **do RP Info** muda com a migração, ou permanece igual? Se permanecer, um dos três de-paras é reaproveitado inteiro.

---

# 6. O que ainda não está decidido

| Tema | Situação |
|---|---|
| **Data de virada do RM** | ⚠️ Não sabemos se o RM já roda folha ou se a migração está em andamento. **Determina se construímos uma ponte ou duas.** |
| **Escrita por API no RP Info** | A API tem `POST /v1.0/fde`, cujo array `contrapartidas[]` o fornecedor descreve como *"lançamento contábil"* e tem exatamente os campos do arquivo atual. **Mas FDE significa *Fiscal Data Entry*, e folha não é documento fiscal.** Precisa de confirmação do fornecedor. |
| **Pós-importação (Etapa E)** | ❓ Entra no escopo? Há indício de que é automatizável: o documento tem `pendencias[]` com campo `portador` (banco), e existe endpoint de baixa de pendências. |
| **Reprocesso** | ⚠️ Não sabemos o que se faz hoje com o que já foi importado quando há reprocesso. |

---

# 7. O que pedimos que vocês confirmem

1. Os **três fluxos** da seção 1 estão corretos e completos? Falta algum?
2. O **Fluxo 3** (pendências) passa a ir para o **RM**? — seção 4.3
3. O RM será a folha das **17 lojas**? — seção 2.3
4. O **plano de contas do RP Info** muda com a migração? — seção 5
5. O **CPF** do RM baterá com o do RP Info? — seção 3.2
6. A **Etapa E** (pós-importação) entra no escopo? — seção 2.1
7. Algum passo do processo atual descrito aqui **já não é mais executado**?

---

> **Sobre o que está escrito aqui:** nenhuma afirmação marcada com ✅ é opinião.
> Todas foram conferidas contra os arquivos de 08/2026 e podem ser reproduzidas.
> Se alguma estiver errada, é a informação mais útil que vocês podem nos dar.

**Perguntas para a reunião:** [PERGUNTAS-PRIORITARIAS.md](PERGUNTAS-PRIORITARIAS.md) (as 14 principais) · [CONTRATO-DE-DADOS.md](CONTRATO-DE-DADOS.md) (as 79, com evidências e propostas)
