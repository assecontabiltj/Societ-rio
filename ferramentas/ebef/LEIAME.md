# Triagem e-BEF da carteira

Consulta o QSA de todos os CNPJs dos clientes numa base pública do CNPJ e indica quais empresas precisam entregar o e-BEF (IN RFB 2.119/2022, com a redação da IN RFB 2.290/2025).

## Como usar

1. Instale o **Python 3** (python.org). No Windows, marque "Add Python to PATH" na instalação.
2. Preencha o `modelo_clientes.csv` no Excel: uma linha por empresa, com o **CNPJ** e, se souber, o **faturamento do ano anterior**. Salve como CSV.
3. No terminal (Prompt de Comando), dentro desta pasta, rode:

   ```
   python triagem_ebef.py modelo_clientes.csv
   ```

4. O resultado sai em `triagem_ebef_AAAAMMDD_HHMM.csv`, que abre direto no Excel.

O script faz uma consulta a cada 1,5 segundo para não ser bloqueado pelas APIs públicas. Com 300 clientes, leva cerca de 8 minutos.

## O que significa cada classificação

| Classificação | Significado |
|---|---|
| OBRIGADA DESDE 2026 | Ltda ou sociedade simples com pessoa jurídica ou estrangeiro no QSA |
| OBRIGADA A PARTIR DE 2027 | Só sócios PF e faturamento acima de R$ 78 milhões |
| OBRIGADA A PARTIR DE 2028 | Só sócios PF e faturamento acima de R$ 4,8 milhões |
| DISPENSADA | Só sócios PF e faturamento até R$ 4,8 milhões |
| INFORMAR FATURAMENTO | Só sócios PF, mas o faturamento não foi informado |
| OBRIGADA (A CONFIRMAR) | S.A. fechada: o QSA não mostra acionistas, então é preciso conferir no Livro de Registro de Ações |
| ANALISAR | Cooperativa, associação, fundação, S.A. aberta ou natureza jurídica não mapeada |
| NÃO SE APLICA | Empresário individual |
| ERRO NA CONSULTA / CNPJ INVÁLIDO | Conferir o CNPJ ou rodar de novo mais tarde |

## Limites

- O script **não calcula quem é o beneficiário final**: ele só separa quais empresas precisam declarar. A análise da cadeia societária (holdings, participação indireta, acordo de sócios, administradores) continua sendo feita caso a caso.
- A base pública pode ter alguns dias de atraso em relação ao cadastro da Receita.
- O faturamento não está no CNPJ; ele vem da planilha de entrada.
- As regras de S.A. só com acionistas PF não foram confirmadas no texto oficial; por isso aparecem como "a confirmar".
