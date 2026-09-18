# Societário — Subagentes Claude Code

Subagentes especialistas no ciclo de vida societário de uma empresa, do pacote
**57 Agents Contabilidade** (Bravy / ASV Digital).

## Agentes instalados

| Agente | Arquivo | Cobre |
|---|---|---|
| `abertura-empresa-cnpj` | [.claude/agents/52-abertura-empresa-cnpj.md](.claude/agents/52-abertura-empresa-cnpj.md) | Abertura via REDESIM: viabilidade, DBE, contrato social (CC 997), Junta Comercial, inscrições e opção tributária |
| `alteracao-contratual` | [.claude/agents/53-alteracao-contratual.md](.claude/agents/53-alteracao-contratual.md) | Entrada/saída de sócios, capital, objeto/CNAE, endereço, transformação societária |
| `encerramento-empresa-baixa` | [.claude/agents/54-encerramento-empresa-baixa.md](.claude/agents/54-encerramento-empresa-baixa.md) | Baixa regular ou com débito, distrato, encerramento contábil e declarações fracionadas |

Os três se encadeiam: abertura → alteração → encerramento, e escalam entre si
quando a demanda muda de fase.

## Uso

Os agentes já estão em `.claude/agents/`, então basta abrir o Claude Code neste
repositório. Confirme com `/agents`.

**Modo automático** — são acionados sozinhos quando a tarefa descrita bate com a
especialidade.

**Modo manual:**

```
> use o agente abertura-empresa-cnpj para [tarefa]
```

### Instalação global (todos os projetos)

```bash
mkdir -p ~/.claude/agents
cp .claude/agents/*.md ~/.claude/agents/
```

## Boas práticas

- **Contexto é tudo.** Quanto mais dados (números, datas, nomes), melhor a entrega.
- **Não dispense a revisão.** O agente entrega rascunho profissional — a revisão
  final é obrigatória antes de transmitir, declarar ou pagar.
- **Combine agentes.** Funcionam em pipeline com os demais do pacote.
  Catálogo completo: https://github.com/asv-digital/agents-contabilidade

## Licença

Uso permitido para clientes ASV Digital / Bravy. Não redistribuir.
Suporte: produtos@asv.digital
