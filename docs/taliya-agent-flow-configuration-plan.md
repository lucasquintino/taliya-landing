# Taliya Agent Flow Configuration Plan

## Objetivo

Transformar o mapa final de fluxos dos agentes em configuracoes por studio, sem permitir que cada cliente redesenhe a operacao do zero.

O resultado esperado e:

- todos os agentes revisados;
- todos os fluxos com dono, canal, autonomia e estados finais;
- todos os fluxos com configuracoes disponiveis;
- todos os fluxos com cenarios de teste;
- todos os riscos sensiveis com handoff;
- todas as transicoes apontando para fluxos reais;
- todas as acoes caras com regra de economia de creditos.

## Artefatos Fonte

- `docs/taliya-agent-flow-deep-map.md`
- `docs/taliya-agent-flow-validation-matrix.md`

## Artefatos Criados Nesta Etapa

- `docs/taliya-agent-flow-config-template.md`
- `docs/taliya-agent-flow-configuration-matrix.md`
- `docs/taliya-agent-flow-test-scenarios.md`

## Ordem De Fechamento

1. Travar o template unico de fluxo.
2. Aplicar o template a todos os fluxos dos 7 agentes.
3. Criar cenarios de teste por agente.
4. Auditar consistencia entre mapa, validacao, configuracao e testes.
5. Corrigir lacunas encontradas.
6. Usar a matriz para desenhar as telas/configuracoes do studio.

## Responsabilidades Dos Agentes

| Agente | Responsabilidade Final |
| --- | --- |
| Atendimento | Entrada, classificacao, respostas permitidas, consentimento, identidade e handoff. |
| Agenda | Presenca, faltas, reposicoes, vagas, horarios, grade, conflitos e primeira aula. |
| Vendas | Interessado, valores, experimental, follow-up, pre-matricula, checkout, perda e upsell. |
| Financeiro | Vencimento, pagamento, link/Pix, comprovante, contrato, bloqueio, cortesias e fechamento. |
| Retencao | Risco, inatividade, retorno, cancelamento, ex-alunos, satisfacao e campanhas de retencao. |
| Gestao | Prioridades, dinheiro na mesa, fila humana, gargalos, setup, creditos, auditoria e falhas. |
| Historico/Evolucao | Contexto interno, observacoes, restricoes, documentos, permissoes e linha do tempo. |

## Definicao De Pronto Para Um Fluxo

Um fluxo so pode ir para configuracao quando tiver:

- dono unico;
- canal de nascimento;
- canal de execucao;
- local de registro;
- autonomia padrao;
- trigger;
- dados obrigatorios;
- caminho quando falta dado;
- subfluxos de sucesso;
- subfluxos de espera;
- subfluxos de excecao;
- estados finais padronizados;
- transicoes permitidas;
- pontos de handoff;
- regra de economia de creditos;
- logs/auditoria obrigatorios;
- configuracoes disponiveis para o studio;
- cenarios de teste.

## Definicao De Pronto Para Um Agente

Um agente esta pronto quando:

- todos os seus fluxos passam na definicao de pronto;
- nao existem fluxos duplicados com outro agente;
- as transicoes para outros agentes estao claras;
- riscos sensiveis nunca ficam em modo autonomo livre;
- todo fluxo externo pelo WhatsApp tem limite, janela e opt-out;
- todo fluxo interno tem responsavel, tarefa ou estado final.

## Regras De Configuracao

- O studio pode ativar/desativar fluxos, mas nao redesenhar a estrutura principal.
- O studio escolhe o modo de operacao de cada fluxo: manual, copiloto ou autonomo.
- O studio define ate onde o autonomo vai em cada fluxo e o que acontece depois: parar, criar tarefa, pedir aprovacao, chamar responsavel ou mover para outro fluxo.
- O studio pode ajustar tom, templates, responsaveis, horarios, limites e criterios de aprovacao sem mexer no desenho principal do fluxo.
- WhatsApp pago, campanhas, reativacao e tentativas externas sao consequencias do modo escolhido por fluxo, nao decisoes globais do agente ou do studio.
- Configuracoes globais existem apenas como teto de seguranca: limite mensal, modo economia, horarios gerais, opt-out, permissoes e responsaveis padrao.
- Cada fluxo explica de onde o custo pode vir: IA, WhatsApp service, WhatsApp utility, WhatsApp marketing, jobs em lote, midias ou historico.
- O studio nao pode remover guardrails de saude, LGPD, financeiro critico, reputacao ou dados conflitantes.
- O studio nao pode permitir campanhas/lotes sem aprovacao explicita.
- O studio nao pode fazer o agente conceder desconto, reembolso, cortesia ou bloqueio sozinho.

## Modelo De Configuracao Por Fluxo

Cada fluxo deve explicitar:

- modo manual, copiloto e/ou autonomo;
- o que muda no comportamento e no custo em cada modo;
- ate onde o autonomo vai;
- o que acontece depois do limite;
- se pode iniciar conversa paga ou apenas responder conversa aberta pelo contato;
- quando a mensagem tende a ser service, utility ou marketing;
- se campanha/lote/reativacao ficam em copiloto ou manual;
- limite de tentativas por pessoa;
- limite de gasto/creditos do fluxo;
- origem do custo estimado;
- prioridade quando o modo economia estiver ativo;
- aprovador obrigatorio quando houver custo alto, lote, risco ou baixa confianca;
- proximo fluxo quando a pessoa responde, ignora, pede humano ou entra em excecao.

## Ordem Recomendada De Configuracao No Produto

1. Studio base
   - unidade, horarios, canais, equipe, responsaveis, planos, regras, tom global.
2. Atendimento
   - entrada, classificacao, consentimento, identidade e handoff.
3. Agenda
   - grade, presenca, falta, reposicao, lista, experimental e conflitos.
4. Vendas
   - politica de preco, experimental, follow-up, pre-matricula e checkout.
5. Financeiro
   - vencimentos, links, comprovantes, excecoes e contratos.
6. Retencao
   - risco, inatividade, retorno, cancelamento e reativacao.
7. Historico/Evolucao
   - contexto, notas, restricoes, documentos e permissao.
8. Gestao
   - prioridades, fila humana, credito, auditoria, setup e relatorios.

## Gates Antes De Ativar Um Fluxo

| Gate | Bloqueia Ativacao Quando |
| --- | --- |
| Dados obrigatorios | falta regra, plano, horario, responsavel ou canal. |
| Risco | fluxo sensivel esta marcado como autonomo livre. |
| Canal | fluxo externo nao tem janela, opt-out ou template aprovado. |
| Custo | fluxo caro nao mostra origem do custo nem limite de tentativas/creditos. |
| Alcance | modo autonomo nao define ate onde vai e o que acontece depois. |
| Responsavel | handoff nao tem fila ou responsavel. |
| Teste | simulacao basica falha. |

## Resultado Esperado Para A Landing

Depois dessa etapa, a landing pode afirmar com seguranca:

- os agentes seguem fluxos prontos;
- cada studio configura como eles se comportam;
- a equipe continua no controle;
- Taliya economiza creditos automaticamente;
- o sistema sabe quando agir, quando sugerir e quando chamar humano.

