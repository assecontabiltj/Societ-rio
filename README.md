# 57 Agents Contabilidade — Subagentes Claude Code

Subagentes especialistas nas rotinas de um escritório contábil brasileiro, do
pacote **57 Agents Contabilidade** (Bravy / ASV Digital). Cada agente cobre uma
rotina específica — apuração, obrigações acessórias, folha, conciliação,
fechamento, atendimento, societário, contencioso — e é acionado quando o
contexto da conversa bate com a especialidade.

Os 57 agentes estão em [`.claude/agents/`](.claude/agents/).

## Uso

Os agentes já estão em `.claude/agents/`, então basta abrir o Claude Code neste
repositório — não há passo de ativação. O Claude Code carrega os arquivos de
`.claude/agents/` ao iniciar.

> O comando `/agents` **não existe mais** (o wizard foi removido). Se a
> documentação do pacote mandar confirmar por ele, ignore: para conferir se
> carregou, basta pedir uma tarefa da especialidade e ver o agente ser acionado.

**Modo automático** — são acionados sozinhos quando a tarefa descrita bate com a
especialidade.

**Modo manual:**

```
> use o agente apuracao-simples-nacional para [tarefa]
```

**Em pipeline** — encadeiam entre si:

```
cadastro-nf → conciliacao-bancaria → fechamento-mensal → relatorio-mensal → cobranca-honorarios
abertura-empresa-cnpj → alteracao-contratual → encerramento-empresa-baixa
```

### Instalação global (todos os projetos)

```bash
mkdir -p ~/.claude/agents
cp .claude/agents/*.md ~/.claude/agents/
```

## Catálogo

### 1 · Apuração & Tributário

| Agente | Arquivo | Cobre |
|---|---|---|
| `apuracao-simples-nacional` | [01](.claude/agents/01-apuracao-simples-nacional.md) | DAS mensal, PGDAS-D, alíquota efetiva, anexos e fator R |
| `icms-iss` | [02](.claude/agents/02-icms-iss.md) | ICMS (LC 87/96, CONFAZ, legislação estadual) e ISS (LC 116/2003, legislação municipal) |
| `pis-cofins` | [03](.claude/agents/03-pis-cofins.md) | Regime cumulativo e não-cumulativo, créditos e monofásicos |
| `irpj-csll` | [04](.claude/agents/04-irpj-csll.md) | Lucro Presumido e Lucro Real, adicional de 10%, LALUR |
| `conferencia-guia` | [05](.claude/agents/05-conferencia-guia.md) | Conferência cruzada de guias × declarações antes do envio ao cliente |

### 2 · Obrigações Acessórias

| Agente | Arquivo | Cobre |
|---|---|---|
| `sped-fiscal` | [06](.claude/agents/06-sped-fiscal.md) | EFD-ICMS-IPI: escrituração, apuração e blocos obrigatórios |
| `ecf-ecd` | [07](.claude/agents/07-ecf-ecd.md) | ECD (IN RFB 2.003/2021) e ECF (IN RFB 2.004/2021) |
| `dctfweb` | [08](.claude/agents/08-dctfweb.md) | Confissão de débitos federais, vinculação de DARFs e PER/DCOMP |
| `efd-reinf` | [09](.claude/agents/09-efd-reinf.md) | Eventos R-1000 a R-4080, retenções e fechamento periódico |
| `esocial` | [10](.claude/agents/10-esocial.md) | Os 5 grupos de eventos (S-1000 a S-5000) |

### 3 · Folha & Departamento Pessoal

| Agente | Arquivo | Cobre |
|---|---|---|
| `holerite` | [11](.claude/agents/11-holerite.md) | Proventos, descontos e conferência do recibo de pagamento |
| `ferias-13-salario` | [12](.claude/agents/12-ferias-13-salario.md) | Período aquisitivo, abono pecuniário, parcelamento e 13º em duas parcelas |
| `rescisao-clt-calculo` | [13](.claude/agents/13-rescisao-clt-calculo.md) | Verbas por motivo de desligamento, inclusive acordo do art. 484-A |
| `inss-fgts` | [14](.claude/agents/14-inss-fgts.md) | CPP, RAT/GILRAT, Terceiros, FGTS e desoneração |
| `admissao` | [15](.claude/agents/15-admissao.md) | Documentos, ASO, CTPS Digital e eventos de admissão |

### 4 · Conciliação & Financeiro

| Agente | Arquivo | Cobre |
|---|---|---|
| `conciliacao-bancaria` | [16](.claude/agents/16-conciliacao-bancaria.md) | Match extrato (OFX/CSV/PDF) × razão, tarifas, IOF e pendências |
| `cobranca-honorarios` | [17](.claude/agents/17-cobranca-honorarios.md) | Régua de cobrança, mora (CC 397) e título executivo (CPC 784 III) |
| `dre-gerencial` | [18](.claude/agents/18-dre-gerencial.md) | Custos fixos × variáveis, margem de contribuição e ponto de equilíbrio |
| `fluxo-caixa-projetado` | [19](.claude/agents/19-fluxo-caixa-projetado.md) | Fluxo direto realizado e projetado em 3 cenários |

### 5 · Atendimento ao Cliente

| Agente | Arquivo | Cobre |
|---|---|---|
| `triagem-whatsapp` | [20](.claude/agents/20-triagem-whatsapp.md) | Classificação por urgência e área, com resposta sugerida |
| `documentos-pendentes` | [21](.claude/agents/21-documentos-pendentes.md) | Controle do que falta o cliente enviar para fechar o período |
| `onboarding-cliente` | [22](.claude/agents/22-onboarding-cliente.md) | Contrato, procuração e-CAC e implantação do cliente novo |
| `follow-up-cliente` | [23](.claude/agents/23-follow-up-cliente.md) | Atualização pós-fechamento e reunião de planejamento |

### 6 · Operação Interna

| Agente | Arquivo | Cobre |
|---|---|---|
| `cadastro-nf` | [24](.claude/agents/24-cadastro-nf.md) | Classificação de NF-e, NFS-e, NFC-e e CT-e para escrituração |
| `lembrete-prazo` | [25](.claude/agents/25-lembrete-prazo.md) | Calendário fiscal mensal e anual do escritório |
| `relatorio-mensal` | [26](.claude/agents/26-relatorio-mensal.md) | Síntese de KPIs entregue ao cliente |
| `backup-escritorio` | [27](.claude/agents/27-backup-escritorio.md) | Política e rotina de backup dos arquivos do escritório |

### 7 · Especializações por área

**Tributário**

| Agente | Arquivo | Cobre |
|---|---|---|
| `apuracao-mei` | [28](.claude/agents/28-apuracao-mei.md) | DAS-MEI, DASN-SIMEI, limite e desenquadramento |
| `calculo-ipi` | [29](.claude/agents/29-calculo-ipi.md) | TIPI, suspensão, crédito presumido de exportação e Bloco K |
| `calculo-irrf-folha` | [30](.claude/agents/30-calculo-irrf-folha.md) | IRRF de folha, pró-labore, RPA e pagamentos PJ→PF |
| `retencoes-tributarias-tomador` | [31](.claude/agents/31-retencoes-tributarias-tomador.md) | IRRF, CSRF, INSS e ISS retidos pelo tomador |

**Obrigações**

| Agente | Arquivo | Cobre |
|---|---|---|
| `efd-contribuicoes` | [32](.claude/agents/32-efd-contribuicoes.md) | CSTs, Bloco M, F500/F600 e CPRB |
| `dimob` | [33](.claude/agents/33-dimob.md) | DIMOB de imobiliárias, construtoras e administradoras |
| `dmed` | [34](.claude/agents/34-dmed.md) | DMED de prestadores de serviços de saúde e operadoras |

**Folha**

| Agente | Arquivo | Cobre |
|---|---|---|
| `folha-pagamento-mensal` | [35](.claude/agents/35-folha-pagamento-mensal.md) | Folha CLT completa: adicionais, descontos, FGTS e CCT |

**Contábil**

| Agente | Arquivo | Cobre |
|---|---|---|
| `plano-contas-cpc` | [36](.claude/agents/36-plano-contas-cpc.md) | Plano de contas com mapeamento referencial e aderência aos CPCs |
| `lancamentos-contabeis-padrao` | [37](.claude/agents/37-lancamentos-contabeis-padrao.md) | Catálogo de lançamentos D/C das operações cotidianas |

**Conciliação**

| Agente | Arquivo | Cobre |
|---|---|---|
| `conciliacao-cartoes-credenciadora` | [38](.claude/agents/38-conciliacao-cartoes-credenciadora.md) | Repasses de credenciadoras, MDR, antecipação e chargebacks |
| `conciliacao-fornecedores` | [39](.claude/agents/39-conciliacao-fornecedores.md) | Razão de contas a pagar, duplicidades e adiantamentos |
| `conciliacao-clientes` | [40](.claude/agents/40-conciliacao-clientes.md) | Razão de contas a receber, aging e PCLD |

**Fechamento**

| Agente | Arquivo | Cobre |
|---|---|---|
| `fechamento-mensal` | [41](.claude/agents/41-fechamento-mensal.md) | Roteiro de fechamento em até 5 dias úteis |
| `balancete-analise` | [42](.claude/agents/42-balancete-analise.md) | Integridade, coerência e variações do balancete |
| `ativo-imobilizado-depreciacao` | [43](.claude/agents/43-ativo-imobilizado-depreciacao.md) | Reconhecimento, depreciação e baixa (CPC 27) |

**Análise estratégica**

| Agente | Arquivo | Cobre |
|---|---|---|
| `analise-tributaria-regime` | [44](.claude/agents/44-analise-tributaria-regime.md) | Simples × Presumido × Real com projeção de 12 meses |
| `recuperacao-creditos-pis-cofins` | [45](.claude/agents/45-recuperacao-creditos-pis-cofins.md) | Créditos retroativos de 5 anos (Tema 69 STF, Tema 779 STJ) |
| `revisao-fiscal-cruzamento-sped` | [46](.claude/agents/46-revisao-fiscal-cruzamento-sped.md) | Cruzamento ECD × ECF × EFDs × eSocial × Reinf × DCTFWeb |

**Malha fina**

| Agente | Arquivo | Cobre |
|---|---|---|
| `malha-fina-pf-diagnostico` | [47](.claude/agents/47-malha-fina-pf-diagnostico.md) | Diagnóstico da malha do IRPF e retificadora |
| `malha-fina-pj-diagnostico` | [48](.claude/agents/48-malha-fina-pj-diagnostico.md) | TIF, Comunicado de Inconsistência, Auto de Infração, Despacho Decisório |

**Consultoria**

| Agente | Arquivo | Cobre |
|---|---|---|
| `due-diligence-contabil` | [49](.claude/agents/49-due-diligence-contabil.md) | Passivos ocultos, contingências (CPC 25) e Quality of Earnings |
| `valuation-pme` | [50](.claude/agents/50-valuation-pme.md) | DCF, múltiplos comparáveis e valor patrimonial |

**IR Pessoa Física**

| Agente | Arquivo | Cobre |
|---|---|---|
| `irpf-declaracao-completa` | [51](.claude/agents/51-irpf-declaracao-completa.md) | Múltiplas fontes, Simplificada × Completa, ganho de capital e exterior |

**Societário**

| Agente | Arquivo | Cobre |
|---|---|---|
| `abertura-empresa-cnpj` | [52](.claude/agents/52-abertura-empresa-cnpj.md) | Abertura via REDESIM: viabilidade, DBE, contrato social (CC 997), Junta Comercial, inscrições e opção tributária |
| `alteracao-contratual` | [53](.claude/agents/53-alteracao-contratual.md) | Entrada/saída de sócios, capital, objeto/CNAE, endereço, transformação societária |
| `encerramento-empresa-baixa` | [54](.claude/agents/54-encerramento-empresa-baixa.md) | Baixa regular ou com débito, distrato, encerramento contábil e declarações fracionadas |

**Contencioso fiscal**

| Agente | Arquivo | Cobre |
|---|---|---|
| `parcelamento-receita-federal` | [55](.claude/agents/55-parcelamento-receita-federal.md) | Ordinário, simplificado e transação tributária (Lei 13.988/2020) |
| `resposta-fiscalizacao-intimacao` | [56](.claude/agents/56-resposta-fiscalizacao-intimacao.md) | Resposta a TIF, impugnação ao DRJ e defesa administrativa |

**Reforma Tributária**

| Agente | Arquivo | Cobre |
|---|---|---|
| `reforma-tributaria-cbs-ibs` | [57](.claude/agents/57-reforma-tributaria-cbs-ibs.md) | CBS e IBS (EC 132/2023 + LC 214/2025), transição e split payment |

## Boas práticas

- **Contexto é tudo.** Quanto mais dados (números, datas, nomes), melhor a entrega.
- **Não dispense a revisão.** O agente entrega rascunho profissional — a revisão
  final é obrigatória antes de transmitir, declarar ou pagar.
- **Combine agentes.** Funcionam em pipeline entre si.
  Catálogo completo: https://github.com/asv-digital/agents-contabilidade

## Avisos legais

- Os agentes refletem CTN, RIR/2018, IN RFB, LC 87/96, LC 116/2003, LC 123/2006,
  LC 190/2022, EC 132/2023 (Reforma Tributária), Resolução CFC 1.546/2024 e
  legislação especial vigentes em 2026.
- Outputs gerados são **rascunhos**; o contador responsável deve revisar e assumir
  a responsabilidade técnica (CRC, Resolução CFC 1.546/2024).
- Templates e exemplos usam dados fictícios.

## Licença

Uso permitido para clientes ASV Digital / Bravy. Não redistribuir.
Suporte: produtos@asv.digital
