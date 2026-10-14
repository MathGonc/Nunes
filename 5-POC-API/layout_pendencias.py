# -*- coding: utf-8 -*-
"""
Sentido inverso da ponte: geracao do arquivo posicional de pendencias.

Este script faz duas coisas:

1. Confronta o layout DOCUMENTADO (em "Doc Relatorio exportado pela
   Ivanilza.docx") com o layout REAL do arquivo entregue. Eles nao batem.

2. Implementa o layout real, le o arquivo de volta e reescreve byte a byte --
   provando que a regra esta correta antes de qualquer linha de integracao
   ser escrita.

Hoje este arquivo e gerado manualmente, UMA LOJA POR VEZ, por um unico usuario
autorizado. Com o layout em codigo, as 17 lojas saem numa chamada.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ARQ = BASE / "1-Atividade - Importar Pendências" / \
    "Arquivo de Importação Pendência Convênio- Loja 01.txt"

# Layout como esta escrito na documentacao entregue pelo cliente.
LAYOUT_DOCUMENTADO = [
    ("Mascara Dominio (fixo 10)",  1, 2),
    ("Numero Ponto",               3, 10),
    ("Ano",                       14, 4),
    ("Mes",                       19, 2),
    ("Rubrica",                   21, 4),
    ("Mascara Dominio (fixo 11)",  25, 2),
    ("Valor",                     27, 9),
    ("Codigo da Loja",            36, 10),
]

# Layout deduzido do arquivo real e conferido contra as 86 linhas.
LAYOUT_REAL = [
    ("Mascara Dominio (fixo 10)",  1, 2),
    ("Numero Ponto",               3, 10),
    ("Ano",                       13, 4),
    ("Mes",                       17, 2),
    ("Rubrica",                   19, 4),
    ("Mascara Dominio (fixo 11)", 23, 2),
    ("Valor",                     25, 9),
    ("Codigo da Loja",            34, 10),
]


@dataclass
class Pendencia:
    ponto: str
    ano: int
    mes: int
    rubrica: str
    valor: Decimal
    loja: str


def comprimento(layout):
    nome, inicio, tam = layout[-1]
    return inicio + tam - 1


def ler(linha: str, layout) -> dict:
    return {nome: linha[inicio - 1:inicio - 1 + tam] for nome, inicio, tam in layout}


def parse(linha: str) -> Pendencia:
    c = ler(linha, LAYOUT_REAL)
    return Pendencia(
        ponto=c["Numero Ponto"],
        ano=int(c["Ano"]),
        mes=int(c["Mes"]),
        rubrica=c["Rubrica"],
        valor=Decimal(c["Valor"]) / 100,
        loja=c["Codigo da Loja"],
    )


def serializar(p: Pendencia) -> str:
    """Escreve no layout real. E esta funcao que substitui o relatorio manual."""
    return (
        "10"
        + p.ponto.rjust(10, "0")
        + f"{p.ano:04d}"
        + f"{p.mes:02d}"
        + p.rubrica.rjust(4, "0")
        + "11"
        + str(int(p.valor * 100)).rjust(9, "0")
        + p.loja.rjust(10, "0")
    )


def main():
    linhas = [l.rstrip("\r\n") for l in open(ARQ, encoding="latin-1") if l.strip()]
    tamanhos = Counter(len(l) for l in linhas)

    print("=" * 78)
    print("Layout do arquivo de pendencias: documentacao  x  arquivo real")
    print("=" * 78)
    print(f"\nArquivo ......................... {ARQ.name}")
    print(f"Linhas .......................... {len(linhas)}")
    print(f"Tamanho das linhas .............. {dict(tamanhos)}")
    print(f"Tamanho segundo a documentacao .. {comprimento(LAYOUT_DOCUMENTADO)}")
    print(f"Tamanho segundo o arquivo ....... {comprimento(LAYOUT_REAL)}")

    print(f"\n{'CAMPO':<28} {'DOC':>10} {'REAL':>10}   {'DESVIO':>7}")
    print("-" * 62)
    for (nome, ini_d, tam_d), (_, ini_r, tam_r) in zip(LAYOUT_DOCUMENTADO, LAYOUT_REAL):
        marca = "" if ini_d == ini_r else "  <-- diverge"
        print(f"{nome:<28} {f'{ini_d}-{ini_d + tam_d - 1}':>10} "
              f"{f'{ini_r}-{ini_r + tam_r - 1}':>10}   {ini_d - ini_r:>+7}{marca}")

    print("\nPROVA DE QUE O LAYOUT REAL ESTA CORRETO")
    print("-" * 39)
    mascaras_1 = set(l[0:2] for l in linhas)
    mascaras_2 = set(l[22:24] for l in linhas)
    print(f"Mascara em 1-2 .................. {mascaras_1}  (esperado {{'10'}})")
    print(f"Mascara em 23-24 ................ {mascaras_2}  (esperado {{'11'}})")

    pends = [parse(l) for l in linhas]
    print(f"Competencia ..................... "
          f"{ {f'{p.mes:02d}/{p.ano}' for p in pends} }")
    print(f"Lojas ........................... { {int(p.loja) for p in pends} }")
    print(f"Rubricas ........................ {dict(Counter(p.rubrica for p in pends))}")
    print(f"Pontos distintos ................ {len({p.ponto for p in pends})}")
    print(f"Valor total ..................... R$ {sum(p.valor for p in pends):,.2f}")

    print("\nTESTE DE IDA E VOLTA (round-trip)")
    print("-" * 33)
    divergentes = [(i, o, serializar(p))
                   for i, (o, p) in enumerate(zip(linhas, pends), 1)
                   if serializar(p) != o]
    if divergentes:
        print(f"[X] {len(divergentes)} linha(s) nao reescrevem identicas:")
        for i, o, n in divergentes[:5]:
            print(f"    linha {i}\n      original: {o}\n      gerado  : {n}")
    else:
        print(f"[OK] as {len(linhas)} linhas foram reescritas identicas ao original.")
        print("     O layout real esta provado. A geracao automatica pode ser")
        print("     implementada com seguranca -- para as 17 lojas de uma vez.")

    deslocados = sum(1 for (_, d, _), (_, r, _) in
                     zip(LAYOUT_DOCUMENTADO, LAYOUT_REAL) if d != r)
    print("\n" + "=" * 78)
    print(f"CONSEQUENCIA: quem implementar a partir da documentacao entregue vai")
    print(f"produzir um arquivo de {comprimento(LAYOUT_DOCUMENTADO)} posicoes, "
          f"com {deslocados} de {len(LAYOUT_REAL)} campos deslocados, que o")
    print("destino rejeita ou -- pior -- aceita com os valores errados.")
    print("=" * 78)


if __name__ == "__main__":
    main()
