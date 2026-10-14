# As perguntas que destravam o projeto
### Pauta da reunião · integração Folha → RP Info


## Sumário

- [Antes das perguntas](#antes-das-perguntas)
- [PARTE 1 — Negócio e processo](#parte-1-negócio-e-processo)
- [PARTE 2 — Sistemas e integração](#parte-2-sistemas-e-integração)
  - [2.1 · Para a RP Info (destino)](#21-para-a-rp-info-destino)
  - [2.2 · Para o implantador do RM (origem futura)](#22-para-o-implantador-do-rm-origem-futura)
- [Como conduzir](#como-conduzir)

---

> Extraído do [CONTRATO-DE-DADOS.md](CONTRATO-DE-DADOS.md) (79 perguntas).
> Estas são as que **mudam o desenho, o prazo ou o custo**. As outras são
> detalhamento — podem ser respondidas por e-mail depois.

**Estão separadas em duas partes, porque são duas conversas diferentes:**

| | Parte 1 | Parte 2 |
|---|---|---|
| **Quem responde** | Diretoria, Controladoria, RH/DP | TI, implantador do RM, suporte da RP Info |
| **Tipo de resposta** | uma **decisão** ou uma **política da empresa** | um **fato sobre um sistema** |
| **Quem pergunta** | qualquer um da equipe | precisa de alguém técnico na sala |
| **Quantas** | 9 | 8 |

**Podem ser feitas em reuniões separadas** — e provavelmente devem. A Parte 2
exige pessoas que muito provavelmente não estarão na primeira conversa.

---

## Antes das perguntas

Estas perguntas pressupõem o processo descrito em
**[ENTENDIMENTO-DO-PROCESSO.md](ENTENDIMENTO-DO-PROCESSO.md)** — os três fluxos
de hoje e o desenho futuro de cada um.

**Envie aquele documento antes da reunião.** Se o entendimento estiver errado,
metade destas perguntas muda. Em resumo:

| Fluxo | Hoje | Futuro |
|---|---|---|
| **1. Folha** | Domínio → planilha → RP Info | **TOTVS RM → API → RP Info** |
| **2. Base de funcionários** | download de 5.682 cadastros para pasta de rede | **desaparece** — consulta por CPF |
| **3. Pendências** | RP Info → arquivo → **Domínio** | RP Info → **?** → **RM** |

⚠️ **O fluxo 3 é o que o direcionamento não menciona** — ver pergunta **N6**.

---
---

# PARTE 1 — Negócio e processo

### Para quem conhece a operação
**Diretoria · Controladoria · RH / DP**

> Nenhuma destas exige conhecimento técnico. Todas pedem uma **decisão** ou a
> descrição de **como a empresa trabalha**.

| # | Pergunta | Quem responde |
|:---:|---|---|
| N1 | Qual a **data de virada** para o RM — e o prazo que vocês querem para a integração é antes ou depois dela? | Diretoria |
| N2 | O **trabalho que vem depois da importação** entra no escopo? | Controladoria |
| N3 | Quando aparece uma **rubrica nova** sem mapeamento, a carga **para e espera**, ou **segue e ajusta depois**? | Controladoria |
| N4 | Quando uma competência é **reprocessada**, o que se faz com o que **já foi importado**? | Controladoria / RH |
| N5 | Quem passa a ser o **dono das tabelas de correspondência**? E quem constrói a de contas? | Controladoria |
| N6 | As **pendências de convênio**, que hoje vão para o Domínio, passam a ir para o RM? | Diretoria / TI |
| N7 | O **CPF** dos colaboradores é confiável e igual nos dois sistemas? | RH / DP |
| N8 | Em que dia a folha **fecha** e os dados param de mudar? | RH / DP |
| N9 | Existe **relação formal com a RP Info** que dê acesso ao suporte técnico deles? | Diretoria |

### Detalhamento

**N1 · Qual a data de virada para o RM — e o prazo que vocês querem é antes ou depois dela?**
É a primeira porque determina se construímos **uma ponte ou duas**.
**Nossa recomendação é ligar direto no RM**, mesmo que isso signifique esperar. Construir a ponte a partir do sistema que está saindo significa refazer três tabelas de correspondência, repetir o ciclo de homologação e manter o export manual — porque **o sistema de origem atual não tem como entregar os dados sozinho**.
E para o "precisamos de algo agora", há três frentes que entregam valor imediato sem construir nada descartável — ver seção 6 da [recomendação de arquitetura](RECOMENDACAO-ARQUITETURA.md).
**Se a virada estiver longe ou sem data, a conversa muda de assunto** — e essa é a discussão que realmente destrava o projeto.

**N2 · O trabalho que vem depois da importação entra no escopo?**
Falamos de: agrupar os líquidos por banco, ajustar o portador da pensão com os dados bancários, baixar as pendências das contas totalizadoras e conferir se a conta zerou.
**É aproximadamente metade do trabalho manual de hoje.**
Há indício de que dá para automatizar — mas precisa entrar no escopo explicitamente, ou ficar de fora explicitamente. Deixar ambíguo é a forma mais rápida de o projeto ser considerado incompleto depois de entregue.

**N3 · Rubrica nova sem mapeamento: a carga para, ou segue?**
Hoje isso é descoberto por um relatório manual e configurado **loja a loja, 17 vezes**, com a instrução de não replicar para não desconfigurar.
No desenho novo, o sistema detecta sozinho. A pergunta é o que ele faz em seguida: **bloqueia tudo e avisa o que falta**, ou joga numa conta de trânsito e alguém acerta depois?
Não existe resposta certa — existe a resposta de vocês.

**N4 · Em reprocesso, o que se faz com o que já subiu?**
O procedimento atual manda sobrescrever os arquivos, mas não diz o que acontece com o que já foi importado.
Precisamos saber se **estorna, complementa ou convive** — porque isso define como o sistema novo se protege contra lançar a folha duas vezes.

**N5 · Quem é o dono das tabelas de correspondência?**
Hoje a correspondência entre as lojas dos dois sistemas está escrita **dentro do código de uma planilha**. Abrir uma loja nova exige mexer nesse código.
No desenho novo vira cadastro com tela e histórico — e alguém precisa ser o dono.
**Pergunta junto:** com a migração, **quem constrói a correspondência entre o plano de contas do RM e o do RP Info?** É o maior item de trabalho novo que a migração traz.
**E uma que pode reduzir isso pela metade:** o plano de contas **do RP Info** muda, ou permanece igual?

**N6 · As pendências passam a ir para o RM?**
Hoje esse arquivo é gerado **uma loja por vez**, por uma única pessoa autorizada, 17 vezes por mês, e enviado para o Domínio.
Se o Domínio sai do fluxo, essas pendências precisam passar a entrar no RM. **É uma integração inteira que o direcionamento não menciona** — precisamos saber se está no escopo.

**N7 · O CPF é confiável e igual nos dois sistemas?**
É a fundação de todo o desenho novo. Hoje os dois sistemas são conciliados **pelo nome** do colaborador — e por isso o processo tem uma etapa de correção de acentos e uma planilha onde alguém digita códigos à mão.
**O que já verificamos:** 100% dos 5.682 cadastros do RP Info têm CPF. Do lado deles, está pronto.
**O que sustenta a urgência:** encontramos **3 pares de pessoas diferentes com o mesmo nome** no cadastro. Nenhum apareceu na folha de agosto — mas se aparecer, o lançamento contábil duplica.

**N8 · Em que dia a folha fecha e os dados param de mudar?**
Hoje é uma pessoa que sabe. Para automatizar, precisa virar um momento definido — senão a carga automática lê dado ainda em movimento.
**Pergunta junto:** com que frequência há reprocesso, e o que costuma motivá-lo?

**N9 · Existe relação formal com a RP Info que dê acesso ao suporte técnico?**
A documentação deles diz que o acesso de integração precisa ser solicitado à empresa que fornece o serviço. **Sem isso, nada pode ser testado** — nem em ambiente de teste com dados de vocês.
É pergunta comercial, não técnica: **quem, do lado de vocês, autoriza?**

> **Se só houver tempo para três: N1, N2 e N6.**
> A primeira define a arquitetura. A segunda define o tamanho do projeto.
> A terceira revela um fluxo inteiro que ainda não tem destino.

---
---

# PARTE 2 — Sistemas e integração

### Para quem conhece as ferramentas
**TI · implantador do RM · suporte / parceria da RP Info**

> Estas são precisas de propósito. A resposta de cada uma é um **fato verificável
> sobre um sistema** — não uma opinião nem uma decisão.
> **Provavelmente exigem duas conversas separadas**, uma com cada fornecedor.

## 2.1 · Para a RP Info (destino)

| # | Pergunta |
|:---:|---|
| S1 | `POST /v1.0/fde` aceita um documento de folha — **sem chave de NFe, sem itens fiscais, com espécie própria**? Se não, **qual é o endpoint correto para carga contábil de folha?** |
| S2 | Existe **idempotência**? O `numeroRecibo` da resposta permite detectar reenvio do mesmo lote? Como se **estorna** uma carga inteira — `PUT /v1.0/documento/cancelar` serve? |
| S3 | Onde entra o **código do colaborador** dentro do `ContrapartidaFDE` — `subContas`, `cCustos`, ou exige um documento por colaborador? Qual o **limite de contrapartidas** e de tamanho de payload por documento? |
| S4 | Qual a **versão do RP One / Mix** instalada, e ela atende a API v2.0.89? Como se cria o **usuário de API** com as permissões necessárias? |

**Contexto para S1 — é a pergunta mais importante da Parte 2.**
O array `contrapartidas[]` é descrito na própria documentação do fornecedor como *"contrapartida/**lançamento contábil**"*, e tem **exatamente** os campos do arquivo importado hoje: `unidade`, `conta`, `valor`, `dc`, `historico`.
**A ressalva:** FDE significa *Fiscal Data Entry*. O objeto é modelado em torno de nota fiscal — modelo, série, chave de 44 caracteres, ICMS. **Folha de pagamento não é documento fiscal.**
*Se a resposta for não:* o sistema gera o arquivo, como hoje — mas por código testado — até indicarem o caminho certo.

**Contexto para S3:** hoje o código do colaborador existe **por linha** do arquivo. No objeto do fornecedor **não há campo para ele na contrapartida**; os campos de entidade são do documento inteiro. Dependendo da resposta, o volume vai de **17 chamadas para 7.853**.

**Perguntas menores, se houver tempo:**
- `pendencias[]` tem campo `portador` — isso substitui o agrupamento manual de líquidos por banco?
- `POST /v2.0/financeiro/pendenciasFinanceiras/baixarPendenciaFin` cobre a baixa das contas totalizadoras?
- `GET /v1.0/contabil/movimentos` permite conferir a carga logo após o envio?
- O ambiente de homologação pode ser usado com **dados reais do cliente**?
- **Alguém sabe o que é a 11ª coluna do arquivo importado hoje?**

## 2.2 · Para o implantador do RM (origem futura)

| # | Pergunta |
|:---:|---|
| S5 | O RM entrega a folha **já contabilizada** (conta, débito/crédito, valor) ou apenas as rubricas? A integração **Folha × Gestão Contábil (Saldus)** estará ativa? |
| S6 | Qual **DataServer / WebService** usar para **ler** os lançamentos contábeis da folha? **SOAP (`wsDataServer`) ou REST**? Como funciona a autenticação e qual usuário de serviço será criado? |
| S7 | Existe **status consultável de "lote de folha fechado"**, que sirva de gatilho para a extração? Como o RM trata **reabertura** de competência? |
| S8 | `FopLancExternoData` está **liberado para inclusão de eventos externos**? *(É o caminho das pendências no sentido inverso.)* |

**Contexto para S5:** o RM faz contabilização internamente, via Agrupamento de Contas Contábeis. Se a folha vier já contabilizada, a transformação simplifica muito — mas **o problema do de-para se muda para dentro do RM**, e passa a ser configuração de implantação, não desenvolvimento. Muda quem faz o trabalho.

**Perguntas menores, se houver tempo:**
- Estrutura de **coligada/filial** no RM × as 17 lojas.
- RM é **on-premise ou TOTVS Cloud**? Onde o serviço de integração pode rodar?
- Existe **ambiente de homologação** do RM com dados representativos?
- O CPF no RM é confiável e bate com o do RP Info? *(espelha N7)*

> **Se só houver tempo para duas: S1 e S5.**
> A primeira define se "API" é possível no lado da escrita.
> A segunda define quanto trabalho de transformação ainda existe.

---
---

# Como conduzir

**Ordem sugerida:**

1. **Abra pelo layout de pendências** — a documentação diverge do arquivo real em **6 dos 8 campos**. É verificável na hora, não é opinião, e mostra em 30 segundos que o trabalho já começou.
2. **Mostre a paridade** — 7.853 linhas geradas, 7.853 conferidas, **zero divergência**. Muda a conversa de *"vocês conseguem?"* para *"quando começamos?"*.
3. **Parte 1 inteira**, com quem estiver na sala.
4. **Agende a Parte 2** — são duas conversas, uma com cada fornecedor. Peça os contatos ao final da primeira reunião.

**Um cuidado:** as perguntas da Parte 2 **não devem ser feitas à mesa de negócio**. Ninguém de Controladoria tem obrigação de saber o que é um DataServer, e perguntar cria a impressão errada de que o projeto depende de vocês saberem — quando na verdade depende dos fornecedores responderem.

**E o contrário também:** as da Parte 1 não devem ir para os fornecedores. Nenhum deles decide se o pós-importação entra no escopo.

---

> **Sobre o formato:** toda pergunta da Parte 1 está escrita sem jargão, de
> propósito. Se alguma precisar ser explicada antes de ser respondida, ela está
> no lugar errado — avise que corrigimos.
