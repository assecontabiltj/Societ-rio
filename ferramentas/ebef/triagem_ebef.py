#!/usr/bin/env python3
"""
Triagem e-BEF da carteira de clientes.

Lê uma lista de CNPJs, consulta o QSA de cada um numa base pública do CNPJ
(BrasilAPI, com a Minha Receita como alternativa) e classifica cada empresa
quanto à obrigatoriedade do e-BEF (IN RFB 2.119/2022, redação da IN RFB 2.290/2025).

Uso:
    python triagem_ebef.py clientes.csv
    python triagem_ebef.py clientes.csv -o resultado.csv

Arquivo de entrada (CSV ou TXT, separador ";" ou ","):
    - uma linha por empresa;
    - 1ª coluna: CNPJ (com ou sem pontuação);
    - 2ª coluna (opcional): faturamento do ano anterior, em reais (ex.: 5200000 ou 5.200.000,00).

Saída: CSV separado por ";" (abre direto no Excel).

Só usa a biblioteca padrão do Python 3.8+.
"""
import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

FONTES = [
    "https://brasilapi.com.br/api/cnpj/v1/{cnpj}",
    "https://minhareceita.org/{cnpj}",
]
PAUSA_ENTRE_CONSULTAS = 1.5  # segundos, para não sobrecarregar as APIs públicas

LIMITE_2027 = 78_000_000
LIMITE_2028 = 4_800_000

# Códigos de natureza jurídica (tabela da RFB)
LTDA_OU_SIMPLES = {"2062", "2240", "2232"}  # Ltda (inclui SLU), soc. simples limitada, soc. simples pura
SA_FECHADA = {"2054"}
SA_ABERTA = {"2046"}
EMPRESARIO_INDIVIDUAL = {"2135"}
REGRAS_PROPRIAS = {"2143": "Cooperativa", "3999": "Associação", "3069": "Fundação privada"}


def so_digitos(texto):
    return re.sub(r"\D", "", texto or "")


def formata_cnpj(c):
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"


def cnpj_valido(c):
    if len(c) != 14 or c == c[0] * 14:
        return False
    def dv(base, pesos):
        s = sum(int(d) * p for d, p in zip(base, pesos)) % 11
        return "0" if s < 2 else str(11 - s)
    d1 = dv(c[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    d2 = dv(c[:12] + d1, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return c[12:] == d1 + d2


def le_faturamento(texto):
    texto = (texto or "").strip().replace("R$", "").strip()
    if not texto:
        return None
    if "," in texto:  # formato brasileiro: 5.200.000,00
        texto = texto.replace(".", "").replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return None


def le_entrada(caminho):
    empresas = []
    with open(caminho, encoding="utf-8-sig") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            partes = re.split(r"[;\t]", linha) if (";" in linha or "\t" in linha) else linha.split(",", 1)
            cnpj = so_digitos(partes[0])
            if not cnpj:  # cabeçalho ou linha sem CNPJ
                continue
            fat = le_faturamento(partes[1]) if len(partes) > 1 else None
            empresas.append((cnpj.zfill(14), fat))
    return empresas


def consulta(cnpj):
    ultimo_erro = ""
    for modelo in FONTES:
        url = modelo.format(cnpj=cnpj)
        for tentativa in range(3):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "triagem-ebef/1.0"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    return json.loads(r.read().decode("utf-8")), url.split("/")[2]
            except urllib.error.HTTPError as e:
                ultimo_erro = f"HTTP {e.code} em {url.split('/')[2]}"
                if e.code == 404:
                    break  # CNPJ não encontrado nesta fonte
                if e.code == 429:
                    time.sleep(10 * (tentativa + 1))
                    continue
                break
            except Exception as e:  # rede, timeout, JSON inválido
                ultimo_erro = f"{type(e).__name__} em {url.split('/')[2]}"
                time.sleep(2)
    return None, ultimo_erro


def classifica(dados, faturamento):
    """Devolve (classificação, observação)."""
    natureza = str(dados.get("codigo_natureza_juridica") or "")
    qsa = dados.get("qsa") or []
    socios_pj = [s for s in qsa if s.get("identificador_de_socio") == 1]
    socios_ext = [s for s in qsa if s.get("identificador_de_socio") == 3]
    situacao = (dados.get("descricao_situacao_cadastral") or "").upper()
    obs = []
    if situacao and situacao != "ATIVA":
        obs.append(f"CNPJ com situação {situacao}: a IN alcança também entidades suspensas e inaptas")
    if socios_ext:
        obs.append("Há sócio estrangeiro: analisar cadeia no exterior")

    if natureza in EMPRESARIO_INDIVIDUAL:
        return "NÃO SE APLICA", "Empresário individual (não é sociedade)"
    if natureza in REGRAS_PROPRIAS:
        return "ANALISAR", f"{REGRAS_PROPRIAS[natureza]}: regras próprias. " + " | ".join(obs)
    if natureza in SA_ABERTA:
        return "ANALISAR", "S.A. aberta: regras próprias. " + " | ".join(obs)
    if natureza in SA_FECHADA:
        obs.insert(0, "S.A.: o QSA não mostra acionistas. Conferir no Livro de Registro de Ações se há PJ acionista")
        return "OBRIGADA (A CONFIRMAR)", " | ".join(obs)
    if natureza in LTDA_OU_SIMPLES:
        if socios_pj or socios_ext:
            return "OBRIGADA DESDE 2026", "Tem pessoa jurídica ou estrangeiro no QSA. " + " | ".join(obs)
        if faturamento is None:
            return "INFORMAR FATURAMENTO", "Só sócios PF: depende do faturamento do ano anterior. " + " | ".join(obs)
        if faturamento > LIMITE_2027:
            return "OBRIGADA A PARTIR DE 2027", "Só sócios PF, faturamento > R$ 78 mi. " + " | ".join(obs)
        if faturamento > LIMITE_2028:
            return "OBRIGADA A PARTIR DE 2028", "Só sócios PF, faturamento > R$ 4,8 mi. " + " | ".join(obs)
        return "DISPENSADA", "Só sócios PF e faturamento até R$ 4,8 mi. Reavaliar se entrar PJ no QSA. " + " | ".join(obs)
    return "ANALISAR", f"Natureza jurídica {natureza} não mapeada. " + " | ".join(obs)


COLUNAS = [
    "CNPJ", "Razão social", "Natureza jurídica", "Situação cadastral", "Faturamento informado",
    "Sócios PJ", "Sócios estrangeiros", "Sócios PF (qtde)", "Administradores",
    "Classificação e-BEF", "Observações", "Fonte", "Consultado em",
]


def linha_resultado(cnpj, fat, dados, fonte):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    fat_txt = f"{fat:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if fat is not None else ""
    if dados is None:
        return [formata_cnpj(cnpj), "", "", "", fat_txt, "", "", "", "",
                "ERRO NA CONSULTA", fonte, "", agora]
    qsa = dados.get("qsa") or []
    def nome(s):
        doc = s.get("cnpj_cpf_do_socio") or ""
        return f"{s.get('nome_socio', '')} ({doc})" if doc and "*" not in doc else s.get("nome_socio", "")
    pj = [nome(s) for s in qsa if s.get("identificador_de_socio") == 1]
    ext = [s.get("nome_socio", "") for s in qsa if s.get("identificador_de_socio") == 3]
    pf = [s for s in qsa if s.get("identificador_de_socio") == 2]
    adm = [f"{s.get('nome_socio', '')} - {s.get('qualificacao_socio', '')}" for s in qsa
           if "administrador" in (s.get("qualificacao_socio") or "").lower()
           or "diretor" in (s.get("qualificacao_socio") or "").lower()
           or "presidente" in (s.get("qualificacao_socio") or "").lower()]
    classe, obs = classifica(dados, fat)
    return [
        formata_cnpj(cnpj), dados.get("razao_social", ""),
        f"{dados.get('codigo_natureza_juridica', '')} - {dados.get('natureza_juridica', '')}",
        dados.get("descricao_situacao_cadastral", ""), fat_txt,
        " | ".join(pj), " | ".join(ext), len(pf), " | ".join(adm),
        classe, obs.strip(" |"), fonte, agora,
    ]


def main():
    ap = argparse.ArgumentParser(description="Triagem e-BEF da carteira de clientes")
    ap.add_argument("entrada", help="CSV/TXT com CNPJ;faturamento (faturamento opcional)")
    ap.add_argument("-o", "--saida", default=None, help="arquivo CSV de saída")
    args = ap.parse_args()

    empresas = le_entrada(args.entrada)
    saida = args.saida or f"triagem_ebef_{datetime.now():%Y%m%d_%H%M}.csv"
    print(f"{len(empresas)} CNPJs lidos. Consultando...")

    with open(saida, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(COLUNAS)
        for i, (cnpj, fat) in enumerate(empresas, 1):
            if not cnpj_valido(cnpj):
                w.writerow([cnpj, "", "", "", "", "", "", "", "", "CNPJ INVÁLIDO", "Dígito verificador não confere", "", ""])
                print(f"[{i}/{len(empresas)}] {cnpj}: CNPJ inválido")
                continue
            dados, fonte = consulta(cnpj)
            linha = linha_resultado(cnpj, fat, dados, fonte)
            w.writerow(linha)
            f.flush()
            print(f"[{i}/{len(empresas)}] {linha[0]} {linha[1][:40]}: {linha[9]}")
            time.sleep(PAUSA_ENTRE_CONSULTAS)
    print(f"Pronto: {saida}")


if __name__ == "__main__":
    sys.exit(main())
