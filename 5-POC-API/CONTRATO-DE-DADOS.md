# Contrato de Dados e Roteiro de Esclarecimento
### Integração automatizada Folha → RP Info · Fase 0 (Descoberta)


## Sumário

- [Como ler este documento](#como-ler-este-documento)
- [PARTE 0 — A topologia](#parte-0-a-topologia)
  - [Hoje](#hoje)
  - [Futuro — o que o cliente pediu](#futuro-o-que-o-cliente-pediu)
- [PARTE 1 — O que já está provado](#parte-1-o-que-já-está-provado)
  - [1.1 Os três fornecedores](#11-os-três-fornecedores)
  - [1.2 A API da RP Info — o que foi confirmado na especificação](#12-a-api-da-rp-info-o-que-foi-confirmado-na-especificação)
  - [1.3 O TOTVS RM — o que foi confirmado](#13-o-totvs-rm-o-que-foi-confirmado)
  - [1.4 Volumetria e invariantes (competência 08/2026, base Domínio)](#14-volumetria-e-invariantes-competência-082026-base-domínio)
  - [1.5 As 11 regras de transformação](#15-as-11-regras-de-transformação)
  - [1.6 Layout de pendências (sentido inverso) — divergência confirmada](#16-layout-de-pendências-sentido-inverso-divergência-confirmada)
  - [1.7 O que o arquivo importado hoje revela](#17-o-que-o-arquivo-importado-hoje-revela)
- [PARTE 2 — Perguntas para a reunião](#parte-2-perguntas-para-a-reunião)
  - [Bloco Z — A migração para o RM](#bloco-z-a-migração-para-o-rm)
  - [Bloco R — RP Info (destino)](#bloco-r-rp-info-destino)
  - [Bloco T — TOTVS RM (origem futura)](#bloco-t-totvs-rm-origem-futura)
  - [Bloco B — Regras contábeis](#bloco-b-regras-contábeis)
  - [Bloco C — Identidade do colaborador](#bloco-c-identidade-do-colaborador)
  - [Bloco D — Processo e operação](#bloco-d-processo-e-operação)
  - [Bloco E — Pendências (sentido inverso)](#bloco-e-pendências-sentido-inverso)
  - [Bloco F — Pós-importação](#bloco-f-pós-importação)
  - [Bloco G — Governança, LGPD e comercial](#bloco-g-governança-lgpd-e-comercial)
- [PARTE 3 — Propostas](#parte-3-propostas)
- [PARTE 4 — O que já foi construído](#parte-4-o-que-já-foi-construído)
  - [O payload da API já foi gerado](#o-payload-da-api-já-foi-gerado)
- [PARTE 5 — O que muda conforme a resposta](#parte-5-o-que-muda-conforme-a-resposta)
- [PARTE 6 — Próximos passos](#parte-6-próximos-passos)
  - [Fontes consultadas](#fontes-consultadas)

---

**Versão:** 2.0 · **Base:** documentação do cliente + arquivos reais de 08/2026 + documentação pública dos três fornecedores
**Status:** documento de trabalho para a reunião de esclarecimento

> **O que mudou da v1.0 para a v2.0:** o cliente definiu o destino da migração —
> a origem deixa de ser o Domínio e passa a ser o **TOTVS RM**. Isso troca uma
> das duas pontas da ponte e traz um terceiro fornecedor para a conversa.
> Também investigamos a documentação pública dos três, e uma boa parte do que
> na v1.0 era pergunta hoje é resposta.

---

## Como ler este documento

| Marca | Significado |
|:---:|---|
| **✅ PROVADO** | Verificado nos arquivos ou na documentação pública do fornecedor. Não depende de confirmação. |
| **❓ EM ABERTO** | Ninguém nos disse, e não achamos. Precisa de resposta. |
| **💡 PROPOSTA** | Nossa recomendação. |

Onde não temos certeza, dizemos que não temos. Onde temos, mostramos a evidência.

---

# PARTE 0 — A topologia

## Hoje

```
  Domínio Sistemas                                        RP Info
   (folha/contábil)                                    (RP One / Mix)
         │                                                   ▲
         │  export TXT                                       │  CSV + Ctrl+D
         └──────────►  Planilha Excel  ────────────────────► │
                       8 consultas PQ                        │
                       operação manual                       │
                                                             │
        ◄──── TXT posicional de pendências (1 loja por vez) ──┘
```

## Futuro — o que o cliente pediu

```
     TOTVS RM                    API DE INTEGRAÇÃO                 RP Info
   (folha de pagto)          ┌────────────────────────┐        (RP One / Mix)
         │                   │  adaptador de origem   │              ▲
         ├──────────────────►│  regras + de-para      │──────────────┤
         │   wsDataServer    │  VALIDAÇÃO (trava)     │  POST /v1.0/fde
         │   / REST          │  trilha de auditoria   │              │
         │                   └────────────────────────┘              │
         ◄──────────────── pendências (sentido inverso) ─────────────┘
```

**A mudança de origem valida a decisão de arquitetura da v1.0.** O núcleo de
regras foi construído sem saber quem seria a origem. Trocar Domínio por RM
troca **um adaptador** — as 11 regras, as validações e a trilha permanecem.

> ❓ **A pergunta que precede todas as outras:** o RM já está implantado, ou a
> migração Domínio → RM é um projeto em andamento? **A resposta determina se
> construímos uma ponte ou duas.** Ver pergunta Z1.

## A terceira topologia — a que não se sustenta

Em algum momento do planejamento vai aparecer uma proposta intermediária:

```
  Domínio ──► API ──► RP Info        "e depois a gente troca para o RM"
```

⚠️ **Ela descreve algo que não existe.** ✅ O Domínio **não tem API de saída** —
a documentação da Thomson Reuters cobre envio de documentos fiscais e
lançamento de rubricas **para dentro** dele. Não há extração. Escrita com
honestidade, a topologia é:

```
  Domínio ──export manual──► nosso serviço ──API──► RP Info
           └── isto continua manual ──┘
```

**O gargalo que motiva o projeto permanece intacto.** Somam-se três de-paras
construídos sobre códigos que vão mudar, um ciclo extra de homologação em
paralelo, e a perda da janela em que o implantador do RM ainda está contratado.

📄 **Argumentação completa, com as seis objeções que virão e a resposta para
cada uma:** [RECOMENDACAO-ARQUITETURA.md](RECOMENDACAO-ARQUITETURA.md)

---

# PARTE 1 — O que já está provado

## 1.1 Os três fornecedores

| | Tem API? | Documentação | O que serve para este projeto |
|---|:---:|---|---|
| **RP Info** *(destino)* | ✅ **Sim** | OpenAPI 3.0.1 público, "RP Services" v2.0.89, **679 operações** | Escrita de lançamento, consulta por CPF, plano de contas, pendências |
| **TOTVS RM** *(origem futura)* | ✅ **Sim** | wsDataServer (SOAP) + REST, DataServers documentados | Leitura de folha, eventos e contabilização |
| **Domínio** *(origem atual)* | ⚠️ **Sim, mas só entrada** | Developer Portal Thomson Reuters | API de Rubricas — **recebe** dados, não exporta |

✅ **A API do Domínio é desenhada para enviar dados *para dentro* dele, não para extrair.** Isso é o argumento técnico que sustenta a decisão do cliente: **enquanto a origem for o Domínio, a extração continua sendo por arquivo.** Sair para o RM é o que destrava a automação da origem.

## 1.2 A API da RP Info — o que foi confirmado na especificação

✅ **Autenticação:** `POST /v1.2/auth` (usuário + senha) → token no header `token:` em todas as chamadas seguintes. Atributos `tokenExpiration`/`expiresIn` controlam validade. Sessão por cookie foi **descontinuada** na versão 3.0.0.01.

✅ **Existe ambiente de homologação documentado pelo próprio fornecedor:** `servicosflex.rpinfo.com.br:9000`.

✅ **A API atende RP One, Flex, Mix, Cxo e Mix-Integração** — o que também explica a confusão de nomes no POP: "MIX", "RP One" e "RP Info" são produtos da mesma casa, na mesma API.

### Endpoints que resolvem problemas identificados na v1.0

| Endpoint | Resolve |
|---|---|
| `GET /v1.2/funcionario/codcpf/{codcpf}` | **Conciliação por CPF.** Mata o dump `dfunc.txt` e a aba "Nomes Divergentes" |
| `GET /v1.1/financeiro/planocontas` · `GET /v1.0/financeiro/planocontabil` | Plano de contas por API — substitui o `Plano Gerencial RP.txt` |
| `GET /v1.0/contabil/movimentos` · `GET /v1.0/gerencial/movimentos` | **Conferência pós-carga automática** — substitui a conferência visual em tela |
| `GET /v1.1/financeiro/centrodecustos` | Centro de custos |
| `GET /v1.6/financeiro/pendenciasFinanceiras/...` | Leitura das pendências |
| `POST /v2.0/financeiro/pendenciasFinanceiras/baixarPendenciaFin` | **Baixa de pendências** — é o passo 6.6 do POP |
| `POST /v1.0/funcionario` · `PUT /v1.0/funcionario/{id}` | Cadastro de colaborador novo |

### O caminho de escrita do lançamento contábil

✅ **`POST /v1.0/fde`** recebe um objeto `DocumentoFDE` que contém:

| Array | Conteúdo | Corresponde a |
|---|---|---|
| `contrapartidas[]` | *"Contrapartida/lançamento contábil de um documento FDE"* | O arquivo CSV que se importa hoje |
| `pendencias[]` | inclui **`portador`** (banco) | O passo 6.5 do POP — "agrupar líquidos por banco" |

**O `ContrapartidaFDE` tem exatamente os campos do arquivo atual:**

| Coluna do CSV de hoje | Campo do `ContrapartidaFDE` |
|---|---|
| Cód. loja (`014`) | `unidade` |
| Conta (`331207`) | `conta` |
| Valor (`83.43`) | `valor` |
| `DB` / `CR` | `dc` (`D` / `C`) |
| Histórico | `historico` + `complemento` |
| Data | `dataMvto` *(no documento)* |

❓ **O que falta confirmar:** "FDE" significa *Fiscal Data Entry*. O objeto é modelado em torno de um **documento fiscal** (modelo, série, chave DFe de 44 caracteres, ICMS, fornecedor). **Folha de pagamento não é documento fiscal.** Ver perguntas R1–R5.

❓ **Lacuna concreta:** não existe, na especificação pública, campo para o **código do colaborador dentro da contrapartida**. Hoje esse código existe por **linha** (coluna 7 do CSV). No FDE, `catEntidade`/`codEntidade` são do **documento**. Ver R2.

## 1.3 O TOTVS RM — o que foi confirmado

✅ **Dois caminhos de integração:** `wsDataServer` (SOAP/XML) e API REST. Autenticação com usuário do próprio RM.

✅ **DataServers relevantes já documentados:**

| DataServer | Uso |
|---|---|
| `FopFuncData` | Cadastro de funcionários |
| `FopLancExternoData` | **Inclusão/edição de eventos e verbas por webservice** — é o caminho do sentido inverso (pendências), com camada extra de permissão recomendada pela TOTVS |
| WebService de lançamentos contábeis | Inclusão **e leitura** de lançamentos contábeis |

✅ **O RM já faz contabilização internamente.** O módulo de Folha integra com o Gestão Contábil (Saldus) por meio de **Agrupamento de Contas Contábeis** (`Encargos | Cadastros | Cadastros Contábeis | Agrupamentos de Contas`), e o lote de folha é transferido para o lote contábil por um processo próprio.

💡 **Consequência de desenho:** provavelmente a origem entregará **lançamentos já contabilizados**, não rubricas cruas. Isso simplifica o núcleo — mas **transfere o problema do de-para para dentro do RM**. Ver perguntas Z4 e B13.

## 1.4 Volumetria e invariantes (competência 08/2026, base Domínio)

> Números da origem **atual**. Servem de linha de base para conferir a origem nova.

| Medida | Valor |
|---|---|
| Lançamentos lidos | 6.849 |
| Pernas de crédito recuperadas (FGTS) | 1.004 |
| **Total processado** | **7.853** |
| Lojas com movimento | 17 |
| Colaboradores distintos | 1.078 |
| Cadastros na base do destino | 5.682 |
| Contas contábeis movimentadas | 23 |
| **Débito = Crédito** | **R$ 2.645.178,88** |

✅ **A partida dobrada fecha exatamente, e cada uma das 17 lojas fecha isoladamente, no centavo.**

| Loja | Lanç. | Débito | Crédito | Dif. |
|---|---:|---:|---:|---:|
| 001 | 474 | 162.660,83 | 162.660,83 | 0,00 |
| 002 | 426 | 130.930,33 | 130.930,33 | 0,00 |
| 003 | 629 | 207.119,73 | 207.119,73 | 0,00 |
| 004 | 321 | 98.236,37 | 98.236,37 | 0,00 |
| 005 | 475 | 148.879,12 | 148.879,12 | 0,00 |
| 006 | 401 | 122.458,09 | 122.458,09 | 0,00 |
| 007 | 539 | 176.483,31 | 176.483,31 | 0,00 |
| 008 | 459 | 169.120,84 | 169.120,84 | 0,00 |
| 010 | 535 | 221.279,73 | 221.279,73 | 0,00 |
| 011 | 253 | 92.663,64 | 92.663,64 | 0,00 |
| 012 | 326 | 101.283,02 | 101.283,02 | 0,00 |
| 013 | 578 | 194.984,64 | 194.984,64 | 0,00 |
| 014 | 527 | 169.429,99 | 169.429,99 | 0,00 |
| 015 | 443 | 134.555,00 | 134.555,00 | 0,00 |
| 016 | 428 | 137.345,09 | 137.345,09 | 0,00 |
| 018 | 483 | 82.363,65 | 82.363,65 | 0,00 |
| 031 | 556 | 295.385,50 | 295.385,50 | 0,00 |
| **TOTAL** | **7.853** | **2.645.178,88** | **2.645.178,88** | **0,00** |

✅ **100% dos 5.682 cadastros do destino possuem CPF.** Combinado com `GET /v1.2/funcionario/codcpf/{codcpf}`, **a conciliação por CPF é executável hoje** — não é aspiração.

## 1.5 As 11 regras de transformação

> Extraídas do código das 8 consultas Power Query embutidas no `.xlsx`. Não
> constavam em nenhum documento. **Estas regras sobrevivem à troca de origem** —
> o que muda é de onde os dados chegam.

| # | Regra | Sobrevive à migração? |
|---|---|:---:|
| R1 | Conta única: débito se ≠ 0, senão crédito | ✅ |
| R2 | Natureza `DB`/`CR` | ✅ |
| R3 | Valor em centavos ÷ 100 | ⚠️ depende do formato do RM |
| R4 | De-para de lojas (18 pares) | ⚠️ **refazer** com códigos do RM |
| R5 | Recuperação da perna de crédito do FGTS (1.004 linhas) | ⚠️ pode deixar de existir |
| R6 | Contas de terceiro → código fixo (`128384` Caixa) | ✅ |
| R7 | Conciliação de identidade | ✅ **melhora** — passa a ser por CPF |
| R8 | Fallback manual digitado | ✅ **deve desaparecer** |
| R9 | Classificação gerencial (conta → `NN`/`CP`/`TT`) | ⚠️ **refazer** com plano do RM |
| R10 | Remoção de acento (lista de 24 letras) | ✅ |
| R11 | Descarte silencioso de linha ilegível | ❌ **eliminar** |

**Três de-paras precisam ser reconstruídos para o RM: lojas, plano de contas e classificação gerencial.** É o principal item de esforço novo que a migração introduz. Ver Z4.

## 1.6 Layout de pendências (sentido inverso) — divergência confirmada

O layout documentado **não corresponde** ao arquivo real. Conferido contra as 86 linhas:

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
| **Tamanho** | **45** | **43** | **−2** |

✅ **Provado por teste de ida e volta:** as 86 linhas, lidas com o layout corrigido e reescritas, saem **idênticas ao original, byte a byte**.

💡 **Com a migração, esse arquivo posicional pode deixar de existir.** O destino das pendências passa a ser o RM, que expõe `FopLancExternoData` para inclusão de eventos por webservice. **Arquivo posicional → chamada de API.** Ver bloco E.

## 1.7 O que o arquivo importado hoje revela

O arquivo efetivamente importado **não é cópia fiel** do que a planilha produziu:

| Achado | Medida |
|---|---|
| Colunas | planilha tem **10**, arquivo importado tem **11** |
| 11ª coluna (valores `103,13`) | preenchida em **5.381 de 7.853** linhas — não existe na planilha |
| Zeros à esquerda da loja | perdidos: `001` → `1` |
| Valores sem 2 casas decimais | **1.793 de 7.853 (22,8%)** |
| Convenção decimal | ponto na coluna 5, vírgula na coluna 11 — mesmo arquivo |
| Cabeçalho | removido à mão após salvar |

✅ **O destino aceitou assim.** Não há validação de layout na entrada do arquivo. É a razão de o processo nunca ter estourado — e a razão de ele ser perigoso. **Pela API, com `dc` e `valor` tipados, esse problema deixa de existir por construção.**

---

# PARTE 2 — Perguntas para a reunião

> 🔴 **bloqueia o desenho** · 🟠 **muda o esforço** · 🟡 **pode esperar**

## Bloco Z — A migração para o RM
*Destinatário: Diretoria + TI · **responder antes de todo o resto***

| # | Pergunta | Pri. |
|---|---|:---:|
| Z1 | **O RM já está implantado e rodando folha, ou a migração Domínio → RM é um projeto em andamento?** Qual a data de virada? | 🔴 |
| Z2 | Se ainda não virou: **construímos a ponte a partir do Domínio agora e refazemos depois, ou esperamos o RM?** *(Recomendação nossa na Parte 3.)* | 🔴 |
| Z3 | Haverá período de convivência entre Domínio e RM? Alguma loja vira antes das outras? | 🔴 |
| Z4 | **Quem tem — ou vai construir — o de-para entre o plano de contas do RM e o plano de contas da RP Info?** *(Três de-paras precisam ser refeitos: lojas, plano contábil e classificação gerencial.)* | 🔴 |
| Z5 | O RM será o sistema de folha **de todas as 17 lojas**, ou apenas de parte? | 🟠 |
| Z6 | Quem é o implantador do RM? Está disponível para as conversas de integração? | 🟠 |
| Z7 | Com o RM, o escritório contábil externo sai do fluxo, ou continua recebendo alguma coisa? | 🟠 |

## Bloco R — RP Info (destino)
*Destinatário: suporte técnico / parceria RP Info*

| # | Pergunta | Pri. |
|---|---|:---:|
| R1 | **Um documento FDE pode ser criado com espécie/`codigoDocumento` de folha (o `3607` do POP), sem chave de NFe, sem itens fiscais e sem ICMS?** Se não, **qual é o endpoint correto para carga de folha?** | 🔴 |
| R2 | **Onde entra o código do colaborador?** Hoje ele existe por **linha**. No `ContrapartidaFDE` não há campo próprio; `catEntidade`/`codEntidade` são do documento. Vai em `subContas`, `cCustos`, ou exige 1 documento por colaborador? | 🔴 |
| R3 | **Granularidade:** 1 documento por competência, por loja, ou por colaborador? *(Muda de 1 para 7.853 chamadas — ver Parte 4.)* | 🔴 |
| R4 | Há limite de tamanho de payload ou de contrapartidas por documento? *(O maior documento por loja tem 629 contrapartidas, ~1 MB no total.)* | 🔴 |
| R5 | **Existe idempotência?** O `numeroRecibo` da resposta identifica o lote. **Reenviar o mesmo documento duplica ou é rejeitado?** | 🔴 |
| R6 | Como se **estorna** uma carga? `PUT /v1.0/documento/cancelar` serve para um lote de folha inteiro? | 🔴 |
| R7 | Qual a versão do RP One/Mix instalada no cliente, e ela atende a API v2.0.89? *(A documentação alerta que sessão por cookie foi descontinuada na 3.0.0.01.)* | 🔴 |
| R8 | Como se solicita o usuário de API com as permissões necessárias? *(A documentação diz que deve ser pedido "à empresa que disponibiliza o web service".)* | 🔴 |
| R9 | O ambiente de homologação `servicosflex.rpinfo.com.br:9000` pode ser usado com **dados do cliente**, ou só com a base de demonstração? | 🟠 |
| R10 | O endpoint de documentação responde com cadeia de certificado TLS incompleta. Há endereço oficial com certificado completo? | 🟡 |
| R11 | `POST /v1.0/fde` aceita `pendencias[]` com `portador` — **isso substitui o agrupamento manual de líquidos por banco** (POP 6.5)? | 🟠 |
| R12 | `POST /v2.0/financeiro/pendenciasFinanceiras/baixarPendenciaFin` cobre a baixa das contas totalizadoras (POP 6.6)? | 🟠 |
| R13 | `GET /v1.0/contabil/movimentos` permite conferir a carga logo após o envio, por competência e unidade? | 🟠 |
| R14 | **Alguém sabe o que é a 11ª coluna do arquivo importado hoje?** | 🟠 |

## Bloco T — TOTVS RM (origem futura)
*Destinatário: TI + implantador RM*

| # | Pergunta | Pri. |
|---|---|:---:|
| T1 | O RM exporta a folha **já contabilizada** (lançamentos com conta, D/C, valor) ou apenas as rubricas? | 🔴 |
| T2 | A integração Folha × Gestão Contábil (Saldus) estará **ativa**? É de lá que extraímos? | 🔴 |
| T3 | Qual DataServer/WebService usar para **ler** os lançamentos contábeis da folha? | 🔴 |
| T4 | wsDataServer (SOAP) ou API REST — qual a orientação do implantador? | 🔴 |
| T5 | Como funciona a autenticação e qual usuário de serviço será criado? | 🔴 |
| T6 | Existe ambiente de homologação do RM com dados representativos? | 🔴 |
| T7 | Qual a estrutura de **coligada/filial** no RM e como ela se relaciona com as 17 lojas? | 🔴 |
| T8 | O RM é on-premise ou TOTVS Cloud? Onde o serviço de integração pode rodar? | 🟠 |
| T9 | Em que momento do fechamento os lançamentos ficam **estáveis** para extração? Há status de "lote fechado"? | 🔴 |
| T10 | `FopLancExternoData` está liberado para inclusão de eventos externos? *(É o caminho do sentido inverso.)* | 🟠 |
| T11 | O CPF no RM é confiável e bate com o CPF cadastrado na RP Info? | 🔴 |
| T12 | Como o RM trata reprocesso/reabertura de competência? | 🟠 |

## Bloco B — Regras contábeis
*Destinatário: Controladoria*

| # | Pergunta | Pri. |
|---|---|:---:|
| B1 | **O arquivo de 08/2026 contém 95 lançamentos datados de setembro, R$ 123.215,95** (todos na loja 018). É esperado? Devem ir na mesma carga? | 🔴 |
| B2 | As contas `331207`/`211402` são as únicas que chegam com débito e crédito na mesma linha? **Esse comportamento vai existir no RM?** | 🔴 |
| B3 | A regra zera o débito para `331207` **e** `212401`, mas nenhuma linha usa `212401` nesse caso. Obsoleta ou cenário não ocorrido? | 🟠 |
| B4 | Além de Receita Federal (`211415`) e Caixa (`211402`/`331207`), **quais outras contas são de terceiro**? Sindicato, plano de saúde, pensão? | 🔴 |
| B5 | A conta `211415` está cadastrada com CNPJ mas sem código no destino. Intencional? | 🟠 |
| B6 | Qual a lista **completa e estável** de rubricas a ignorar? | 🔴 |
| B7 | Rubrica nova sem mapeamento: **bloqueia a carga** ou vai para conta de trânsito? | 🔴 |
| B8 | Quem decide o grupo de despesa de uma rubrica nova, e em quanto tempo? | 🟠 |
| B9 | "Eder Luis de Oliveira" deve ser excluído sempre? Por que consta no cadastro? **Existe equivalente no RM?** | 🟠 |
| B10 | Há tolerância de centavos na conferência, ou exigência de diferença zero? | 🟠 |
| B11 | Adiantamento, 13º, férias e rescisão entram na mesma carga ou em cargas separadas? | 🟠 |
| B12 | A loja `017` (origem `1181`) **não teve nenhum lançamento** nesta competência. Inativa, em abertura, ou erro de cadastro? | 🟡 |
| B13 | **O plano de contas da RP Info muda com a migração, ou permanece igual?** *(Se permanecer, metade do de-para é reaproveitada.)* | 🔴 |

## Bloco C — Identidade do colaborador
*Destinatário: RH / DP*

| # | Pergunta | Pri. |
|---|---|:---:|
| C1 | O CPF é confiável e idêntico nos dois sistemas? Há divergências conhecidas? | 🔴 |
| C2 | **Encontramos 3 pares de homônimos no cadastro do destino** — códigos `558`/`680`, `723`/`717`, `719`/`714`. Pessoas diferentes ou cadastros duplicados a unificar? *(Nenhum apareceu na folha de 08/2026 — mas a conciliação por nome duplicaria o lançamento se aparecessem.)* | 🔴 |
| C3 | O registro `2488` já foi filtrado como duplicado dentro do código da planilha. Foi corrigido na origem? | 🟠 |
| C4 | Colaborador na folha mas ainda não cadastrado no destino: **bloquear, ou criar via `POST /v1.0/funcionario`?** | 🔴 |
| C5 | O código `128384` (Caixa) é cadastro de fornecedor ou "funcionário" fictício no destino? | 🟠 |
| C6 | Colaborador que troca de loja no meio do mês: como atribuir o lançamento? | 🟠 |
| C7 | Mudança de nome: qual sistema é atualizado primeiro e por quem? | 🟡 |

## Bloco D — Processo e operação
*Destinatário: RH / DP*

| # | Pergunta | Pri. |
|---|---|:---:|
| D1 | Em que dia a folha fecha e a partir de quando os dados estão estáveis? | 🔴 |
| D2 | Com que frequência ocorre reprocesso, e o que o motiva? | 🔴 |
| D3 | Quando há reprocesso, **o que é feito com o que já foi importado** no destino? | 🔴 |
| D4 | Quem aprova a carga hoje? Quem **deve** aprovar depois? | 🟠 |
| D5 | Quem será o dono dos cadastros de de-para? | 🟠 |
| D6 | O processo roda uma vez por mês ou em etapas? | 🟠 |
| D7 | Quantas pessoas executam o processo de ponta a ponta hoje? | 🟠 |
| D8 | Há passo do POP que, na prática, não é mais executado? | 🟡 |

## Bloco E — Pendências (sentido inverso)

| # | Pergunta | Pri. |
|---|---|:---:|
| E1 | **Com o RM, as pendências passam a ser lançadas via `FopLancExternoData`, ou continuam por arquivo?** | 🔴 |
| E2 | **O layout documentado diverge do real em 6 dos 8 campos.** Qual é o oficial, e quem o mantém? *(Relevante mesmo na migração: é a referência do que o dado significa.)* | 🔴 |
| E3 | O que significam as máscaras fixas `10` e `11`? | 🟠 |
| E4 | "Número do ponto" é o mesmo "Código" da base do destino, ou outro identificador? | 🔴 |
| E5 | As rubricas `0065`, `0295` e `0452` são as únicas possíveis? **Como se chamam no RM?** | 🟠 |
| E6 | Por que o relatório é travado a **uma unidade por vez** — limitação ou parametrização? | 🟠 |
| E7 | Por que só o "usuário 11" tem acesso? Como liberar a outros? | 🟠 |
| E8 | Hoje há **confirmação de recebimento** do arquivo pela origem, ou o envio é cego? | 🔴 |
| E9 | Existe conferência de que o valor enviado bateu com o lançado na folha? | 🟠 |

## Bloco F — Pós-importação
*Destinatário: Controladoria + Financeiro*

| # | Pergunta | Pri. |
|---|---|:---:|
| F1 | **Esta etapa entra no escopo?** *(É cerca de metade do POP — e agora há evidência de que é automatizável: ver R11 e R12.)* | 🔴 |
| F2 | O agrupamento de líquidos por banco pode sair via `pendencias[].portador` do FDE? | 🟠 |
| F3 | A baixa das totalizadoras é sempre pelas mesmas 4 contas? | 🟠 |
| F4 | Portador e dados bancários da pensão seguem regra fixa ou decisão caso a caso? | 🟠 |
| F5 | Quanto tempo essa etapa consome hoje? | 🟡 |

## Bloco G — Governança, LGPD e comercial
*Destinatário: Diretoria*

| # | Pergunta | Pri. |
|---|---|:---:|
| G1 | Existe DPO? **O dump `dfunc.txt` em pasta de rede já foi avaliado sob a ótica da LGPD?** *(Com `GET /v1.2/funcionario/codcpf/{codcpf}`, ele pode ser eliminado já.)* | 🔴 |
| G2 | Qual o prazo desejado para a primeira competência pela nova ponte? **Ele é compatível com a data de virada do RM (Z1)?** | 🔴 |
| G3 | Quem sustenta a solução depois de entregue? | 🔴 |
| G4 | Existe orçamento aprovado, ou é estudo de viabilidade? | 🟠 |
| G5 | Há contrato/parceria formal com a RP Info que dê acesso ao suporte técnico de API? | 🔴 |
| G6 | Apetite para mudar o formato de entrada do destino (2 casas, zeros à esquerda)? *(Pela API, deixa de ser problema.)* | 🟡 |
| G7 | O `\\192.168.3.2` é de quem? Política de backup e acesso? | 🟡 |

---

# PARTE 3 — Propostas

💡 **P1 — Ir direto para RM → API → RP Info. Não construir a ponte a partir do Domínio.**

> ⚠️ **Esta proposta substitui a P1 da versão 1.0**, que recomendava o contrário
> — construir sobre o Domínio e trocar o adaptador depois. A mudança se deve à
> definição da direção estratégica, que não tínhamos quando aquela foi escrita.

O motivo determinante: ✅ **o Domínio não tem API de saída.** A documentação da Thomson Reuters descreve envio de documentos fiscais e lançamento de rubricas **para dentro** do Domínio. Não há extração. Logo, a topologia "Domínio → API → RP Info" mantém o export manual — **o gargalo que motiva o projeto permanece intacto.**

Somam-se a isso: três de-paras construídos sobre códigos que vão mudar, um ciclo extra de homologação em paralelo, regras que nascem mortas (a recuperação do FGTS é peculiaridade do export do Domínio), e a perda da janela em que o implantador do RM ainda está contratado.

**Argumentação completa, com as objeções e as respostas:** [RECOMENDACAO-ARQUITETURA.md](RECOMENDACAO-ARQUITETURA.md)

💡 **P2 — Conciliação por CPF, imediatamente.** `GET /v1.2/funcionario/codcpf/{codcpf}` já existe. Cascata `CPF → PIS → matrícula → nome`, com nome apenas como último recurso e aprovação humana registrada.

💡 **P3 — Eliminar o `dfunc.txt` já nesta fase.** É o item de LGPD mais exposto e o de solução mais barata: uma consulta por CPF substitui um dump de 76 campos × 5.682 pessoas.

💡 **P4 — Cadastro no lugar de código.** De-paras de loja, conta, classificação gerencial, contas de terceiro e exceções saem do código e viram tabela com tela e histórico. **Com a migração isso deixa de ser boa prática e vira necessidade** — os três de-paras serão refeitos para o RM.

💡 **P5 — Validação que bloqueia, não que avisa.** Partida dobrada, fechamento por loja, cobertura de rubricas, identidade resolvida, zero linhas descartadas. *As duas primeiras já fecham hoje: a trava não atrapalha operação legítima.*

💡 **P6 — Nada é descartado em silêncio.** Toda linha não processável bloqueia a carga e aparece nomeada.

💡 **P7 — Idempotência na entrega.** Chave `competência + loja + hash do lote`, casada com o `numeroRecibo` devolvido pela API. *Condicionado a R5.*

💡 **P8 — Conferência automática pós-carga.** Após o envio, ler `GET /v1.0/contabil/movimentos` e confrontar com o que foi enviado. **Substitui a conferência visual em tela por uma asserção.**

💡 **P9 — Trilha por competência.** Origem + hash, versão das regras, contagens, totais, quem aprovou, `numeroRecibo` por lote.

💡 **P10 — Paridade antes de corte.** Roda em paralelo por 1–2 competências; só vira oficial quando bater linha a linha. **Já feito para 08/2026 — ver Parte 4.**

---

# PARTE 4 — O que já foi construído

Antes desta reunião, as regras foram reescritas em código e executadas sobre os arquivos reais.

| Verificação | Resultado |
|---|---|
| Linhas geradas | 7.853 |
| Linhas na planilha atual | 7.853 |
| Divergências | **0** |
| Partida dobrada | R$ 2.645.178,88 = R$ 2.645.178,88 |
| Layout de pendências (ida e volta) | 86/86 linhas idênticas |

**Paridade total.** E, na mesma execução, 4 situações que o processo atual não enxerga:

| Alerta | Medida |
|---|---|
| Homônimos latentes no cadastro | 3 pares |
| Histórico com caractere fora do ASCII (`º`) | 63 lançamentos |
| Códigos resolvidos por digitação manual | 6 lançamentos |
| Competência misturada no mesmo arquivo | 95 lançamentos de 09/2026, R$ 123.215,95 |

## O payload da API já foi gerado

O mesmo lote foi convertido em `DocumentoFDE` nas três granularidades possíveis. **Nenhuma chamada de rede foi feita** — apenas geração e validação local.

| Estratégia | Documentos | Contrapartidas | Maior documento | JSON |
|---|---:|---:|---:|---:|
| 1 por competência | 1 | 7.853 | 7.853 | ~1 MB |
| **1 por loja** | **17** | **7.853** | **629** | **~1 MB** |
| 1 por loja e data | 86 | 7.853 | 574 | ~1 MB |

Nas três, o payload **preserva as 7.853 linhas e fecha em partida dobrada**.
A escolha depende da resposta R3.

---

# PARTE 5 — O que muda conforme a resposta

| Se… | Então… |
|---|---|
| **RM já rodando** | Adaptador de origem RM direto. Ponte única. |
| **RM ainda não virou** | Recomendação P1: construir sobre o Domínio e trocar o adaptador na virada. |
| `POST /v1.0/fde` **aceitar** folha (R1) | Entrega 100% por API. Arquivo CSV morre. |
| `POST /v1.0/fde` **não aceitar** (R1) | Adaptador gera o arquivo — mesmo resultado de hoje, por código testado — até a RP Info indicar o endpoint correto. |
| **Houver idempotência** (R5) | Reprocesso seguro, automático. |
| **Não houver** (R5) | Controle de duplicidade do nosso lado + estorno manual documentado. |
| **Plano de contas mudar** no RM (B13) | +1 frente: reconstrução dos três de-paras com a Controladoria. |
| **R11/R12 confirmarem** | Fase 4 (pós-importação) passa de "talvez" para viável. |

---

# PARTE 6 — Próximos passos

1. **Responder o Bloco Z.** Sem a data de virada do RM, qualquer cronograma é ficção.
2. **Reunião técnica com a RP Info** sobre R1–R8. É a conversa de maior valor: destrava a ponta de escrita.
3. **Reunião técnica com o implantador do RM** sobre T1–T7.
4. **Acesso aos ambientes de homologação** dos dois lados, com usuário de API.
5. **Amostras de mais 2 competências**, incluindo uma com 13º ou férias.
6. **Fechamento deste contrato de dados** com as respostas.
7. **Estimativa firme** de prazo e custo.

> Enquanto 1 a 6 não acontecem, o núcleo de transformação continua evoluindo:
> ele não depende de nenhuma decisão de canal. Foi construído assim de propósito
> — e a troca de origem, que ninguém tinha anunciado quando ele foi escrito,
> acabou de provar que valeu a pena.

---

## Fontes consultadas

- [RP Info — site oficial](https://www.rpinfo.com.br/) · [Produto RP One](https://www.rpinfo.com.br/produto/rp-one/56)
- [RP Services — especificação OpenAPI 3.0.1 v2.0.89](https://servicosflex.rpinfo.com.br:7443/v1.0/documentacao?location=documentacao)
- [Domínio Sistemas — Integração com ERP](https://www.dominiosistemas.com.br/solucoes/integracao-com-erp/) · [Central do Desenvolvedor / API](https://www.dominiosistemas.com.br/lp-centraldodesenvolvedor-api/) · [Thomson Reuters Developer Portal](https://developerportal.thomsonreuters.com/onvio-br-accounting-api/documents/documentao-api)
- [TOTVS — Inclusão e leitura de lançamentos contábeis (RM)](https://tdn.totvs.com/pages/releaseview.action?pageId=440839794) · [Webservices/API do TOTVS Folha de Pagamento](https://centraldeatendimento.totvs.com/hc/pt-br/articles/8558471418135-RH-RM-FOP-Webservices-API-dispon%C3%ADveis-no-TOTVS-Folha-de-Pagamento) · [Lançamento de eventos via DataServer/API](https://centraldeatendimento.totvs.com/hc/pt-br/articles/39228619469847-RH-RM-FOP-Como-realizar-o-lan%C3%A7amento-de-eventos-verbas-para-o-envelope-de-pagamento-via-DataServer-ou-API) · [Utilização de DataServers RM WebServices](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360051030334-RM-SAU-Utiliza%C3%A7%C3%A3o-de-DataServers-RM-WebServices)
