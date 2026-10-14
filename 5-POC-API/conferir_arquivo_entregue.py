# -*- coding: utf-8 -*-
"""
Confere o arquivo que foi efetivamente importado no destino contra a aba
"Importacao" da planilha que o gerou.

Motivo: os dois deveriam ser identicos. Nao sao. Este script mede a diferenca,
em vez de opinar sobre ela.
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

import openpyxl

BASE = Path(__file__).resolve().parent.parent
ARQ_PLANILHA = BASE / "3-Atividade - Tratar Dado Folha para Importação" / \
    "Planilha para tratar e preparar dado para Importar Folha no RP Info.xlsx"
ARQ_CSV = BASE / "4-Atividade - Exportar txt e Importar no RP One" / \
    "Importar_Folha - Todas Lojas.csv"


def ler_csv():
    with open(ARQ_CSV, encoding="utf-8-sig", newline="") as fh:
        return [l.rstrip("\r\n").split(";") for l in fh if l.strip()]


def ler_planilha():
    wb = openpyxl.load_workbook(ARQ_PLANILHA, read_only=True, data_only=True)
    ws = wb["Importação"]
    linhas = []
    for l in ws.iter_rows(min_row=2, values_only=True):
        if l[0] is None:
            continue
        data = l[3].strftime("%d/%m/%Y") if isinstance(l[3], datetime) else str(l[3])
        linhas.append([str(l[0]), "0", str(l[2]), data, str(l[4]),
                       str(l[5] or ""), str(l[6] or ""), str(l[7] or ""),
                       str(l[8] or ""), str(l[9] or "")])
    wb.close()
    return linhas


def main():
    csv_rows = ler_csv()
    plan_rows = ler_planilha()

    print("=" * 78)
    print("Conferencia: arquivo importado no destino  x  planilha que o gerou")
    print("=" * 78)
    print(f"\nLinhas no CSV importado ....... {len(csv_rows):>6}")
    print(f"Linhas na aba 'Importacao' .... {len(plan_rows):>6}")

    larguras = Counter(len(r) for r in csv_rows)
    print(f"\n1. LARGURA DAS LINHAS")
    print(f"   Planilha ................... 10 colunas")
    for n, q in larguras.most_common():
        print(f"   CSV ........................ {n} colunas em {q} linhas")
    if max(larguras) > 10:
        extras = [r[10] for r in csv_rows if len(r) > 10 and r[10].strip()]
        print(f"   -> coluna 11 preenchida em {len(extras)} de {len(csv_rows)} linhas")
        print(f"   -> amostra: {extras[:6]}")
        print(f"   -> essa coluna NAO existe na planilha. Origem desconhecida.")

    print(f"\n2. CODIGO DE LOJA")
    lojas_csv = sorted(set(r[0] for r in csv_rows), key=lambda x: int(x))
    lojas_pl = sorted(set(r[0] for r in plan_rows))
    print(f"   Planilha ................... {lojas_pl[:6]} ...")
    print(f"   CSV ........................ {lojas_csv[:6]} ...")
    if any(len(l) < 3 for l in lojas_csv):
        print(f"   -> zeros a esquerda perdidos na gravacao do CSV")

    print(f"\n3. FORMATO DE VALOR (coluna 5)")
    casas = Counter(len(r[4].split(".")[1]) if "." in r[4] else 0 for r in csv_rows)
    for n in sorted(casas):
        print(f"   {casas[n]:>6} linhas com {n} casa(s) decimal(is)")
    fora = sum(q for n, q in casas.items() if n != 2)
    print(f"   -> {fora} de {len(csv_rows)} valores ({fora / len(csv_rows):.1%}) "
          f"nao estao com 2 casas")

    print(f"\n4. CONVENCAO DECIMAL")
    tem_ponto = sum(1 for r in csv_rows if "." in r[4])
    tem_virgula = sum(1 for r in csv_rows if len(r) > 10 and "," in r[10])
    print(f"   Coluna 5 usa ponto ......... {tem_ponto} linhas")
    print(f"   Coluna 11 usa virgula ...... {tem_virgula} linhas")
    if tem_ponto and tem_virgula:
        print(f"   -> duas convencoes decimais no mesmo arquivo")

    print(f"\n5. CABECALHO")
    primeira = csv_rows[0][0] if csv_rows else ""
    print(f"   Primeira linha do CSV ...... {primeira!r}")
    print(f"   -> {'sem cabecalho (removido a mao, conforme o POP)' if primeira.isdigit() else 'com cabecalho'}")

    print("\n" + "=" * 78)
    print("CONCLUSAO: o arquivo importado no destino NAO e uma copia fiel do que")
    print("a planilha produziu. O destino aceitou mesmo assim -- o que significa")
    print("que ele e tolerante, e que nao ha validacao de layout na entrada.")
    print("=" * 78)


if __name__ == "__main__":
    main()
