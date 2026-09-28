# Setup E Configuracoes - Auditoria Final V0.1

Status: auditoria final v0.1.
Data: 2026-05-13.

## Conclusao curta

Estamos no caminho certo, com uma correcao importante: o setup nao tem dois modos funcionais.

Existe um unico setup guiado por agente. O studio pode seguir sozinho com o agente ou agendar uma chamada com humano Taliya para acompanhar o mesmo fluxo. A configuracao real continua sendo feita pelo sistema, com validacao, impacto, aprovacao, publicacao e auditoria.

## O que ficou definido

### Papel de cada camada

| Camada | Papel |
|---|---|
| Gestor | Informa como o studio funciona, revisa e aprova. |
| Agente de setup | Guia, pergunta, explica, detecta contradicao e prepara rascunho. |
| Humano Taliya | Acompanha e orienta quando houver chamada, sem configurar por fora. |
| Sistema | Transforma respostas em configuracao, valida, publica e audita. |
| CRM | Consome configuracao publicada para operar. |
| Agentes operacionais | Consomem configuracao publicada e respeitam plano, cota, permissao e politica. |
| Configuracao de fluxos | Acontece depois do setup inicial, em Agentes/Fluxos, com o mesmo agente de configuracao guiando o usuario. |
| Control planes | Monitoram execucao, falha, bloqueio, uso, incidente e auditoria; nao substituem configuracao de fluxo. |

### Fonte da verdade

Configuracao nao pode morar em prompt, conversa, imagem ou anotacao solta.

Ela precisa morar em regra estruturada, versionada e publicada.

### Publicacao parcial

O setup pode publicar:

- CRM manual;
- Agenda;
- Financeiro;
- Canais/modelos de mensagem;
- Regras de seguranca/aprovacoes;
- Agentes preparados em nivel superficial;
- Rascunhos/pendencias de fluxos recomendados.

Modo manual/copiloto/autonomo, limites, cotas por fluxo, aprovacoes por acao, fallback detalhado, simulacao final e publicacao de fluxo autonomo pertencem a Agentes/Fluxos pos-go-live.

Automacao autonoma e a ultima camada e so entra depois, quando preflight, permissao, plano, cota, regra de seguranca, canal, fallback e auditoria estiverem corretos.

### 0 agentes

O plano Base com 0 agentes continua sendo CRM completo:

- manual;
- programatico quando seguro;
- sem execucao de agentes;
- sem travar rotinas essenciais.

## Documentos que agora fecham a arquitetura

- `onboarding-setup-modes.pt-BR.md`
- `setup-configuration-plan-100.pt-BR.md`
- `setup-configuration-integrity-contract.pt-BR.md`
- `setup-configuration-inventory.pt-BR.md`
- `setup-technical-configuration-contract.pt-BR.md`
- `setup-source-of-truth-precedence.pt-BR.md`
- `setup-consumption-contract-crm-agents.pt-BR.md`
- `setup-agent-role.pt-BR.md`
- `configuration-agent-transversal-contract.pt-BR.md`
- `setup-onboarding-question-map.pt-BR.md`
- `setup-adaptive-decision-tree.pt-BR.md`
- `setup-impact-matrix.pt-BR.md`
- `setup-billing-class-consumption-models.pt-BR.md`
- `setup-partial-publishing-rules.pt-BR.md`
- `setup-reconfiguration-rules.pt-BR.md`
- `setup-conflict-tests.pt-BR.md`
- `setup-scenario-tests.pt-BR.md`
- `setup-acceptance-criteria.pt-BR.md`
- `setup-screens-blueprint.pt-BR.md`
- `setup-image-plan.pt-BR.md`

## Auditoria contra riscos principais

| Risco | Status |
|---|---|
| Setup virar dois produtos separados | Resolvido: fluxo unico, chamada humana opcional. |
| Agente virar fonte da verdade | Resolvido: agente guia; sistema valida/publica. |
| CRM depender de IA | Resolvido: 0 agentes continua completo. |
| Regra duplicada entre paginas | Mitigado com fonte da verdade e precedencia. |
| Autonomia sem guardrail | Mitigado com preflight, cota, permissao, politica e fallback. |
| Setup configurando fluxo profundo cedo demais | Resolvido: setup prepara agentes e rascunhos; configuracao profunda fica em Agentes/Fluxos pos-go-live. |
| Control Plane confundido com builder de fluxo | Resolvido: Control Planes monitoram/governam execucao, nao configuram fluxo do zero. |
| Financeiro confundir billing Taliya | Mitigado: financeiro do studio separado de billing Taliya. |
| Consumo de aula ficar ambiguo | Mitigado: modelo de cobranca separado de consumo/reposicao. |
| Reconfiguracao pos-setup quebrar fluxo ativo | Mitigado: diff, simulacao, snapshot e publicacao. |
| Cotas serem esquecidas | Mitigado: consumo por CRM/agentes e uso/cotas no setup. |
| Chamada humana criar configuracao por fora | Resolvido: humano apenas acompanha dentro do fluxo. |

## Auditoria contra fluxos/casos/paginas

### Hoje, tarefas, checklists e aprovacoes

Configura:

- quem recebe tarefas;
- quando algo vira aprovacao;
- quem aprova;
- quando item vira tarefa manual, sugestao de copiloto ou execucao automatizada conforme fluxo ja configurado;
- quais alertas entram no Hoje.

Status: coberto.

### Inbox e comunicacao

Configura:

- canais;
- consentimento/opt-out;
- templates;
- janelas de envio;
- handoff humano;
- falhas de envio.

Status: coberto.

### Agenda, aulas, turmas e reposicoes

Configura:

- regras de aula;
- chamada;
- no-show;
- creditos;
- reposicao;
- encaixe;
- lista de espera;
- fallback manual.

Status: coberto, com dependencia do detalhamento visual da familia Agenda que esta sendo resolvida em outra conversa.

### Financeiro

Configura:

- modelo de cobranca;
- vencimentos;
- canais de pagamento;
- conciliacao;
- cobrancas recorrentes;
- excecoes e quebra-galhos;
- limites de agente.

Status: coberto.

### Retencao, cancelamento, reativacao e reclamacao

Configura:

- quando automacao pausa;
- quando caso sensivel exige humano;
- quem responde;
- quais mensagens sao permitidas;
- quando criar tarefa/aprovacao.

Status: coberto.

### Agentes, fluxos e cotas

Configura:

- agentes disponiveis por plano;
- agentes preparados no setup;
- pacotes de fluxos recomendados como rascunho;
- configuracao profunda de modo, preflight, cotas por fluxo e fallback em Agentes/Fluxos pos-go-live;
- uso/cotas em Control Plane;
- incidentes;
- auditoria.

Status: coberto.

## O que ainda fica aberto de forma consciente

Estas decisoes nao bloqueiam a arquitetura, mas precisam ser refinadas antes de implementar defaults finais:

1. Presets exatos para studios de Pilates.
2. Textos finais das perguntas do setup.
3. Thresholds de risco para recomendar chamada humana.
4. Defaults sugeridos para rascunhos de fluxo e defaults finais de autonomia definidos em Agentes/Fluxos.
5. Provedores financeiros do MVP.
6. Regras finas de comunicacao por canal.
7. Visual final das imagens 4.1J.

## Decisao final v0.1

A arquitetura de setup/configuracoes esta consistente para seguir para a familia visual 4.1J.

Nao ha necessidade de inventar novas familias agora. O proximo passo correto e desenhar as imagens de setup/configuracoes usando o blueprint e o plano de imagens, validando cada uma antes de documentar.
