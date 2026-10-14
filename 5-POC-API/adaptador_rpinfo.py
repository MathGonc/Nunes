# -*- coding: utf-8 -*-
"""
Adaptador de destino: RP Info (RP One / Mix).

Converte os lancamentos ja transformados pelo nucleo em payloads da API
publica da RP Info -- `POST /v1.0/fde`, objeto `DocumentoFDE`.

Base: especificacao OpenAPI 3.0.1 "RP Services" v2.0.89, publicada em
https://servicosflex.rpinfo.com.br:7443/v1.0/documentacao
(679 operacoes; ambiente de homologacao documentado pelo proprio fornecedor).

--------------------------------------------------------------------------
IMPORTANTE -- ESTE ADAPTADOR NAO ENVIA NADA
--------------------------------------------------------------------------
Ele apenas GERA e VALIDA o payload localmente. Nenhuma chamada de rede e
feita. Enviar dados a um sistema de terceiro exige autorizacao do cliente e
credenciais proprias, e isso nao foi solicitado nem concedido.

--------------------------------------------------------------------------
A PERGUNTA QUE ESTE ARQUIVO EXISTE PARA FAZER
--------------------------------------------------------------------------
"FDE" significa Fiscal Data Entry. O objeto e modelado em torno de um
DOCUMENTO FISCAL (modelo, serie, chave DFe de 44 caracteres, ICMS,
fornecedor). Uma folha de pagamento nao e documento fiscal.

O que ja esta provado: o array `contrapartidas` do DocumentoFDE tem
exatamente os campos do arquivo que a empresa importa hoje -- conta,
unidade, valor, dc, historico. E o array `pendencias` tem `portador`,
que e o "agrupar liquidos por banco" do POP atual.

O que falta confirmar com a RP Info:
  Q1. Um documento FDE pode ser criado com especie/codigoDocumento de folha
      (o "3607" do POP), sem chave de NFe e sem itens fiscais?
  Q2. Onde entra o CODIGO DO COLABORADOR? Hoje ele existe por LINHA
      (coluna 7 do CSV). No FDE, catEntidade/codEntidade sao do DOCUMENTO.
      Vai em subContas, cCustos, ou 1 documento por colaborador?
  Q3. Granularidade: 1 documento por competencia, por loja, ou por
      colaborador? Isso muda de 1 para 7.853 chamadas.
  Q4. Ha limite de tamanho de payload / contrapartidas por documento?
  Q5. Existe idempotencia? `numeroRecibo` identifica o lote -- reenviar o
      mesmo documento duplica ou e rejeitado?

Enquanto Q1-Q5 nao forem respondidas, este adaptador produz tres
granularidades diferentes para a conversa ser concreta na reuniao.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from etl_folha import (
    ARQ_FOLHA, ARQ_PLANILHA, ARQ_PLANOGER, SAIDA,
    enriquecer, ler_base_colaboradores, ler_codigos_manuais,
    ler_folha_dominio, ler_plano_gerencial, recuperar_pernas_de_credito,
    validar,
)

# Codigo de documento usado hoje na operacao manual do destino, citado no POP.
# PERGUNTA Q1: e este o codigo correto para a carga de folha?
CODIGO_DOCUMENTO_FOLHA = "3607"
ESPECIE_FOLHA = "3607"


def _cents(v: Decimal) -> float:
    """A API espera number/double. Arredondamos uma unica vez, no limite."""
    return float(v.quantize(Decimal("0.01")))


def contrapartida(lc) -> dict:
    """Um lancamento -> um item do array `contrapartidas` do DocumentoFDE."""
    return {
        "conta": lc.conta,
        "unidade": lc.loja_destino,
        "valor": _cents(lc.valor),
        "dc": "D" if lc.natureza == "DB" else "C",
        "historico": lc.historico,
        # PERGUNTA Q2: o codigo do colaborador nao tem campo proprio na
        # contrapartida. Provisoriamente vai no complemento, so para nao
        # perder o dado. Nao e onde ele deve ficar.
        "complemento": f"COLAB:{lc.codigo_final}",
    }


def documento(unidade: str, data, lancamentos: list) -> dict:
    """Monta um DocumentoFDE. Campos fiscais omitidos de proposito: ver Q1."""
    total = sum((lc.valor for lc in lancamentos if lc.natureza == "DB"), Decimal(0))
    return {
        "unidade": unidade,
        "dataMvto": data.strftime("%d/%m/%Y"),
        "dataEmissao": data.strftime("%d/%m/%Y"),
        "codigoDocumento": CODIGO_DOCUMENTO_FOLHA,
        "especie": ESPECIE_FOLHA,
        "totalDcto": _cents(total),
        "observacao": f"Folha de pagamento {data.strftime('%m/%Y')} - carga automatizada",
        "contrapartidas": [contrapartida(lc) for lc in lancamentos],
    }


# ---------------------------------------------------------------------------
# Tres granularidades possiveis. Qual delas vale depende da resposta Q3.
# ---------------------------------------------------------------------------


def por_competencia(lancamentos) -> list:
    data = max(lc.data for lc in lancamentos)
    return [documento("", data, lancamentos)]


def por_loja(lancamentos) -> list:
    grupos = defaultdict(list)
    for lc in lancamentos:
        grupos[lc.loja_destino].append(lc)
    return [documento(u, max(g, key=lambda x: x.data).data, g)
            for u, g in sorted(grupos.items())]


def por_loja_e_data(lancamentos) -> list:
    grupos = defaultdict(list)
    for lc in lancamentos:
        grupos[(lc.loja_destino, lc.data)].append(lc)
    return [documento(u, d, g) for (u, d), g in sorted(grupos.items())]


ESTRATEGIAS = {
    "competencia": (por_competencia, "1 documento com tudo"),
    "loja": (por_loja, "1 documento por loja"),
    "loja-data": (por_loja_e_data, "1 documento por loja e data de movimento"),
}


def conferir(docs, lancamentos) -> list:
    """O payload precisa preservar o que o nucleo ja validou."""
    problemas = []

    linhas = sum(len(d["contrapartidas"]) for d in docs)
    if linhas != len(lancamentos):
        problemas.append(f"perdeu linhas: {linhas} no payload vs {len(lancamentos)} no lote")

    d = sum(Decimal(str(c["valor"])) for doc in docs
            for c in doc["contrapartidas"] if c["dc"] == "D")
    c = sum(Decimal(str(c["valor"])) for doc in docs
            for c in doc["contrapartidas"] if c["dc"] == "C")
    if d != c:
        problemas.append(f"partida dobrada quebrou no payload: D {d} != C {c}")

    sem_unidade = [c for doc in docs for c in doc["contrapartidas"] if not c["unidade"]]
    if sem_unidade:
        problemas.append(f"{len(sem_unidade)} contrapartida(s) sem unidade")

    return problemas


def main():
    lancamentos, _ = ler_folha_dominio(ARQ_FOLHA)
    lancamentos += recuperar_pernas_de_credito(lancamentos)
    base, _ = ler_base_colaboradores(ARQ_PLANILHA)
    enriquecer(lancamentos, base, ler_plano_gerencial(ARQ_PLANOGER),
               ler_codigos_manuais(ARQ_PLANILHA))
    validar(lancamentos)

    SAIDA.mkdir(exist_ok=True)
    print("=" * 78)
    print("Adaptador de destino: RP Info  |  POST /v1.0/fde  (DocumentoFDE)")
    print("=" * 78)
    print(f"\nLancamentos no lote ........... {len(lancamentos)}")
    print("NENHUMA chamada de rede e feita. Somente geracao e validacao local.\n")

    print(f"{'ESTRATEGIA':<14}{'DOCS':>7}{'CONTRAPARTIDAS':>17}{'MAIOR DOC':>12}{'JSON':>11}")
    print("-" * 61)
    for nome, (fn, _) in ESTRATEGIAS.items():
        docs = fn(lancamentos)
        blob = json.dumps(docs, ensure_ascii=False)
        maior = max(len(d["contrapartidas"]) for d in docs)
        print(f"{nome:<14}{len(docs):>7}{sum(len(d['contrapartidas']) for d in docs):>17}"
              f"{maior:>12}{len(blob) / 1024:>10.0f}K")
        problemas = conferir(docs, lancamentos)
        for p in problemas:
            print(f"   [X] {p}")

    padrao = "loja"
    docs = ESTRATEGIAS[padrao][0](lancamentos)
    destino = SAIDA / f"payload_rpinfo_fde_{padrao}.json"
    destino.write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n>>> Payload gravado em {destino}")
    print(f"    ({ESTRATEGIAS[padrao][1]}, {len(docs)} documentos)")

    print("\nAMOSTRA -- primeiro documento, 2 primeiras contrapartidas")
    print("-" * 56)
    amostra = dict(docs[0])
    amostra["contrapartidas"] = amostra["contrapartidas"][:2] + ["... (truncado)"]
    print(json.dumps(amostra, ensure_ascii=False, indent=2))

    print("\n" + "=" * 78)
    print("O payload fecha em partida dobrada e preserva as 7.853 linhas.")
    print("Falta a RP Info confirmar Q1-Q5 no topo deste arquivo.")
    print("=" * 78)


if __name__ == "__main__":
    sys.exit(main())
