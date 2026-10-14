# Resumo — como o processo de hoje pode ficar automático

> Este documento explica, para quem não leu nada, **como o processo funciona hoje
> e como ele ficaria com os sistemas conversando sozinhos**. Cada informação diz de onde veio.

## De onde vêm as informações

| Marca | O que é |
|---|---|
| **[POP]** | O procedimento escrito do processo atual (pasta `0-POP`) |
| **[Pendências]** | O arquivo de pendências de convênio e a documentação do relatório (pasta `1-Atividade - Importar Pendências`) |
| **[Conferência]** | Os relatórios do Domínio usados para conferir os valores (pasta `2-Atividade - Validar Dados Domínio`) |
| **[Planilha]** | O arquivo exportado do Domínio e a planilha que trata os dados (pasta `3-Atividade - Tratar Dado Folha para Importação`) |
| **[Importado]** | O arquivo que foi de fato importado no RP Info (pasta `4-Atividade - Exportar txt e Importar no RP One`) |
| **[Fornecedores]** | Documentação pública da RP Info, da TOTVS e do Domínio |
| **[Nossa leitura]** | Recomendação nossa — não é fato verificado |

Os números são do fechamento de **agosto/2026**, contados nos próprios arquivos.

---

## 1. O problema em uma frase

A folha de pagamento é calculada num sistema; a contabilidade e o financeiro ficam em outro.
**A informação nasce de um lado e precisa chegar no outro — e hoje ela é levada à mão,
passando por uma planilha.**

| Sistema | Papel |
|---|---|
| **Domínio** | Calcula a folha **hoje** |
| **TOTVS RM** | Vai calcular a folha **no futuro** (decisão da empresa) |
| **RP Info** (também chamado de RP One ou Mix) | Contabilidade e financeiro — é para onde a folha vai |

---

## 2. Como funciona hoje

São **três trocas de informação**, não uma:

```
1. FOLHA          Domínio ──► planilha Excel ──► RP Info
2. FUNCIONÁRIOS   RP Info ──► pasta de rede ──► planilha        (para a planilha saber quem é quem)
3. PENDÊNCIAS     RP Info ──► Domínio, uma loja por vez         (convênio e quebra de caixa viram desconto na folha)
```

**Todo mês · até o 5º dia útil · 7.853 lançamentos · R$ 2,6 milhões · 17 lojas · 1.078 colaboradores** [POP, Planilha]

### 1. Folha

O passo a passo [POP]:

1. **Preparar:** descobrir se surgiu algum tipo novo de verba na folha e configurá-lo **loja por loja — 17 vezes**.
2. **Extrair e conferir:** tirar relatórios do Domínio e conferir os valores **no olho** [Conferência].
3. **Tratar:** atualizar a planilha e, quando o nome de um funcionário não bate entre os sistemas, **digitar o código dele à mão**.
4. **Importar:** salvar o arquivo, apagar o cabeçalho à mão e importar no RP Info.
5. **Depois da importação:** agrupar pagamentos por banco, ajustar pensões, dar baixa em contas e conferir. **É cerca de metade do trabalho.**

**As regras de negócio não estão escritas em lugar nenhum** — estão dentro da planilha, em
fórmulas que só quem montou entende [Planilha]. Por exemplo: como cada loja do Domínio
corresponde a cada loja do RP Info, ou como separar os valores de FGTS para que a conta feche.

### 2. Base de funcionários

- Todo mês, a base **inteira** de funcionários é baixada do RP Info para uma pasta de rede [POP].
- São **5.682 pessoas**, com CPF, RG, endereço, salário e conta bancária [Planilha].
- Ela serve só para descobrir quem é quem **pelo nome** — o que exige correções à mão [Planilha].
- **Todos os cadastros já têm CPF**, que seria a forma segura de identificar a pessoa — mas não é usado [Planilha].
- Há **3 pares de pessoas diferentes com o mesmo nome**. Se uma delas entrar na folha, o lançamento sai duplicado [Planilha].

### 3. Pendências de convênio

- O relatório só gera **uma loja por vez** e só **um usuário** tem acesso → 17 arquivos por mês, feitos por uma pessoa [Pendências].
- A documentação do formato do arquivo **não bate com o arquivo real** [Pendências].
- Não se sabe se o Domínio confirma que recebeu.

### O que os arquivos mostram

- O arquivo importado no RP Info **não é igual** ao que a planilha gerou — tem coluna a mais, números sem zeros e valores em formatos diferentes. **O RP Info aceitou mesmo assim** — ou seja, não há nenhuma trava contra erro [Importado].
- O arquivo de agosto contém **95 lançamentos de setembro** (R$ 123 mil) misturados [Planilha].
- Uma das lojas não teve nenhum lançamento no mês [Planilha].

### Por que isso é um risco

- As regras do negócio **só existem dentro de uma planilha**.
- Os sistemas se reconhecem **pelo nome da pessoa**, não por um documento.
- Dados pessoais de 5.682 pessoas **ficam numa pasta de rede**, todo mês (LGPD).
- **Tudo depende de uma pessoa só.**

---

## 3. Como ficaria

```
   TOTVS RM  ─────►  serviço de integração  ─────►  RP Info
                     (confere, trava se tiver erro,
                      guarda histórico de tudo)
```

Em vez de alguém exportar arquivos, tratar numa planilha e importar, **os sistemas passam a
conversar diretamente**. Os três fornecedores têm essa possibilidade — com uma exceção
importante, explicada na seção 4 [Fornecedores].

| Hoje | Como ficaria |
|---|---|
| Alguém exporta a folha do Domínio | O serviço busca a folha direto no RM |
| Regras escondidas numa planilha | Regras escritas, documentadas e testadas |
| Tipo novo de verba configurado 17 vezes | O sistema detecta e avisa o que falta antes de enviar |
| Base inteira de funcionários numa pasta de rede | **Deixa de existir** — o sistema consulta só a pessoa que precisa, pelo CPF |
| Nome digitado e código corrigido à mão | **Deixa de existir** — a pessoa é identificada pelo CPF |
| Salvar arquivo, apagar cabeçalho, importar | O envio é direto |
| Conferência no olho | O sistema confere sozinho e mostra se bateu |
| Pendências: 17 arquivos por mês | Uma única execução, direto para o RM |
| Erro descoberto depois (ou nunca) | Erro **impede o envio** e aparece com nome e motivo |

A parte de **depois da importação** (bancos, pensões, baixas) também parece automatizável,
mas depende de decidir se entra no projeto.

**O que dá trabalho novo com a troca para o RM:** as tabelas que dizem "esta loja aqui é aquela
loja lá" e "esta conta aqui é aquela conta lá" precisam ser **refeitas** para os códigos do RM.
É o maior esforço novo do projeto, e depende da Controladoria [Nossa leitura].

**O que ainda precisa de resposta dos fornecedores:** se o RP Info aceita receber a folha
diretamente, e se o RM entrega a folha já no formato contábil [Fornecedores].

---

## 4. A recomendação [Nossa leitura]

⚠️ **Ligar direto o RM ao RP Info. Não montar a integração a partir do Domínio.**

Em algum momento vai aparecer a ideia: *"Faz agora a partir do Domínio, e depois troca para o RM."*
Não compensa, porque:

1. **O Domínio não consegue entregar os dados sozinho** — ele só recebe [Fornecedores]. Alguém continuaria exportando à mão todo mês, que é justamente o problema.
2. As tabelas de correspondência seriam feitas **duas vezes**.
3. O período de testes em paralelo (1 a 2 meses) também seria feito **duas vezes**.
4. Enquanto a implantação do RM está acontecendo, pedir acessos ao fornecedor é barato; **depois, vira custo**.
5. A solução provisória tende a **virar definitiva** e tirar a urgência da migração.

**O que dá para fazer já, qualquer que seja a decisão:**
1. **Parar de baixar a base de funcionários** para a pasta de rede — maior ganho de LGPD, e o mais barato.
2. **Identificar as pessoas pelo CPF**, e não pelo nome.
3. **Levar as perguntas técnicas aos fornecedores.**

---

## 5. As perguntas

**Para a empresa** — Diretoria, Controladoria, RH/DP:

1. **Quando o RM entra no lugar do Domínio?** Isso decide se fazemos a integração uma vez ou duas.
2. O **trabalho depois da importação** (bancos, pensões, baixas) entra no projeto?
3. Quando aparecer um **tipo novo de verba** sem configuração, o envio **para** ou **segue** e se ajusta depois?
4. Quando a folha é **refeita**, o que se faz com o que já tinha sido importado?
5. Quem será **responsável pelas tabelas de correspondência** (lojas e contas)? O plano de contas do RP Info vai mudar?
6. As **pendências de convênio** passam a ir para o RM?
7. O **CPF** dos funcionários é confiável e igual nos dois sistemas?
8. Em que dia a folha **fecha** e para de mudar?
9. Existe **contrato com a RP Info** que dê acesso ao suporte técnico deles?

**Para os fornecedores** — conversa separada, com a TI:

- **RP Info:** o sistema aceita receber a folha diretamente? Se o mesmo envio for feito duas vezes, duplica? Como se desfaz um envio?
- **RM:** a folha sai já no formato contábil? Como se sabe que a folha do mês está fechada? As pendências podem entrar direto no RM?

**Se só der tempo para três:** 1, 2 e 6.

---

> **Se só sobrar tempo para uma:** quando o RM entra no lugar do Domínio.
> Ela decide se fazemos a integração uma vez ou duas.

---

## Onde está o detalhe

| Documento | Conteúdo |
|---|---|
| [ENTENDIMENTO-DO-PROCESSO.md](ENTENDIMENTO-DO-PROCESSO.md) | Os três fluxos passo a passo, hoje e depois |
| [RECOMENDACAO-ARQUITETURA.md](RECOMENDACAO-ARQUITETURA.md) | Por que começar pelo RM, com a resposta a cada objeção |
| [PERGUNTAS-PRIORITARIAS.md](PERGUNTAS-PRIORITARIAS.md) | As perguntas com contexto e como conduzir a reunião |
| [CONTRATO-DE-DADOS.md](CONTRATO-DE-DADOS.md) | A versão técnica completa |
