# Setup E Configuracoes - Testes De Conflito

Status: contrato v0.1.
Data: 2026-05-13.

## Objetivo

Garantir que configuracoes do Taliya nao briguem entre si e que CRM/agentes sempre escolham a resposta correta quando houver conflito.

Este documento nao e teste tecnico automatizado ainda. Ele e a suite funcional minima que deve virar testes de produto, aceite e QA antes de liberar setup, reconfiguracao, agentes e autonomia.

## Regra central

Quando duas regras entram em conflito, o sistema nao deve "adivinhar" pela ultima resposta do usuario nem pelo agente.

Ele deve aplicar a precedencia definida em:

- `setup-source-of-truth-precedence.pt-BR.md`;
- `setup-configuration-integrity-contract.pt-BR.md`;
- `setup-consumption-contract-crm-agents.pt-BR.md`;
- `permissions-matrix.pt-BR.md`;
- `agent-guardrails-evals-contract.pt-BR.md`;
- `quota-touchpoints.pt-BR.md`.

## Resultado visual esperado

Todo conflito relevante precisa aparecer em pelo menos um destes formatos:

- bloqueio explicito no setup;
- aviso no painel de impacto;
- status no drawer da origem;
- tarefa/checklist de pendencia;
- aprovacao pendente;
- incidente quando houver falha operacional;
- auditoria com motivo e regra vencedora.

## Suite minima de conflitos

| ID | Conflito | Regra vencedora | Resultado esperado |
|---|---|---|---|
| C01 | Aluno sem consentimento/opt-out vs agente autorizado a enviar mensagem | Privacidade/legal | Bloquear envio externo, explicar motivo, permitir tarefa manual interna e auditar. |
| C02 | Usuario sem permissao vs politica permite acao | Permissao | Bloquear acao, oferecer solicitar aprovacao ou trocar responsavel. |
| C03 | Plano Taliya com 0 agentes vs fluxo de agente configurado | Plano/entitlement | CRM segue manual; fluxo fica bloqueado por plano com CTA de upgrade, sem quebrar rotina. |
| C04 | Cota de mensagens/IA esgotada vs fluxo autonomo ativo | Cota | Pausar acao paga/externa, mostrar cota, permitir fallback manual sem consumo indevido. |
| C05 | WhatsApp desconectado vs modelo de mensagem aprovado e pacote de agente em rascunho | Integracao/canal | Bloquear envio externo, criar pendencia de integracao, manter rascunho ou tarefa manual. |
| C06 | Reposicao permitida vs aluno inadimplente e politica bloqueia beneficios | Politica operacional/financeiro | Bloquear encaixe autonomo, sugerir revisao manual ou aprovacao de excecao. |
| C07 | Credito de aula expirado vs gestor quer "quebrar galho" | Excecao auditavel do aluno | Permitir apenas com permissao, motivo, impacto no consumo e auditoria. |
| C08 | Fluxo recomendado como futuro autonomo vs politica sensivel nao publicada | Politica operacional | No setup inicial, criar rascunho/pendencia para Agentes/Fluxos; autonomia so pode ser avaliada depois com politica publicada. |
| C09 | Regra antiga usada em execucao vs regra nova publicada depois | Snapshot da execucao | Execucao antiga preserva snapshot; proximas execucoes usam regra nova. |
| C10 | Importacao trouxe dado divergente vs dado corrigido manualmente | Edicao manual validada | Edicao validada vence; divergencia vai para fila de qualidade de dados. |
| C11 | Telefone compartilhado por dois alunos vs mensagem entrante | Identidade/privacidade | Nao atualizar aluno automaticamente; abrir revisao de identidade. |
| C12 | Downgrade de plano Taliya vs agentes ja ativos | Plano/entitlement | Pausar agentes fora do plano, preservar historico e manter CRM manual. |
| C13 | Usuario financeiro tenta ver dado restrito de aluno | Permissao/sensibilidade | Mostrar apenas o necessario para acao financeira; ocultar dado restrito. |
| C14 | Template aprovado vs janela de envio fechada | Politica de canal | Agendar, criar tarefa ou pedir aprovacao; nao enviar fora da janela. |
| C15 | Fluxo autonomo sem dono de fallback | Fallback humano obrigatorio | Bloquear autonomia ate definir fila/responsavel de fallback. |
| C16 | Agente sugere desconto vs politica exige aprovacao | Politica financeira | Criar aprovacao; nao enviar proposta nem alterar cobranca sozinho. |
| C17 | Aula cheia vs aluno tem prioridade de reposicao | Capacidade/turma | Bloquear encaixe direto; oferecer lista de espera ou alternativas. |
| C18 | Pagamento marcado como pago manualmente vs comprovante divergente | Evidencia financeira | Pedir conciliacao/revisao; nao confirmar automaticamente. |
| C19 | Reclamacao aberta vs automacao de retencao ativa | Caso sensivel | Pausar automacoes externas sobre o aluno ate resolucao/liberacao. |
| C20 | Pedido LGPD/privacidade vs campanha ou comunicacao agendada | Privacidade/legal | Remover do envio, registrar bloqueio e revisar dados vinculados. |

## Criterios por teste

Cada teste so passa quando:

1. a regra vencedora esta clara;
2. a tela mostra o motivo em linguagem de negocio;
3. o CRM continua operavel quando possivel;
4. o agente nao consegue burlar bloqueio via prompt;
5. a acao manual segura continua disponivel quando fizer sentido;
6. a auditoria registra regra, usuario/agente, data, objeto e resultado;
7. a mudanca nao cria duplicidade de configuracao.

## Comportamento por modo

| Modo | Comportamento esperado em conflito |
|---|---|
| Manual | Usuario ve bloqueio/alerta e pode agir se tiver permissao. |
| Copiloto | Agente explica e sugere caminho seguro, mas nao executa acao bloqueada. |
| Autonomo | Agente para, aplica fallback, cria tarefa/aprovacao/incidente quando previsto. |

## Comportamento por quantidade de agentes

| Plano | Resultado esperado |
|---|---|
| 0 agentes | Todos os conflitos ainda funcionam no CRM manual. |
| 1 agente | Apenas fluxos do agente contratado podem sugerir/agir, respeitando bloqueios. |
| 3 agentes | Conflitos podem atravessar areas, mas cada dominio respeita seu dono de regra. |
| 7 agentes | Autonomia maior exige mais preflight, snapshot, fallback e auditoria. |

## Nao negociavel

Nenhum conflito pode ser resolvido somente por texto de prompt.

A decisao precisa estar no motor do sistema: permissoes, politicas, cotas, entitlements, integracoes, snapshots e auditoria.
