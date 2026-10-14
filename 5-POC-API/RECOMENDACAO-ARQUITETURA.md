# Recomendação de arquitetura: começar pelo RM
### Por que o caminho pelo Domínio custa mais caro do que parece

---

## Sumário

- [0. Resumo em uma página](#0-resumo-em-uma-página)
- [1. A proposta que vai aparecer](#1-a-proposta-que-vai-aparecer)
  - [1.1 O problema começa no nome](#11-o-problema-começa-no-nome)
- [2. O que sobrevive e o que é descartável](#2-o-que-sobrevive-e-o-que-é-descartável)
- [3. Os seis argumentos](#3-os-seis-argumentos)
- [4. As objeções que virão — e a resposta para cada](#4-as-objeções-que-virão--e-a-resposta-para-cada)
- [5. Quando o caminho pelo Domínio seria a decisão certa](#5-quando-o-caminho-pelo-domínio-seria-a-decisão-certa)
- [6. O que fazer agora, independentemente da decisão](#6-o-que-fazer-agora-independentemente-da-decisão)
- [7. A recomendação](#7-a-recomendação)

---

## 0. Resumo em uma página

Existem duas topologias possíveis, e elas não custam o mesmo:

```
  OPÇÃO A — provisória              OPÇÃO B — definitiva
  ────────────────────              ────────────────────
  Domínio ─┐                        TOTVS RM ─┐
           │ arquivo                          │ API
           ▼                                  ▼
      nosso serviço                      nosso serviço
           │ API                              │ API
           ▼                                  ▼
       RP Info                            RP Info

  Depois: refazer                    Uma vez só
```

**A Opção A é frequentemente apresentada como "mais rápida".** Ela é — para a
primeira entrega. Mas ela exige construir **duas vezes** a parte mais cara do
projeto, e cria um risco que não aparece no cronograma: **a ponte provisória
vira definitiva**, e a migração para o RM perde a urgência que a justificava.

**Recomendação:** ir direto para a Opção B, e resolver **agora**, em paralelo,
os dois problemas que não dependem da origem — a exposição de dados pessoais e
a conciliação por nome. São semanas de trabalho, não meses, e o ganho é imediato.

> ⚠️ **Esta recomendação substitui a proposta P1 da versão 1.0 do contrato de
> dados**, que sugeria construir sobre o Domínio e trocar o adaptador depois.
> A mudança se deve à definição da direção estratégica, que não tínhamos quando
> aquela proposta foi escrita.

---

## 1. A proposta que vai aparecer

Em algum momento do planejamento, alguém vai propor:

> *"Vamos fazer Domínio → API → RP Info agora, e depois trocamos para o RM."*

Soa razoável. Aproveita o que já existe, entrega valor antes, não depende da
migração. **O problema é que ela descreve algo que não existe.**

### 1.1 O problema começa no nome

✅ **O Domínio não tem API de saída.**

A documentação da Thomson Reuters é explícita: as APIs do Domínio servem para
**enviar dados para dentro dele** — documentos fiscais (NF-e, NFC-e, NFS-e,
CT-e), baixa de parcelas, e a API de Rubricas, que *"permite o lançamento de
rubricas no módulo Folha"*.

**Não há extração.** Nenhum endpoint devolve a folha contabilizada.

Então a topologia proposta, escrita com honestidade, é:

```
  Domínio ──export manual de arquivo──► nosso serviço ──API──► RP Info
           └──────────── isto continua manual ────────┘
```

**A palavra "API" nessa seta é ficção.** O gargalo de hoje — alguém gerar o
arquivo no Domínio, no dia certo, sem errar a seleção de lojas — **permanece
exatamente onde está.**

Isso não é uma objeção de estilo. É a diferença entre automatizar o processo e
automatizar só a metade dele que já era a mais fácil.

---

## 2. O que sobrevive e o que é descartável

Nem tudo que se constrói na Opção A se perde. A questão é **o quê** se perde.

| Componente | Opção A → Opção B |
|---|:---:|
| As 11 regras de transformação | ✅ sobrevive |
| Validações (partida dobrada, fechamento por loja) | ✅ sobrevive |
| Trilha de auditoria e painel | ✅ sobrevive |
| Adaptador de destino (RP Info) | ✅ sobrevive |
| Conciliação por CPF | ✅ sobrevive |
| **Adaptador de origem (leitura do Domínio)** | ❌ **descartado** |
| **De-para de lojas** (códigos 762, 763, 761…) | ❌ **refeito** |
| **De-para de plano de contas** | ❌ **refeito** |
| **De-para de classificação gerencial** | ❌ **refeito** |
| **Recuperação da perna de crédito do FGTS** | ❌ **provavelmente não existe no RM** |
| **Homologação em paralelo** (aceite linha a linha) | ❌ **feita duas vezes** |

✅ **O que já construímos é justamente a coluna de cima.** O motor, as
validações e o adaptador de destino foram escritos sem depender da origem — e
já reproduzem o processo atual linha a linha.

**Isso é argumento a favor da Opção B, não contra.** O investimento já feito é
exatamente a parte reutilizável. O que a Opção A acrescenta é a parte que se joga fora.

---

## 3. Os seis argumentos

### 1 · Não existe API de saída no Domínio
A seta "Domínio → API" não se sustenta. O export continuaria manual, e o gargalo
de pessoa — o mesmo que motiva o projeto — permaneceria.
*Ver seção 1.1.*

### 2 · Três tabelas de correspondência seriam construídas para serem jogadas fora
Lojas, plano de contas e classificação gerencial precisam ser mapeados. Na
Opção A, são mapeados a partir dos **códigos do Domínio** (762 → 001, 763 → 002…).
No RM, os códigos são outros — **coligada e filial**, não o cadastro do Domínio.
**Os três de-paras são refeitos do zero.** E não é trabalho de desenvolvedor: é
trabalho da Controladoria, que é o recurso mais escasso da equação.

### 3 · A homologação, que é a parte mais cara, seria feita duas vezes
O critério de aceite é rodar em paralelo e bater **linha a linha**. Isso consome
1 ou 2 competências — ou seja, **1 a 2 meses de calendário** e atenção da
Controladoria em cada rodada.
Na Opção A, esse ciclo acontece uma vez contra a planilha (Domínio) e **outra
vez contra o RM**. É o item que mais custa, duplicado.

### 4 · Regras nasceriam mortas
A recuperação da perna de crédito do FGTS existe porque o export do Domínio
entrega **débito e crédito na mesma linha** — 1.004 lançamentos em 08/2026.
É uma peculiaridade daquele relatório. O RM contabiliza internamente, e
**muito provavelmente não reproduz esse comportamento.**
Construir, testar e homologar essa regra na Opção A é esforço que se descarta
por completo.

### 5 · A janela de negociação com o implantador do RM fecha
**Requisito de integração se negocia durante a implantação, não depois.**
Enquanto o implantador do RM está contratado e presente, pedir acesso a
DataServer, usuário de serviço, ambiente de homologação e status de lote fechado
é escopo. Depois que ele sai, cada uma dessas coisas vira chamado, orçamento e
fila.
A Opção A **adia essas conversas para depois da janela** em que elas são baratas.

### 6 · O risco que não aparece no cronograma
Se a ponte provisória funcionar bem, a pressão para migrar diminui. A dor que
justificava o projeto do RM — a planilha, o retrabalho, o gargalo de pessoa —
some, e o que sobra é um custo de migração sem urgência aparente.
**A solução provisória passa a ser o argumento contra a definitiva.**
Este é o risco mais difícil de defender numa reunião, porque não tem número —
mas é o mais comum de se materializar.

---

## 4. As objeções que virão — e a resposta para cada

> **"Mas o RM ainda vai demorar. Precisamos resolver alguma coisa agora."**

Concordo com a urgência — e discordo do alvo. **O que dói agora não é o ETL.**
O que dói é (a) a base completa de 5.682 colaboradores, com CPF, salário e conta
bancária, sendo baixada todo mês para uma pasta de rede, e (b) a conciliação
feita pelo nome da pessoa, que já exige digitação manual.
**Os dois se resolvem sem tocar na origem** — ver seção 6. São semanas, não meses.

---

> **"Vocês já não fizeram o motor funcionar com o Domínio?"**

Fizemos, e ele bate linha a linha. **Mas é exatamente a parte que se aproveita
nas duas opções.** O que não se aproveita é o adaptador de entrada e os três
de-paras. Ter chegado até aqui não é razão para seguir por esse caminho — é
razão para não precisar seguir.

---

> **"Vocês mesmos disseram que é só trocar o adaptador depois."**

E continua sendo verdade — **para o adaptador**. O problema nunca foi ele.
São os três de-paras construídos sobre códigos que vão mudar, a homologação
feita duas vezes, e o risco da seção 3.6.
Foi a definição da direção estratégica que mudou a conta. Com ela, a
recomendação muda junto.

---

> **"Assim a gente ganha tempo enquanto o RM não chega."**

Ganha-se tempo de entrega e **perde-se a janela de negociação** com o
implantador do RM — que é quando os acessos e endpoints custam zero.
É uma troca real, mas não é de graça, e costuma ser apresentada como se fosse.

---

> **"O Domínio tem API, está no site deles."**

Tem — **de entrada**. A documentação descreve envio de documentos fiscais e
lançamento de rubricas *para dentro* do Domínio. Para o sentido que este
projeto precisa, **não há endpoint**.
*Se estivermos errados, é a melhor notícia possível: peçam ao contato da
Thomson Reuters o endpoint de extração de lançamentos contábeis. Se existir,
reconsideramos na hora.*

---

> **"E se o RM atrasar?"**

Aí a decisão é revisitada — **com dados, não com suposição**. A seção 5 define
o critério objetivo para isso.

---

## 5. Quando o caminho pelo Domínio seria a decisão certa

Não é uma posição ideológica. **Existe um cenário em que a Opção A se justifica**,
e é honesto dizer qual:

> Quando o custo de continuar no processo manual, pelo tempo que faltar até a
> virada do RM, **superar** o custo de construir a ponte duas vezes.

Os dois lados dessa conta:

| Custo de esperar | Custo de construir duas vezes |
|---|---|
| N meses × (1 tarde de trabalho especializado + risco de erro manual) | adaptador de origem descartado |
| N meses de exposição do dump de dados pessoais *(mas ver seção 6)* | 3 de-paras refeitos pela Controladoria |
| N meses de gargalo de uma pessoa só | 1 ciclo extra de homologação (1–2 competências) |
| | janela de negociação com o implantador perdida |

**Só vocês têm o N.** Ele sai da resposta à pergunta N1 — a data de virada do RM.

**Nossa leitura:** se a virada estiver dentro do horizonte de poucos fechamentos,
a Opção B ganha com folga. Se estiver muito distante ou indefinida, a conversa
deixa de ser técnica e passa a ser sobre **por que a migração não tem data** —
que é uma discussão mais importante que esta.

---

## 6. O que fazer agora, independentemente da decisão

Três coisas valem a pena **hoje**, e nenhuma depende de qual origem vencer.
Todas sobrevivem à migração integralmente:

### 6.1 Eliminar o dump de dados pessoais
O arquivo `dfunc.txt` — **5.682 cadastros × 76 campos**, incluindo CPF, PIS, RG,
filiação, endereço, salário e conta bancária — é baixado todo mês para uma pasta
de rede compartilhada.
A API do RP Info oferece consulta de colaborador **por CPF**. Uma consulta
pontual substitui o download inteiro.
**É o maior ganho de LGPD do projeto, e o mais barato.**

### 6.2 Trocar a conciliação por nome pela conciliação por CPF
Já verificamos: **100% dos 5.682 cadastros do RP Info têm CPF**.
Resolve a digitação manual de códigos, a aba de nomes divergentes e a etapa de
correção de acentos — e desarma os **3 pares de homônimos** encontrados no
cadastro, que hoje duplicariam o lançamento contábil se entrassem na folha.

### 6.3 Levar as perguntas técnicas aos fornecedores
As 8 perguntas da Parte 2 da pauta não dependem de nenhuma decisão de topologia.
Quanto antes forem feitas, mais cedo a Opção B deixa de ter incógnitas — e mais
fraco fica o argumento de que "só o Domínio é viável agora".

> **Estas três frentes são a resposta concreta para "precisamos de algo agora".**
> Elas entregam valor imediato sem comprometer a arquitetura.

---

## 7. A recomendação

**Ir direto para RM → API → RP Info.**

E, em paralelo e desde já, executar as três frentes da seção 6 — que resolvem o
que dói hoje, sem construir nada que precise ser jogado fora depois.

**Se a resposta à pergunta N1 revelar que a virada do RM está longe ou sem data,**
a conversa muda de assunto: deixa de ser sobre qual ponte construir e passa a ser
sobre por que a migração não tem data. Essa é a discussão que realmente destrava
o projeto.

---

**Documentos relacionados:**
[ENTENDIMENTO-DO-PROCESSO.md](ENTENDIMENTO-DO-PROCESSO.md) ·
[PERGUNTAS-PRIORITARIAS.md](PERGUNTAS-PRIORITARIAS.md) ·
[CONTRATO-DE-DADOS.md](CONTRATO-DE-DADOS.md)
