# PoC — Ponte de integração Folha → RP Info

Prova de conceito construída sobre os arquivos reais da competência **08/2026**.

**O que ela demonstra:** que as regras hoje enterradas em 8 consultas Power Query
podem viver em código versionado, testável e auditável — reproduzindo o
resultado atual **linha a linha**, e enxergando o que o processo atual não vê.

## Topologia

```
HOJE     Domínio ──[planilha Excel]──► RP Info (RP One / Mix)
FUTURO   TOTVS RM ──────[API]────────► RP Info (RP One / Mix)
```

O cliente definiu que a origem passa a ser o **TOTVS RM**. O núcleo desta PoC
foi escrito sem saber quem seria a origem — trocar Domínio por RM troca **um
adaptador**, não o sistema. É exatamente o ponto que a arquitetura em
adaptadores existia para provar, e a troca de origem provou.

---

## Como rodar

```bash
python etl_folha.py                  # motor principal + paridade
python adaptador_rpinfo.py           # gera o payload da API da RP Info
python conferir_arquivo_entregue.py  # audita o arquivo importado no destino
python layout_pendencias.py          # valida o layout do sentido inverso
```

Requisito: Python 3.10+ e `openpyxl`. Nenhuma configuração, nenhum servidor,
nenhum acesso externo — lê apenas os arquivos já presentes nas pastas 1 a 4.

---

## Os três scripts

### `etl_folha.py` — o motor

Lê o export da origem, aplica as 11 regras extraídas da planilha, valida e gera
o lote para o destino.

**Resultado:**

```
Linhas geradas pela PoC .......   7853
Linhas na aba 'Importacao' ....   7853
So na PoC .....................      0
So na planilha ................      0

>>> PARIDADE TOTAL. A PoC reproduz o processo atual linha a linha.
```

E, de graça, 4 alertas que o processo atual não produz:

| Alerta | Medida |
|---|---|
| `HOMONIMOS_NA_BASE` | 3 pares de nomes idênticos com códigos diferentes |
| `CARACTERE_NAO_ASCII_NO_HISTORICO` | 63 lançamentos com `º` (U+00BA) |
| `RESOLVIDO_POR_DIGITACAO_MANUAL` | 6 lançamentos |
| `COMPETENCIA_MISTURADA` | 95 lançamentos de 09/2026 dentro do arquivo de 08/2026, R$ 123.215,95 |

### `adaptador_rpinfo.py` — o destino, por API

Converte o lote em `DocumentoFDE` — o objeto do `POST /v1.0/fde` da API pública
da RP Info (OpenAPI 3.0.1, "RP Services" v2.0.89, 679 operações).

**Não envia nada.** Apenas gera e valida o payload localmente.

| Estratégia | Documentos | Contrapartidas | Maior doc | JSON |
|---|---:|---:|---:|---:|
| 1 por competência | 1 | 7.853 | 7.853 | ~1 MB |
| **1 por loja** | **17** | **7.853** | **629** | **~1 MB** |
| 1 por loja e data | 86 | 7.853 | 574 | ~1 MB |

Nas três, o payload preserva as 7.853 linhas e fecha em partida dobrada.

O `ContrapartidaFDE` — descrito pelo fornecedor como *"contrapartida/lançamento
contábil"* — tem exatamente os campos do arquivo atual:

| CSV de hoje | `ContrapartidaFDE` |
|---|---|
| Cód. loja | `unidade` |
| Conta | `conta` |
| Valor | `valor` |
| `DB`/`CR` | `dc` |
| Histórico | `historico` + `complemento` |

As cinco perguntas que faltam para a RP Info estão no topo do arquivo, como
`Q1`–`Q5`. A principal: **FDE significa *Fiscal Data Entry*, e folha de
pagamento não é documento fiscal.**

### `conferir_arquivo_entregue.py` — a auditoria

Compara o arquivo efetivamente importado no destino com a planilha que o gerou.
**Eles não são iguais:** 11 colunas contra 10, zeros à esquerda perdidos, 22,8%
dos valores sem 2 casas decimais, duas convenções decimais no mesmo arquivo.

O destino aceitou assim. Ou seja: **não há validação de layout na entrada.**

### `layout_pendencias.py` — o sentido inverso

Confronta o layout documentado com o arquivo real e prova qual está correto.

| Campo | Doc | Real | Desvio |
|---|---:|---:|---:|
| Ano | 14–17 | 13–16 | +1 |
| Mês | 19–20 | 17–18 | +2 |
| Rubrica | 21–24 | 19–22 | +2 |
| Máscara `11` | 25–26 | 23–24 | +2 |
| Valor | 27–35 | 25–33 | +2 |
| Código da loja | 36–45 | 34–43 | +2 |
| **Total** | **45** | **43** | **−2** |

Prova: as 86 linhas do arquivo, lidas com o layout corrigido e reescritas,
saem **idênticas ao original, byte a byte**.

---

## Onde estão as perguntas em aberto

No topo do `etl_folha.py`, como flags com o comportamento atual por padrão:

```python
APARAR_HISTORICO = False              # o destino usa esse campo p/ conciliar?
NORMALIZAR_ORDINAL_MASCULINO = False  # o destino aceita 'º'?
```

**O default sempre reproduz o que está em produção hoje** — porque enquanto a
pergunta não for respondida, o processo atual é a única referência confiável
que temos. Mudar de ideia depois custa trocar um `False` por `True`.

A lista completa está em [`CONTRATO-DE-DADOS.md`](CONTRATO-DE-DADOS.md).

---

## O que esta PoC **não** é

Não é a arquitetura final. As entradas aqui são os mesmos arquivos que o
processo atual usa.

Na solução definitiva, `ler_folha_dominio()` e `ler_base_colaboradores()` viram
adaptadores de RM e de API — **e só eles mudam**. O núcleo de regras, as
validações e a trilha permanecem exatamente como estão.

E `ler_base_colaboradores()` já tem substituto confirmado:
`GET /v1.2/funcionario/codcpf/{codcpf}`. Uma consulta por CPF no lugar de um
dump de 76 campos × 5.682 pessoas numa pasta de rede.

---

## Estrutura

```
5-POC-API/
├── etl_folha.py                  motor: origem -> regras -> validação -> destino
├── adaptador_rpinfo.py           destino: payload DocumentoFDE (POST /v1.0/fde)
├── conferir_arquivo_entregue.py  auditoria do arquivo importado hoje
├── layout_pendencias.py          layout do sentido inverso, com round-trip
│
├── ENTENDIMENTO-DO-PROCESSO.md   os 3 fluxos, como são e como ficam  ← enviar antes
├── RECOMENDACAO-ARQUITETURA.md   por que começar pelo RM             ← defesa
├── PERGUNTAS-PRIORITARIAS.md     9 de negócio + 8 técnicas           ← pauta
├── CONTRATO-DE-DADOS.md          as 79 perguntas, com evidências     ← referência
│
└── saida/
    ├── Importar_Folha_API.csv         lote normalizado (2 casas, zeros preservados)
    └── payload_rpinfo_fde_loja.json   17 documentos prontos para a API
```

### Ordem de leitura para o cliente

1. **`ENTENDIMENTO-DO-PROCESSO.md`** — enviar antes da reunião, para confirmação.
   Se o entendimento estiver errado, metade das perguntas muda.
2. **`RECOMENDACAO-ARQUITETURA.md`** — ler **antes** da reunião, não durante.
   É a defesa contra a proposta "Domínio → API → RP Info agora, RM depois".
   Traz as seis objeções que costumam aparecer, com a resposta para cada.
3. **`PERGUNTAS-PRIORITARIAS.md`** — a pauta, em duas partes: **negócio**
   (Diretoria, Controladoria, RH/DP) e **sistemas** (TI e os dois fornecedores).
   São duas conversas, não uma.
4. **`CONTRATO-DE-DADOS.md`** — consulta, quando a discussão descer ao detalhe.

---

## Fontes

- [RP Services — OpenAPI v2.0.89](https://servicosflex.rpinfo.com.br:7443/v1.0/documentacao?location=documentacao) · [RP One](https://www.rpinfo.com.br/produto/rp-one/56)
- [Domínio — Integração com ERP](https://www.dominiosistemas.com.br/solucoes/integracao-com-erp/)
- [TOTVS — DataServers RM WebServices](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360051030334-RM-SAU-Utiliza%C3%A7%C3%A3o-de-DataServers-RM-WebServices)
