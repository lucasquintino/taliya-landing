import type { AgentOperationalFlow } from "@/data/landing/niches/types";

export type TaliyaLandingAgentFlow = AgentOperationalFlow & {
  displayTitle: string;
  summary: string;
  channels: Array<"App" | "WhatsApp">;
  when: string;
  does: string;
  outcome: string;
  whenBullets: string[];
  doesBullets: string[];
  outcomeBullets: string[];
  inside: Array<{
    title: string;
    text: string;
  }>;
};

type FlowSeed = {
  code: string;
  title: string;
  channel: AgentOperationalFlow["channel"];
  mode: AgentOperationalFlow["mode"];
  trigger: string;
  checks: string[];
  states: string[];
};

type FeaturedFlowNarrative = Pick<TaliyaLandingAgentFlow, "doesBullets" | "inside" | "outcomeBullets" | "whenBullets">;

function sentence(value: string) {
  return value.endsWith(".") ? value : `${value}.`;
}

function outputFor(flow: FlowSeed) {
  return `A Taliya responde ao pedido de ${flow.title.toLowerCase()} e organiza as informações no app.`;
}

function resultFor(_states: string[]) {
  return "O registro fica disponível para você consultar e continuar quando precisar.";
}

function handoffFor(_states: string[]) {
  return "Se faltar informação ou a decisão depender de você, a Taliya pergunta antes de seguir.";
}

function actionFor(flow: FlowSeed) {
  return `A Taliya organiza ${flow.title.toLowerCase()} com as informações que você confirmar.`;
}

function flow(seed: FlowSeed): AgentOperationalFlow {
  return {
    id: seed.code.toLowerCase(),
    code: seed.code,
    title: seed.title,
    channel: seed.channel,
    mode: seed.mode,
    trigger: sentence(seed.trigger),
    checks: seed.checks,
    action: actionFor(seed),
    message: outputFor(seed),
    result: resultFor(seed.states),
    handoff: handoffFor(seed.states),
  };
}

const atendimento = [
  flow({ code: "A1", title: "Nova conversa", channel: "whatsapp", mode: "automatico", trigger: "mensagem de contato desconhecido ou interessado", checks: ["Identifica o contato", "Classifica a intencao", "Aplica guardrail"], states: ["proximo_fluxo", "aguardando_contato", "handoff_humano", "pausado"] }),
  flow({ code: "A2", title: "Duvidas permitidas", channel: "whatsapp", mode: "automatico", trigger: "pergunta objetiva sobre dados publicos ou regras aprovadas", checks: ["Dados publicos", "Dados operacionais", "Dados comerciais", "Resposta existente"], states: ["resolvido", "proximo_fluxo", "tarefa_criada", "aguardando_contato"] }),
  flow({ code: "A3", title: "Aluno existente", channel: "whatsapp", mode: "automatico", trigger: "aluno manda mensagem operacional", checks: ["Agenda", "Financeiro", "Retencao", "Historico"], states: ["proximo_fluxo", "aguardando_contato", "handoff_humano"] }),
  flow({ code: "A4", title: "Fora do escopo", channel: "whatsapp", mode: "customizado", trigger: "mensagem que nao pertence aos fluxos principais", checks: ["Fornecedor ou parceria", "Vaga de emprego", "Spam", "Prompt injection"], states: ["pausado", "tarefa_criada", "handoff_humano"] }),
  flow({ code: "A5", title: "Handoff humano", channel: "hibrido", mode: "humano", trigger: "excecao, seguranca, risco ou pedido humano", checks: ["Resumo do caso", "Encaminhamento", "Pausa da automacao"], states: ["handoff_humano", "aguardando_equipe", "tarefa_criada"] }),
  flow({ code: "A6", title: "Consentimento, opt-out e janela", channel: "hibrido", mode: "automatico", trigger: "contato pede para parar mensagens, conversa fora de horario ou politica de consentimento exige controle", checks: ["Opt-out", "Janela de atendimento", "Consentimento"], states: ["pausado", "acao_registrada", "proximo_fluxo", "tarefa_criada"] }),
  flow({ code: "A7", title: "Identidade, duplicidade e midias", channel: "hibrido", mode: "customizado", trigger: "contato nao identificado, telefone duplicado, audio, imagem, comprovante ou documento", checks: ["Identidade", "Midias", "Duplicidade"], states: ["acao_registrada", "tarefa_criada", "proximo_fluxo", "handoff_humano"] }),
  flow({ code: "A8", title: "Privacidade, dados e preferencias", channel: "hibrido", mode: "copiloto", trigger: "contato pede dados, exclusao, correcao cadastral, historico de mensagens ou mudanca de preferencia", checks: ["Pedido de dados", "Correcao cadastral", "Preferencias", "Guardrail"], states: ["tarefa_criada", "acao_registrada", "pausado", "handoff_humano"] }),
  flow({ code: "A9", title: "Grupos, familiares e responsaveis", channel: "whatsapp", mode: "customizado", trigger: "mensagem vem de grupo, familiar, responsavel financeiro ou telefone compartilhado", checks: ["Origem", "Caminhos", "Dados sensiveis"], states: ["proximo_fluxo", "aguardando_contato", "handoff_humano", "pausado"] }),
  flow({ code: "A10", title: "Ciclo de vida da conversa e SLA", channel: "hibrido", mode: "automatico", trigger: "conversa fica aberta, contato responde depois de muito tempo, Taliya aguarda retorno ou prazo interno vence", checks: ["Abertura", "Continuidade", "Encerramento", "SLA interno"], states: ["resolvido", "proximo_fluxo", "tarefa_criada", "aguardando_equipe", "pausado"] }),
];

const agenda = [
  flow({ code: "B1", title: "Confirmacao de presenca", channel: "whatsapp", mode: "automatico", trigger: "janela configurada antes da aula", checks: ["Envia confirmacao", "Interpreta resposta"], states: ["acao_registrada", "aguardando_contato", "proximo_fluxo"] }),
  flow({ code: "B2", title: "Falta com aviso", channel: "hibrido", mode: "customizado", trigger: "aluno avisa que nao vai", checks: ["Identifica a aula", "Aplica regra", "Libera vaga"], states: ["acao_registrada", "proximo_fluxo", "handoff_humano"] }),
  flow({ code: "B3", title: "No-show", channel: "hibrido", mode: "customizado", trigger: "aula terminou sem presenca registrada", checks: ["Origem do dado", "Acoes possiveis"], states: ["acao_registrada", "tarefa_criada", "proximo_fluxo"] }),
  flow({ code: "B4", title: "Recuperar vaga aberta", channel: "hibrido", mode: "customizado", trigger: "vaga aberta por falta, cancelamento ou lista de espera", checks: ["Candidato", "Politica de convite", "Resposta", "Economia"], states: ["resolvido", "acao_registrada", "aguardando_contato", "sem_acao"] }),
  flow({ code: "B5", title: "Reposicao ou remarcacao", channel: "whatsapp", mode: "customizado", trigger: "aluno pede reposicao, remarcacao ou encaixe", checks: ["Direito a reposicao", "Horario disponivel", "Conclusao"], states: ["resolvido", "tarefa_criada", "handoff_humano", "aguardando_contato"] }),
  flow({ code: "B6", title: "Lista de espera", channel: "hibrido", mode: "customizado", trigger: "aluno quer horario cheio ou vaga abre", checks: ["Entrada na lista", "Prioridade", "Convite"], states: ["resolvido", "aguardando_contato", "sem_acao", "proximo_fluxo"] }),
  flow({ code: "B7", title: "Disponibilidade para experimental", channel: "hibrido", mode: "automatico", trigger: "Vendas ou Atendimento precisam de horario para interessado", checks: ["Coleta minima", "Busca de vaga", "Saidas"], states: ["proximo_fluxo", "tarefa_criada", "aguardando_contato", "handoff_humano"] }),
  flow({ code: "B8", title: "Mudanca de horario fixo", channel: "hibrido", mode: "customizado", trigger: "aluno pede troca de horario recorrente", checks: ["Motivo", "Caminhos"], states: ["resolvido", "tarefa_criada", "proximo_fluxo", "handoff_humano"] }),
  flow({ code: "B9", title: "Alteracao pelo studio", channel: "hibrido", mode: "copiloto", trigger: "aula cancelada, professor ausente, feriado, manutencao, sala indisponivel ou mudanca de grade", checks: ["Motivo", "Impacto", "Comunicacao"], states: ["tarefa_criada", "proximo_fluxo", "acao_registrada", "aguardando_contato"] }),
  flow({ code: "B10", title: "Conflito de capacidade", channel: "sistema", mode: "copiloto", trigger: "overbooking, professor duplicado, sala cheia, equipamento indisponivel ou turma incompatvel", checks: ["Conflito", "Resolucao"], states: ["tarefa_criada", "handoff_humano", "sem_acao"] }),
  flow({ code: "B11", title: "Criacao ou ajuste de grade", channel: "sistema", mode: "copiloto", trigger: "equipe altera turma, cria horario, muda professor, capacidade ou recorrencia", checks: ["Mudanca", "Impacto", "Saidas"], states: ["tarefa_criada", "acao_registrada", "proximo_fluxo"] }),
  flow({ code: "B12", title: "Experimental no-show ou reagendamento", channel: "hibrido", mode: "customizado", trigger: "interessado nao comparece, cancela ou pede remarcacao da experimental", checks: ["No-show", "Cancelamento com aviso", "Remarcacao"], states: ["proximo_fluxo", "aguardando_contato", "tarefa_criada", "resolvido"] }),
  flow({ code: "B13", title: "Creditos de reposicao", channel: "hibrido", mode: "customizado", trigger: "credito de reposicao criado, perto de vencer, usado, vencido ou acumulado", checks: ["Criacao", "Uso", "Vencimento", "Acumulo"], states: ["acao_registrada", "proximo_fluxo", "tarefa_criada", "sem_acao"] }),
  flow({ code: "B14", title: "Presenca manual e auditoria", channel: "sistema", mode: "copiloto", trigger: "professor corrige chamada, aluno contesta falta, presenca duplicada ou aula encerrada com dado inconsistente", checks: ["Correcao", "Impacto", "Caminhos"], states: ["acao_registrada", "tarefa_criada", "proximo_fluxo"] }),
  flow({ code: "B15", title: "Primeira aula como aluno", channel: "hibrido", mode: "customizado", trigger: "pre-matricula vira aluno, pagamento/contrato confirmado ou equipe libera inicio", checks: ["Preparacao", "Dados faltantes", "Depois da primeira aula"], states: ["acao_registrada", "proximo_fluxo", "tarefa_criada", "aguardando_contato"] }),
  flow({ code: "B16", title: "Aula avulsa, evento ou workshop", channel: "hibrido", mode: "customizado", trigger: "studio cria aula nao recorrente, evento, workshop, turma extra ou vaga especial", checks: ["Tipo", "Publico", "Caminhos"], states: ["proximo_fluxo", "tarefa_criada", "acao_registrada", "aguardando_contato"] }),
];

const vendas = [
  flow({ code: "C1", title: "Valores e planos", channel: "whatsapp", mode: "customizado", trigger: "pergunta sobre preco, plano, pacote ou frequencia", checks: ["Politica comercial", "Qualificacao leve", "Caminhos"], states: ["aguardando_contato", "proximo_fluxo", "handoff_humano"] }),
  flow({ code: "C2", title: "Aula experimental", channel: "hibrido", mode: "automatico", trigger: "interessado quer conhecer o studio", checks: ["Prepara reserva", "Caminhos"], states: ["acao_registrada", "proximo_fluxo", "aguardando_contato", "handoff_humano"] }),
  flow({ code: "C3", title: "Lembrete de experimental", channel: "whatsapp", mode: "automatico", trigger: "janela antes da aula experimental", checks: ["Respostas"], states: ["acao_registrada", "aguardando_contato", "proximo_fluxo"] }),
  flow({ code: "C4", title: "Pos-aula experimental", channel: "whatsapp", mode: "customizado", trigger: "aula experimental concluida", checks: ["Contexto", "Caminhos"], states: ["aguardando_contato", "proximo_fluxo", "handoff_humano"] }),
  flow({ code: "C5", title: "Follow-up comercial", channel: "hibrido", mode: "customizado", trigger: "interessado parado", checks: ["Motivos", "Cadencia", "Respostas"], states: ["aguardando_contato", "tarefa_criada", "pausado", "resolvido"] }),
  flow({ code: "C6", title: "Pre-matricula", channel: "hibrido", mode: "copiloto", trigger: "interessado quer entrar", checks: ["Dados", "Caminhos"], states: ["tarefa_criada", "proximo_fluxo", "acao_registrada", "handoff_humano"] }),
  flow({ code: "C7", title: "Objecoes", channel: "whatsapp", mode: "customizado", trigger: "resistencia comercial", checks: ["Tipos de objecao", "Caminhos"], states: ["aguardando_contato", "proximo_fluxo", "handoff_humano", "resolvido"] }),
  flow({ code: "C8", title: "Origem e qualificacao", channel: "hibrido", mode: "automatico", trigger: "novo interessado entra no funil", checks: ["Origem", "Qualificacao", "Saida"], states: ["acao_registrada", "proximo_fluxo", "aguardando_contato"] }),
  flow({ code: "C9", title: "Perda comercial", channel: "hibrido", mode: "customizado", trigger: "interessado diz que nao quer, escolheu outro studio, achou caro ou parou definitivamente", checks: ["Motivos", "Caminhos"], states: ["resolvido", "acao_registrada", "pausado", "tarefa_criada"] }),
  flow({ code: "C10", title: "Indicacao por aluno", channel: "hibrido", mode: "customizado", trigger: "aluno indica alguem ou interessado menciona indicacao", checks: ["Indicado", "Aluno indicador"], states: ["acao_registrada", "proximo_fluxo", "handoff_humano"] }),
  flow({ code: "C11", title: "Checkout e abandono", channel: "hibrido", mode: "customizado", trigger: "interessado recebe link de contratacao, abre checkout, abandona ou conclui", checks: ["Link", "Abandono", "Conclusao", "Guardrail"], states: ["proximo_fluxo", "aguardando_contato", "tarefa_criada", "resolvido"] }),
  flow({ code: "C12", title: "Demanda sem vaga", channel: "hibrido", mode: "customizado", trigger: "interessado quer horario/plano que nao tem disponibilidade", checks: ["Sem vaga", "Caminhos", "Conversao"], states: ["aguardando_contato", "tarefa_criada", "proximo_fluxo", "resolvido"] }),
  flow({ code: "C13", title: "Transicao para aluno", channel: "hibrido", mode: "copiloto", trigger: "pagamento, contrato ou decisao da equipe confirma nova matricula", checks: ["Conversao", "Pendencias", "Comunicacao"], states: ["acao_registrada", "proximo_fluxo", "tarefa_criada", "resolvido"] }),
  flow({ code: "C14", title: "Upsell e mudanca de plano", channel: "hibrido", mode: "copiloto", trigger: "aluno demonstra interesse em aumentar frequencia, trocar plano, incluir servico ou comprar aula extra", checks: ["Interesse", "Caminhos", "Guardrail"], states: ["proximo_fluxo", "tarefa_criada", "aguardando_contato", "handoff_humano"] }),
];

const financeiro = [
  flow({ code: "D1", title: "Lembrete de vencimento", channel: "whatsapp", mode: "customizado", trigger: "vencimento proximo", checks: ["Momento", "Economia", "Respostas"], states: ["aguardando_contato", "proximo_fluxo", "tarefa_criada"] }),
  flow({ code: "D2", title: "Pagamento atrasado", channel: "hibrido", mode: "customizado", trigger: "parcela vencida", checks: ["Faixas", "Caminhos"], states: ["aguardando_contato", "tarefa_criada", "handoff_humano", "proximo_fluxo"] }),
  flow({ code: "D3", title: "Pix, link ou segunda via", channel: "whatsapp", mode: "automatico", trigger: "aluno pede pagamento ou fluxo financeiro solicita", checks: ["Fonte", "Guardrail", "Caminhos"], states: ["resolvido", "tarefa_criada", "pausado", "aguardando_contato"] }),
  flow({ code: "D4", title: "Confirmacao de pagamento", channel: "hibrido", mode: "customizado", trigger: "webhook, comprovante ou baixa manual", checks: ["Fonte", "Caminhos"], states: ["acao_registrada", "tarefa_criada", "proximo_fluxo", "handoff_humano"] }),
  flow({ code: "D5", title: "Renovacao de plano", channel: "hibrido", mode: "copiloto", trigger: "plano vencendo, pagamento confirmado ou aluno quer renovar", checks: ["Mesmo plano", "Mudanca"], states: ["acao_registrada", "tarefa_criada", "proximo_fluxo", "handoff_humano"] }),
  flow({ code: "D6", title: "Excecoes financeiras", channel: "hibrido", mode: "humano", trigger: "desconto, reembolso, pausa, cancelamento, contestacao, mudanca de vencimento", checks: ["Politica simples", "Decisao"], states: ["handoff_humano", "tarefa_criada", "proximo_fluxo"] }),
  flow({ code: "D7", title: "Falha de pagamento", channel: "hibrido", mode: "customizado", trigger: "cartao recusado, Pix expirado, link vencido, recorrencia falhou ou webhook de falha", checks: ["Tipo de falha", "Caminhos"], states: ["proximo_fluxo", "tarefa_criada", "aguardando_contato", "handoff_humano"] }),
  flow({ code: "D8", title: "Recibo, nota ou comprovante", channel: "hibrido", mode: "customizado", trigger: "aluno pede recibo, nota, comprovante ou declaracao", checks: ["Documento", "Caminhos"], states: ["resolvido", "tarefa_criada", "handoff_humano"] }),
  flow({ code: "D9", title: "Pausa ou trancamento", channel: "hibrido", mode: "humano", trigger: "aluno quer pausar por viagem, saude, agenda ou motivo financeiro", checks: ["Motivo", "Impacto", "Caminhos"], states: ["handoff_humano", "tarefa_criada", "proximo_fluxo"] }),
  flow({ code: "D10", title: "Conciliacao interna", channel: "sistema", mode: "copiloto", trigger: "pagamento sem aluno, aluno sem pagamento, valor divergente ou baixa manual pendente", checks: ["Divergencia", "Caminhos"], states: ["tarefa_criada", "sem_acao", "handoff_humano"] }),
  flow({ code: "D11", title: "Contrato e assinatura", channel: "hibrido", mode: "copiloto", trigger: "nova matricula, renovacao com termo, cancelamento, pausa ou pedido de contrato", checks: ["Documento", "Caminhos", "Guardrail"], states: ["acao_registrada", "tarefa_criada", "handoff_humano", "aguardando_contato"] }),
  flow({ code: "D12", title: "Bloqueio ou liberacao", channel: "hibrido", mode: "humano", trigger: "inadimplencia acima do limite, cancelamento confirmado, fim de plano ou liberacao manual", checks: ["Bloqueio", "Liberacao", "Caminhos"], states: ["tarefa_criada", "acao_registrada", "handoff_humano", "proximo_fluxo"] }),
  flow({ code: "D13", title: "Creditos, bonus e cortesias", channel: "hibrido", mode: "humano", trigger: "equipe concede cortesia, credito manual, bonus de indicacao, ajuste comercial ou compensacao", checks: ["Tipos", "Caminhos", "Guardrail"], states: ["acao_registrada", "tarefa_criada", "handoff_humano", "proximo_fluxo"] }),
  flow({ code: "D14", title: "Fechamento mensal", channel: "sistema", mode: "automatico", trigger: "fim de mes, dono abre financeiro ou rotina de resumo", checks: ["Indicadores", "Caminhos"], states: ["acao_registrada", "tarefa_criada", "proximo_fluxo", "sem_acao"] }),
];

const retencao = [
  flow({ code: "E1", title: "Queda de frequencia", channel: "hibrido", mode: "customizado", trigger: "frequencia abaixo do padrao", checks: ["Sinais", "Caminhos"], states: ["tarefa_criada", "aguardando_contato", "proximo_fluxo", "handoff_humano"] }),
  flow({ code: "E2", title: "Aluno inativo", channel: "hibrido", mode: "customizado", trigger: "aluno ativo sem presenca por janela configurada", checks: ["Faixas", "Economia", "Respostas"], states: ["aguardando_contato", "proximo_fluxo", "tarefa_criada", "handoff_humano"] }),
  flow({ code: "E3", title: "Retorno", channel: "hibrido", mode: "customizado", trigger: "aluno inativo aceita voltar", checks: ["Preferencia", "Conclusao"], states: ["acao_registrada", "proximo_fluxo", "tarefa_criada", "handoff_humano"] }),
  flow({ code: "E4", title: "Risco de cancelamento", channel: "hibrido", mode: "humano", trigger: "cancelamento, pausa, insatisfacao ou risco alto", checks: ["Sinais", "Caminhos"], states: ["handoff_humano", "tarefa_criada", "proximo_fluxo"] }),
  flow({ code: "E5", title: "Reativacao de ex-aluno", channel: "hibrido", mode: "copiloto", trigger: "ex-aluno elegivel para reativacao", checks: ["Segmentos", "Execucao", "Resposta"], states: ["tarefa_criada", "proximo_fluxo", "pausado", "aguardando_contato"] }),
  flow({ code: "E6", title: "Satisfacao e experiencia", channel: "hibrido", mode: "customizado", trigger: "aula experimental, retorno, reclamacao, queda de frequencia ou janela de pesquisa", checks: ["Coleta", "Caminhos"], states: ["acao_registrada", "tarefa_criada", "handoff_humano", "proximo_fluxo"] }),
  flow({ code: "E7", title: "Retorno apos pausa", channel: "hibrido", mode: "customizado", trigger: "pausa/trancamento tem data prevista de retorno", checks: ["Antes da data", "Caminhos"], states: ["proximo_fluxo", "aguardando_contato", "tarefa_criada"] }),
  flow({ code: "E8", title: "Risco por perfil de uso", channel: "sistema", mode: "automatico", trigger: "combinacao de sinais indica risco sem mensagem explicita", checks: ["Sinais combinados", "Caminhos"], states: ["tarefa_criada", "proximo_fluxo", "sem_acao"] }),
  flow({ code: "E9", title: "Pos-cancelamento", channel: "hibrido", mode: "copiloto", trigger: "cancelamento aprovado/concluido pela equipe", checks: ["Encerramento", "Comunicacao", "Pos-cancelamento"], states: ["acao_registrada", "proximo_fluxo", "pausado", "tarefa_criada"] }),
  flow({ code: "E10", title: "Marco de engajamento", channel: "hibrido", mode: "customizado", trigger: "aluno completa marco relevante de presenca, retorno, consistencia ou objetivo", checks: ["Marcos", "Caminhos"], states: ["acao_registrada", "tarefa_criada", "resolvido", "sem_acao"] }),
  flow({ code: "E11", title: "Saude, dor ou evento pessoal", channel: "hibrido", mode: "humano", trigger: "aluno menciona dor, lesao, cirurgia, gravidez, luto, mudanca pessoal ou situacao delicada que afeta frequencia", checks: ["Tipo", "Caminhos", "Guardrail"], states: ["handoff_humano", "tarefa_criada", "proximo_fluxo", "pausado"] }),
  flow({ code: "E12", title: "Campanhas de retencao", channel: "sistema", mode: "copiloto", trigger: "dono quer ver grupos de risco, campanha de retencao ou lista priorizada", checks: ["Segmentos", "Caminhos"], states: ["tarefa_criada", "proximo_fluxo", "sem_acao"] }),
];

const gestao = [
  flow({ code: "F1", title: "Visão do dia", channel: "hibrido", mode: "copiloto", trigger: "você pede os horários e lembretes de hoje", checks: ["Agenda do dia", "Lembretes criados para hoje"], states: ["resumo consultado"] }),
  flow({ code: "F2", title: "Resumo de recebimentos", channel: "hibrido", mode: "copiloto", trigger: "você pede os recebimentos de um período", checks: ["Pagamentos registrados", "Valores combinados", "Período informado"], states: ["resumo consultado"] }),
  flow({ code: "F5", title: "Resumo do período", channel: "hibrido", mode: "copiloto", trigger: "você pede um resumo da atividade em um período", checks: ["Serviços registrados", "Horários", "Orçamentos", "Recebimentos"], states: ["resumo consultado"] }),
  flow({ code: "F8", title: "Fechamento do expediente", channel: "hibrido", mode: "copiloto", trigger: "você pede o fechamento do dia", checks: ["Serviços concluídos registrados", "Recebimentos informados", "Agenda de amanhã", "Lembretes criados"], states: ["resumo consultado"] }),
];

const listagens = [
  flow({ code: "F3", title: "Clientes com horário marcado", channel: "hibrido", mode: "copiloto", trigger: "você pergunta quem tem serviço marcado em um período", checks: ["Agenda registrada", "Período informado", "Serviço associado"], states: ["lista consultada"] }),
  flow({ code: "F4", title: "Serviços prestados", channel: "hibrido", mode: "copiloto", trigger: "você pergunta quais serviços foram prestados em um período", checks: ["Serviços registrados", "Status informado", "Período solicitado"], states: ["lista consultada"] }),
  flow({ code: "F6", title: "Orçamentos aguardando resposta", channel: "hibrido", mode: "copiloto", trigger: "você pergunta quais orçamentos aguardam resposta", checks: ["Orçamentos registrados", "Status atual", "Data ou cliente, se informados"], states: ["lista consultada"] }),
  flow({ code: "F7", title: "Saldos em aberto", channel: "hibrido", mode: "copiloto", trigger: "você pergunta quais serviços ainda têm saldo a receber", checks: ["Valor combinado registrado", "Recebimentos registrados", "Cliente ou período solicitado"], states: ["lista consultada"] }),
];

const historicoEvolucao = [
  flow({ code: "G1", title: "Contexto antes da aula", channel: "sistema", mode: "automatico", trigger: "professor abre turma ou preparacao antes da aula", checks: ["Dados", "Caminhos"], states: ["acao_registrada", "tarefa_criada", "pausado"] }),
  flow({ code: "G2", title: "Observacao pos-aula", channel: "sistema", mode: "automatico", trigger: "aula encerrada ou professor adiciona nota", checks: ["Entrada", "Caminhos"], states: ["acao_registrada", "proximo_fluxo", "tarefa_criada"] }),
  flow({ code: "G3", title: "Restricao ou cuidado", channel: "sistema", mode: "copiloto", trigger: "restricao, dor, lesao, gravidez, limitacao ou cuidado", checks: ["Acoes internas", "Guardrail"], states: ["acao_registrada", "handoff_humano", "pausado"] }),
  flow({ code: "G4", title: "Objetivo e evolucao", channel: "sistema", mode: "automatico", trigger: "intervalo de revisao ou nota de professor", checks: ["Caminhos"], states: ["acao_registrada", "tarefa_criada", "proximo_fluxo"] }),
  flow({ code: "G5", title: "Contexto para outra rotina", channel: "sistema", mode: "automatico", trigger: "outra rotina precisa de contexto seguro", checks: ["Solicitantes", "Caminhos"], states: ["proximo_fluxo", "tarefa_criada", "handoff_humano", "sem_acao"] }),
  flow({ code: "G6", title: "Documentos e anamnese", channel: "hibrido", mode: "copiloto", trigger: "aluno envia documento, equipe anexa arquivo, professor pede ficha ou avaliacao", checks: ["Tipo", "Caminhos"], states: ["acao_registrada", "tarefa_criada", "handoff_humano"] }),
  flow({ code: "G7", title: "Correcao de historico", channel: "sistema", mode: "copiloto", trigger: "dado errado, nota duplicada, restricao desatualizada ou equipe corrige informacao", checks: ["Tipo", "Caminhos"], states: ["acao_registrada", "tarefa_criada", "handoff_humano"] }),
  flow({ code: "G8", title: "Handoff entre professores", channel: "sistema", mode: "automatico", trigger: "troca de professor, substituicao, aluno muda turma ou existe cuidado importante", checks: ["Contexto de handoff", "Caminhos"], states: ["acao_registrada", "tarefa_criada", "sem_acao"] }),
  flow({ code: "G9", title: "Lembrete para professor", channel: "sistema", mode: "automatico", trigger: "aula terminou sem nota, aluno tem cuidado importante ou professor esqueceu acompanhamento", checks: ["Lembrete", "Caminhos"], states: ["tarefa_criada", "acao_registrada", "sem_acao"] }),
  flow({ code: "G10", title: "Compartilhamento seguro", channel: "hibrido", mode: "copiloto", trigger: "aluno pede resumo, evolucao, historico, ficha ou observacao", checks: ["Pedido", "Caminhos"], states: ["tarefa_criada", "handoff_humano", "resolvido", "aguardando_contato"] }),
  flow({ code: "G11", title: "Permissao de visibilidade", channel: "sistema", mode: "automatico", trigger: "professor, recepcao, financeiro ou gestor acessa historico do aluno", checks: ["Papeis", "Dados", "Caminhos"], states: ["acao_registrada", "pausado", "sem_acao"] }),
  flow({ code: "G12", title: "Linha do tempo do aluno", channel: "sistema", mode: "automatico", trigger: "equipe abre perfil, rotina precisa de contexto ou Gestao consolida risco", checks: ["Eventos", "Caminhos"], states: ["acao_registrada", "proximo_fluxo", "sem_acao", "tarefa_criada"] }),
];

export const taliyaAgentFlowsByAgent: Record<string, AgentOperationalFlow[]> = {
  atendimento,
  agenda,
  vendas,
  financeiro,
  retencao,
  gestao,
  listagens,
  "historico-evolucao": historicoEvolucao,
};

export const taliyaAgentFlowTotal = Object.values(taliyaAgentFlowsByAgent).reduce((total, flows) => total + flows.length, 0);

const featuredFlowCodesByAgent: Record<string, string[]> = {
  atendimento: ["A1", "A2", "A3", "A5", "A10"],
  agenda: ["B1", "B2", "B3", "B4", "B5", "B12"],
  vendas: ["C1", "C2", "C4", "C5", "C6", "C7"],
  financeiro: ["D1", "D2", "D3", "D5", "D6", "D14"],
  retencao: ["E1", "E2", "E4", "E5", "E6", "E7"],
  gestao: ["F1", "F2", "F5", "F8"],
  listagens: ["F3", "F4", "F6", "F7"],
  "historico-evolucao": ["G1", "G2", "G3", "G4", "G5", "G12"],
};

const featuredFlowEditorial: Record<string, Pick<TaliyaLandingAgentFlow, "displayTitle" | "when" | "does" | "outcome">> = {
  A1: {
    displayTitle: "Novo cliente",
    when: "Quando alguém chama pela primeira vez ou você pede para cadastrar um cliente.",
    does: "Registra os dados informados e relaciona o contato ao pedido ou serviço correspondente.",
    outcome: "O cadastro fica disponível para consultar e continuar a conversa com contexto.",
  },
  A2: {
    displayTitle: "Dados do cliente",
    when: "Quando você pede um dado já registrado de um cliente.",
    does: "Consulta o cadastro e devolve as informações disponíveis, sem preencher o que não foi informado.",
    outcome: "Você encontra o contato e os detalhes registrados em uma única consulta.",
  },
  A3: {
    displayTitle: "Histórico do cliente",
    when: "Quando você quer retomar o que já foi combinado com um cliente.",
    does: "Reúne os serviços, horários, orçamentos, recebimentos e documentos relacionados que estão registrados.",
    outcome: "A conversa continua a partir do histórico disponível do cliente.",
  },
  A5: {
    displayTitle: "Pedido para a equipe",
    when: "Quando você pede ajuda de uma pessoa ou precisa decidir algo fora do combinado.",
    does: "Organiza o pedido e o contexto já registrado para você continuar o atendimento.",
    outcome: "O histórico fica junto do pedido para a conversa não recomeçar do zero.",
  },
  A10: {
    displayTitle: "Lembrete de retorno",
    when: "Quando você combina de voltar a falar com um cliente em outra data.",
    does: "Cria um lembrete com a data e o assunto que você informar.",
    outcome: "O lembrete ajuda você a retomar a conversa no momento combinado.",
  },
  B1: {
    displayTitle: "Agendar serviço",
    when: "Quando você pede para marcar um serviço para um cliente.",
    does: "Registra o cliente, o serviço e a data e o horário informados na agenda.",
    outcome: "O horário fica ligado ao cliente e ao serviço marcado.",
  },
  B2: {
    displayTitle: "Cancelar horário",
    when: "Quando você pede para cancelar um horário já marcado.",
    does: "Atualiza o status desse horário e mantém o serviço e o histórico registrados.",
    outcome: "A agenda mostra o cancelamento sem apagar o que já foi combinado.",
  },
  B3: {
    displayTitle: "Atualizar agenda",
    when: "Quando você informa uma mudança em um horário ou serviço.",
    does: "Atualiza a data, o horário ou o status conforme o que você pediu.",
    outcome: "A agenda e o histórico refletem a alteração informada.",
  },
  B4: {
    displayTitle: "Encontrar horário",
    when: "Quando você pergunta quais horários estão disponíveis para um serviço.",
    does: "Consulta os horários registrados na agenda e apresenta as opções encontradas.",
    outcome: "Você vê as opções disponíveis antes de marcar ou combinar uma mudança.",
  },
  B5: {
    displayTitle: "Remarcar serviço",
    when: "Quando você pede para mudar o dia ou horário de um serviço.",
    does: "Atualiza o agendamento e preserva o vínculo com o cliente e o serviço.",
    outcome: "O novo horário fica na agenda e a mudança continua no histórico.",
  },
  B12: {
    displayTitle: "Lembrete de agenda",
    when: "Quando você quer lembrar de confirmar ou combinar o próximo horário de um serviço.",
    does: "Cria um lembrete com o cliente, o assunto e a data que você informar.",
    outcome: "O lembrete aparece junto do contexto do serviço para você consultar depois.",
  },
  C1: {
    displayTitle: "Avulso, pacote ou plano",
    when: "Quando você cadastra o que oferece ou precisa explicar os formatos de serviço.",
    does: "Organiza serviços avulsos, pacotes com quantidade definida de atendimentos e planos recorrentes conforme os detalhes informados.",
    outcome: "Cada serviço fica registrado com seu tipo, valor e condições combinadas.",
  },
  C2: {
    displayTitle: "Criar orçamento",
    when: "Quando você pede um orçamento para um cliente.",
    does: "Reúne os serviços, quantidades, valores e condições que você informar e prepara o total para revisão.",
    outcome: "O orçamento fica organizado para você conferir antes de compartilhar.",
  },
  C4: {
    displayTitle: "Aprovar orçamento",
    when: "Quando você informa que o cliente aprovou ou pediu uma alteração na proposta.",
    does: "Atualiza o status ou os detalhes que você indicar e mantém as versões anteriores consultáveis.",
    outcome: "Você acompanha a versão atual sem perder o histórico do orçamento.",
  },
  C5: {
    displayTitle: "Retomar orçamento",
    when: "Quando você quer consultar orçamentos enviados que ainda aguardam resposta.",
    does: "Lista as propostas pelo cliente e pela data de envio; se quiser, cria um lembrete de retorno.",
    outcome: "Você encontra os orçamentos para decidir com quem e quando retomar o assunto.",
  },
  C6: {
    displayTitle: "Registrar serviço",
    when: "Quando você informa que o cliente aprovou o orçamento ou combinou o serviço.",
    does: "Relaciona o serviço aprovado ao cliente e registra os detalhes informados.",
    outcome: "O combinado segue ligado ao orçamento, ao cliente e aos próximos horários.",
  },
  C7: {
    displayTitle: "Ajustar proposta",
    when: "Quando você precisa consultar ou alterar o escopo, o valor ou as condições combinadas.",
    does: "Reúne os detalhes registrados para o serviço avulso, pacote ou plano.",
    outcome: "O combinado fica claro para você consultar e atualizar quando necessário.",
  },
  D1: {
    displayTitle: "Registrar recebimento",
    when: "Quando você informa que recebeu um valor de um cliente.",
    does: "Registra o recebimento no serviço correspondente e atualiza o saldo com base no valor combinado.",
    outcome: "Você consulta o que foi recebido e o que ainda falta receber.",
  },
  D2: {
    displayTitle: "Consultar saldo",
    when: "Quando você pergunta quanto foi recebido e qual saldo consta para o cliente.",
    does: "Consulta o valor combinado e os recebimentos registrados para calcular o saldo atual.",
    outcome: "A resposta mostra os valores usados no cálculo e o que ainda está em aberto.",
  },
  D3: {
    displayTitle: "Lembrete de cobrança",
    when: "Quando você combina de cobrar um saldo em uma data específica.",
    does: "Cria um lembrete vinculado ao cliente e ao serviço e prepara uma mensagem para sua revisão.",
    outcome: "O valor, o cliente e a data da cobrança ficam reunidos no lembrete.",
  },
  D5: {
    displayTitle: "Acompanhar recebimentos",
    when: "Quando você quer listar pagamentos por cliente, serviço ou período.",
    does: "Organiza os recebimentos registrados e mostra os respectivos status.",
    outcome: "Você acompanha os valores lançados sem misturar pagamentos ainda não informados.",
  },
  D6: {
    displayTitle: "Corrigir um registro",
    when: "Quando você informa que um valor ou status foi registrado incorretamente.",
    does: "Localiza o lançamento, aplica a correção solicitada e atualiza o saldo relacionado.",
    outcome: "O recebimento e o saldo passam a refletir a informação corrigida.",
  },
  D14: {
    displayTitle: "Histórico de recebimentos",
    when: "Quando você pede para consultar os recebimentos de um cliente ou período.",
    does: "Reúne os pagamentos registrados com as datas e os serviços relacionados.",
    outcome: "Você consulta os lançamentos existentes e vê o saldo apenas quando ele pode ser calculado.",
  },
  E1: {
    displayTitle: "Criar lembrete",
    when: "Quando você quer guardar uma tarefa para uma data ou horário.",
    does: "Registra o texto e a data informados e relaciona o lembrete ao cliente ou serviço escolhido.",
    outcome: "O lembrete fica disponível para consultar no momento combinado.",
  },
  E2: {
    displayTitle: "Listar lembretes",
    when: "Quando você pergunta quais lembretes já criou.",
    does: "Consulta os lembretes registrados por data, cliente, serviço ou situação.",
    outcome: "A lista mostra os lembretes existentes para o filtro solicitado.",
  },
  E4: {
    displayTitle: "Alterar lembrete",
    when: "Quando você informa uma nova data ou muda o texto de um lembrete.",
    does: "Atualiza o lembrete existente e mantém o vínculo com seu contexto.",
    outcome: "A próxima consulta mostra os detalhes atualizados.",
  },
  E5: {
    displayTitle: "Concluir lembrete",
    when: "Quando você informa que resolveu algo que tinha anotado.",
    does: "Marca como concluído o lembrete escolhido.",
    outcome: "O status do lembrete reflete a conclusão que você informou.",
  },
  E6: {
    displayTitle: "Lembrete para cliente",
    when: "Quando você combina de falar com um cliente sobre um serviço, orçamento ou documento.",
    does: "Cria um lembrete com o assunto e a data que você escolher.",
    outcome: "O contato fica relacionado ao cliente e ao próximo passo combinado.",
  },
  E7: {
    displayTitle: "Próximo lembrete",
    when: "Quando você precisa consultar o que combinou de fazer em seguida.",
    does: "Mostra os lembretes existentes e as respectivas datas.",
    outcome: "Você retoma os próximos passos que registrou.",
  },
  F1: {
    displayTitle: "Visão do dia",
    when: "Quando você pergunta como está o dia de hoje.",
    does: "A Taliya reúne os horários da agenda e os lembretes que você criou para hoje.",
    outcome: "Você vê o que está marcado e o que combinou de lembrar.",
  },
  F2: {
    displayTitle: "Resumo de recebimentos",
    when: "Quando você quer consultar os valores recebidos em um período.",
    does: "A Taliya soma os recebimentos registrados e mostra o que falta receber quando o valor combinado está informado.",
    outcome: "O resumo deixa claro quais registros usou para chegar aos valores.",
  },
  F3: {
    displayTitle: "Clientes com horário marcado",
    when: "Quando você pergunta quem tem serviço agendado em um dia ou período.",
    does: "A Taliya consulta os horários registrados e lista clientes e serviços correspondentes.",
    outcome: "Você encontra quem está na agenda sem conferir cada horário separadamente.",
  },
  F4: {
    displayTitle: "Serviços prestados",
    when: "Quando você quer ver os serviços marcados como prestados em um período.",
    does: "A Taliya filtra os serviços pelo período e pelo status registrado.",
    outcome: "A lista mostra o que consta como prestado, sem inferir registros não atualizados.",
  },
  F5: {
    displayTitle: "Resumo do período",
    when: "Quando você pede um panorama da atividade em um período.",
    does: "A Taliya reúne serviços, horários, orçamentos e recebimentos registrados nesse intervalo.",
    outcome: "Você acompanha o período com base nos dados disponíveis.",
  },
  F6: {
    displayTitle: "Orçamentos aguardando resposta",
    when: "Quando você quer encontrar orçamentos que constam sem resposta.",
    does: "A Taliya lista as propostas com esse status e mostra cliente e data registrados.",
    outcome: "Você decide se quer retomar o contato ou criar um lembrete.",
  },
  F7: {
    displayTitle: "Serviços com saldo a receber",
    when: "Quando você pergunta quais serviços ainda têm valor a receber.",
    does: "A Taliya compara o valor combinado com os recebimentos registrados e mostra apenas o que consegue calcular.",
    outcome: "A lista mostra apenas saldos que podem ser calculados a partir dos registros.",
  },
  F8: {
    displayTitle: "Fechamento do expediente",
    when: "Quando você pede para fechar o dia e ver o que ficou registrado.",
    does: "A Taliya reúne serviços concluídos, recebimentos informados, horários de amanhã e lembretes criados.",
    outcome: "Você vê o que aconteceu e o que deixou combinado para depois.",
  },
  G1: {
    displayTitle: "Criar orçamento",
    when: "Quando você pede para preparar uma proposta para um cliente.",
    does: "Organiza os serviços, valores e condições informados em um orçamento para revisar.",
    outcome: "O documento fica ligado ao cliente e ao serviço correspondente.",
  },
  G2: {
    displayTitle: "Guardar documento",
    when: "Quando você pede para guardar um contrato ou outro arquivo.",
    does: "Relaciona o documento ao cliente e ao serviço que você indicar.",
    outcome: "O arquivo fica disponível no contexto correspondente.",
  },
  G3: {
    displayTitle: "Encontrar documento",
    when: "Quando você procura um arquivo ou documento já registrado.",
    does: "Busca pelo cliente, serviço ou descrição informados.",
    outcome: "Você encontra o documento relacionado sem procurar em conversas separadas.",
  },
  G4: {
    displayTitle: "Consultar versões",
    when: "Quando você quer ver uma versão anterior de um orçamento.",
    does: "Mostra as versões registradas e mantém a versão atual identificada.",
    outcome: "O histórico permite consultar as alterações feitas na proposta.",
  },
  G5: {
    displayTitle: "Documentos do cliente",
    when: "Quando você quer localizar os arquivos relacionados a um cliente.",
    does: "Reúne os documentos registrados para esse cliente e seus serviços.",
    outcome: "Você consulta os arquivos no contexto do cliente.",
  },
  G12: {
    displayTitle: "Histórico do serviço",
    when: "Quando você quer retomar o que aconteceu com um serviço.",
    does: "Reúne o orçamento, os horários, os recebimentos e os documentos relacionados que estão registrados.",
    outcome: "Você acompanha o serviço a partir das informações disponíveis no histórico.",
  },
};

const featuredFlowSummaries: Record<string, string> = {
  A1: "Identifica a conversa e leva para a rotina certa.",
  A2: "Responde duvidas simples sem ocupar a recepcao.",
  A3: "Organiza pedidos de alunos atuais por rotina.",
  A5: "Pausa a automação e entrega o caso com contexto.",
  A10: "Mostra conversas abertas antes de serem esquecidas.",
  B1: "Confirma presenca e atualiza a agenda.",
  B2: "Registra falta avisada e libera vaga quando pode.",
  B3: "Registra falta sem aviso antes de virar risco.",
  B4: "Transforma vaga aberta em chance de ocupacao.",
  B5: "Confere reposicao e encontra horario possivel.",
  B12: "Recupera experimental faltante antes de esfriar.",
  C1: "Explica planos e puxa o proximo passo comercial.",
  C2: "Leva interesse ate uma experimental marcada.",
  C4: "Retoma a venda depois da aula experimental.",
  C5: "Retoma interessado parado sem insistencia.",
  C6: "Organiza dados, pagamento e inicio do aluno.",
  C7: "Responde objecoes sem sair da politica comercial.",
  D1: "Lembra vencimento antes de virar atraso.",
  D2: "Organiza cobrancas por atraso e prioridade.",
  D3: "Envia Pix, link ou segunda via correta.",
  D5: "Acompanha renovacoes antes do vencimento.",
  D6: "Leva excecoes financeiras para aprovacao.",
  D14: "Resume recebimentos, atrasos e dinheiro pendente.",
  E1: "Percebe queda de frequencia antes da perda.",
  E2: "Chama aluno inativo e direciona a resposta.",
  E4: "Sinaliza cancelamento para a equipe agir.",
  E5: "Reativa ex-alunos com criterio.",
  E6: "Transforma feedback em cuidado ou acao.",
  E7: "Lembra o retorno antes da pausa virar abandono.",
  F1: "Reúne os horários da agenda e os lembretes criados para hoje.",
  F2: "Resume o que entrou e o que falta receber com base nos valores registrados.",
  F3: "Lista os clientes com horários registrados no período solicitado.",
  F4: "Mostra os serviços registrados como prestados no período.",
  F5: "Reúne a atividade registrada em serviços, horários, orçamentos e recebimentos.",
  F8: "Fecha o dia com serviços concluídos, recebimentos, agenda de amanhã e lembretes criados.",
  G1: "Prepara o professor antes da aula.",
  G2: "Salva a evolucao logo depois da aula.",
  G3: "Destaca cuidados sem expor dados sensiveis.",
  G4: "Organiza objetivo, progresso e revisoes.",
  G5: "Leva contexto seguro para outras rotinas.",
  G12: "Mostra a historia do aluno em uma linha do tempo.",
  F6: "Lista os orçamentos que constam aguardando resposta.",
  F7: "Lista serviços com valores a receber, quando o combinado e os pagamentos estão registrados.",
};

const featuredFlowNarrative: Record<string, FeaturedFlowNarrative> = {
  A1: {
    whenBullets: ["Contato novo chama no WhatsApp.", "A mensagem mistura preco, horario, experimental ou pedido humano."],
    doesBullets: ["Identifica se e aluno, interessado ou novo contato.", "Entende o pedido e leva para a rotina certa.", "Pede uma pergunta curta ou chama a equipe quando ha risco."],
    outcomeBullets: ["A pessoa recebe uma primeira resposta sem esperar a equipe.", "A recepcao ja ve quem e, o que quer e o proximo passo."],
    inside: [
      { title: "Contato conhecido", text: "Reconhece aluno, interessado antigo ou cria um novo contato simples." },
      { title: "Pedido certo", text: "Valores vao para Vendas, horarios para Agenda e duvidas simples ficam no Atendimento." },
      { title: "Caso sensivel", text: "Dor, lesao, desconto, cancelamento ou irritacao vao para a equipe." },
    ],
  },
  A2: {
    whenBullets: ["Alguem pergunta algo que ja tem regra aprovada.", "A duvida e sobre funcionamento, endereco, reposicao, planos ou experimental."],
    doesBullets: ["Consulta a base cadastrada pelo studio.", "Responde apenas o que esta permitido e evita improviso.", "Deixa uma pendencia quando falta informacao aprovada."],
    outcomeBullets: ["Aluno ou interessado recebe clareza rapida.", "A equipe para de repetir a mesma explicacao durante o dia."],
    inside: [
      { title: "Informacoes simples", text: "Endereco, funcionamento, preparo para aula e tipos de aula." },
      { title: "Regras do studio", text: "Reposicao, ausencia, canais de contato e disponibilidade geral." },
      { title: "Falta informacao", text: "Avisa que a equipe vai confirmar e deixa o dado pendente." },
    ],
  },
  A3: {
    whenBullets: ["Aluno ativo manda mensagem sobre a rotina.", "O pedido pode ser agenda, pagamento, reposicao, falta ou plano."],
    doesBullets: ["Reconhece que a pessoa ja e aluna.", "Entende o assunto e leva para Agenda, Financeiro, Retencao ou Historico.", "Faz uma pergunta curta quando a mensagem nao esta clara."],
    outcomeBullets: ["O aluno nao precisa repetir todo o contexto.", "A recepcao recebe a demanda organizada por tipo de problema."],
    inside: [
      { title: "Pedido de agenda", text: "Falta, reposicao, confirmacao ou troca de horario vao para Agenda." },
      { title: "Financeiro", text: "Pix, vencimento, plano e renovacao seguem para a rotina financeira." },
      { title: "Caso sensivel", text: "Dor, restricao ou cancelamento vao para a equipe com contexto salvo." },
    ],
  },
  A5: {
    whenBullets: ["O assunto pede aprovacao, cuidado ou decisao humana.", "A pessoa pede atendimento humano ou a conversa tem risco."],
    doesBullets: ["Pausa respostas automáticas naquela conversa.", "Resume contato, historico recente, pedido e motivo do cuidado.", "Leva para o responsavel, equipe geral ou dono do studio."],
    outcomeBullets: ["O cliente sente que foi atendido com cuidado.", "A equipe assume sem perder historico nem precisar reler tudo."],
    inside: [
      { title: "Resumo do caso", text: "Mostra quem e a pessoa, o que pediu e por que precisa de cuidado." },
      { title: "Pessoa certa", text: "Leva para o responsavel, equipe geral ou dono do studio." },
      { title: "Conversa pausada", text: "Segura novas respostas automáticas quando continuar sozinha seria ruim." },
    ],
  },
  A10: {
    whenBullets: ["Conversa fica aberta ou a pessoa responde muito depois.", "Um prazo interno de retorno vence e ninguem assumiu."],
    doesBullets: ["Retoma a conversa quando ainda e o mesmo assunto.", "Entende de novo quando a pessoa mudou de tema.", "Avisa a equipe quando existe resposta pendente."],
    outcomeBullets: ["Menos interessados e alunos esquecidos no WhatsApp.", "A equipe sabe o que ainda esta aberto, resolvido ou atrasado."],
    inside: [
      { title: "Mesmo assunto", text: "Continua a conversa antiga sem recomecar do zero." },
      { title: "Assunto novo", text: "Quando a pessoa muda de tema, leva para a rotina certa." },
      { title: "Prazo vencido", text: "Interessado quente, aluno aguardando equipe ou caso critico viram prioridade." },
    ],
  },
  B1: {
    whenBullets: ["A aula esta chegando e o studio precisa confirmar presenca.", "Existe uma janela configurada para lembrar alunos antes da aula."],
    doesBullets: ["Envia confirmacao somente para aulas e planos configurados.", "Entende se o aluno confirmou, faltou, quer remarcar ou tem duvida.", "Atualiza a agenda ou leva para a rotina certa."],
    outcomeBullets: ["Aluno recebe lembrete objetivo antes da aula.", "A equipe ve quem vai, quem faltou e quem ainda nao respondeu."],
    inside: [
      { title: "Aluno confirma", text: "Marca a presenca prevista e mantem a turma organizada." },
      { title: "Aluno nao vai", text: "Registra falta avisada para aplicar regra e liberar vaga." },
      { title: "Aluno pergunta", text: "Endereco, preparo ou remarcacao seguem para a rotina correta." },
    ],
  },
  B2: {
    whenBullets: ["Aluno avisa que nao vai conseguir ir.", "A falta pode gerar credito, liberar vaga ou exigir aprovacao."],
    doesBullets: ["Identifica qual aula esta sendo cancelada.", "Confere prazo, plano e regra de reposicao.", "Libera a vaga quando permitido ou leva excecao para a equipe."],
    outcomeBullets: ["Aluno entende o que acontece com a falta.", "O studio recupera vagas sem conferencia manual em toda conversa."],
    inside: [
      { title: "Aula clara", text: "Segue direto quando a mensagem mostra qual aula e." },
      { title: "Regra da falta", text: "Dentro do prazo gera reposicao; fora do prazo registra ou pede aprovacao." },
      { title: "Vaga liberada", text: "Quando pode liberar, procura alguem para ocupar o horario." },
    ],
  },
  B3: {
    whenBullets: ["Aula termina e o aluno marcado nao apareceu.", "A ausencia veio da chamada do professor, check-in ou turma encerrada."],
    doesBullets: ["Registra a ausencia sem aviso.", "Aplica a regra de contato ou acompanhamento.", "Sinaliza recorrencia para Retencao quando o padrao aparece."],
    outcomeBullets: ["A agenda fica correta depois da aula.", "O studio percebe faltas repetidas antes de perder o aluno."],
    inside: [
      { title: "Primeira falta", text: "Registra e pode enviar contato leve se a regra permitir." },
      { title: "Falta repetida", text: "Leva para Retencao quando a presenca esta caindo." },
      { title: "Justificativa", text: "Caso sensivel depois da falta vai para a equipe ou Historico." },
    ],
  },
  B4: {
    whenBullets: ["Uma vaga abre por falta, cancelamento ou lista de espera.", "O horario tem chance de ser ocupado por outro aluno."],
    doesBullets: ["Busca candidatos com reposicao, lista de espera ou preferencia de horario.", "Convida na politica definida pelo studio.", "Registra aceite, recusa, falta de resposta ou pedido de outro horario."],
    outcomeBullets: ["A turma fica mais cheia sem correria manual.", "O studio perde menos dinheiro com horario vazio."],
    inside: [
      { title: "Pessoa certa", text: "Prioriza reposicao pendente, lista de espera ou aluno que combina com o horario." },
      { title: "Convite", text: "Chama uma pessoa por vez ou sugere uma lista curta para a equipe." },
      { title: "Resposta", text: "Aceitou, reserva; recusou, chama o proximo; silencio espera o prazo." },
    ],
  },
  B5: {
    whenBullets: ["Aluno pede reposicao, remarcacao ou encaixe.", "O pedido depende de direito a reposicao, regra e disponibilidade real."],
    doesBullets: ["Confere se o aluno tem direito a reposicao.", "Procura horario possivel dentro das restricoes.", "Reserva, coloca em espera ou leva pedido especial para a equipe."],
    outcomeBullets: ["Aluno recebe opcoes objetivas em vez de troca longa de mensagens.", "A equipe nao precisa cruzar agenda e regra manualmente."],
    inside: [
      { title: "Direito a repor", text: "Confere reposicao disponivel, vencida, inexistente ou dependente de aprovacao." },
      { title: "Horario", text: "Busca turma equivalente, capacidade e preferencia do aluno." },
      { title: "Conclusao", text: "Escolheu horario, reserva; sem opcao, deixa em espera para a equipe." },
    ],
  },
  B12: {
    whenBullets: ["Interessado faltou, cancelou ou pediu nova experimental.", "A oportunidade pode esfriar se ninguem retomar rapido."],
    doesBullets: ["Identifica se foi falta sem aviso, cancelamento com aviso ou remarcacao.", "Tenta recuperar o interesse com limite de tentativas.", "Conecta com Agenda para nova vaga ou com Vendas para retomar contato."],
    outcomeBullets: ["Menos experimentais perdidas depois do primeiro agendamento.", "A equipe sabe quem ainda vale tentar converter."],
    inside: [
      { title: "Faltou sem aviso", text: "Primeira falta retoma contato; repeticao pode encerrar a oportunidade." },
      { title: "Cancelou", text: "Pede nova preferencia ou registra que o interesse esfriou." },
      { title: "Remarcou", text: "Busca nova vaga sem gastar mensagens repetidas demais." },
    ],
  },
  C1: {
    whenBullets: ["Interessado pergunta preco, plano, pacote ou frequencia.", "A conversa ainda precisa virar escolha de proximo passo."],
    doesBullets: ["Responde com a politica comercial aprovada.", "Pergunta frequencia e objetivo para orientar melhor.", "Leva para experimental, matricula ou equipe quando precisa negociacao."],
    outcomeBullets: ["Interessado entende valores sem esperar a recepcao.", "A venda continua com contexto melhor para fechar."],
    inside: [
      { title: "Preco", text: "Explica valores permitidos sem inventar desconto." },
      { title: "Perfil do interesse", text: "Entende frequencia desejada e objetivo principal." },
      { title: "Proximo passo", text: "Conduz para experimental, matricula ou aprovacao comercial." },
    ],
  },
  C2: {
    whenBullets: ["Alguem quer conhecer o studio ou fazer aula teste.", "Atendimento ou Vendas precisam transformar interesse em horario marcado."],
    doesBullets: ["Coleta nome e preferencia de turno quando necessario.", "Consulta disponibilidade com Agenda.", "Reserva, pede confirmacao ou chama humano se houver restricao sensivel."],
    outcomeBullets: ["Interessado sai com um proximo passo concreto.", "A equipe perde menos oportunidades por demora no agendamento."],
    inside: [
      { title: "Informacoes essenciais", text: "Nome, turno preferido e se ja fez Pilates, sem formulario longo." },
      { title: "Horario possivel", text: "Busca vaga experimental dedicada ou turma com capacidade." },
      { title: "Reserva", text: "Confirma horario ou deixa pendencia quando nao existe opcao boa." },
    ],
  },
  C4: {
    whenBullets: ["A pessoa fez a experimental e ainda nao virou aluna.", "Existe uma janela ideal para continuar a conversa."],
    doesBullets: ["Retoma no momento certo com contexto da visita.", "Responde duvidas finais sobre plano, horario ou matricula.", "Leva para fechamento ou equipe comercial quando precisa decisao."],
    outcomeBullets: ["O interessado nao esfria depois da aula.", "O studio aumenta a chance de transformar visita em plano."],
    inside: [
      { title: "Registro da visita", text: "Usa registro da experimental e interesse demonstrado." },
      { title: "Duvida final", text: "Resolve preco, horario, plano ou inseguranca comum." },
      { title: "Fechamento", text: "Encaminha para matricula, pagamento ou equipe comercial." },
    ],
  },
  C5: {
    whenBullets: ["Interessado parou de responder ou ficou sem decisao.", "A oportunidade ainda esta aberta, mas precisa ser retomada com cuidado."],
    doesBullets: ["Retoma com poucas mensagens e tom apropriado.", "Registra resposta, silencio, perda ou pedido de equipe.", "Para quando a pessoa nao quer continuar."],
    outcomeBullets: ["A equipe recupera oportunidades sem parecer insistente.", "A lista comercial fica clara entre quente, morno, perdido e pendente."],
    inside: [
      { title: "Ritmo de contato", text: "Define quantas tentativas fazer e quando parar." },
      { title: "Quando responde", text: "Interesse volta para experimental ou matricula." },
      { title: "Sem interesse", text: "Recusa, silencio longo ou outro studio encerram com registro." },
    ],
  },
  C6: {
    whenBullets: ["Interessado decide entrar ou pede o proximo passo.", "Faltam dados, contrato, pagamento, horario ou inicio das aulas."],
    doesBullets: ["Organiza dados obrigatorios e pendencias.", "Conecta pagamento, contrato e agenda de inicio.", "Deixa pendencia ou chama a equipe quando existe excecao."],
    outcomeBullets: ["Novo aluno entra com menos atrito.", "A equipe sabe exatamente o que falta para ativar a matricula."],
    inside: [
      { title: "Informacoes para entrar", text: "Confere cadastro minimo, plano escolhido e horario desejado." },
      { title: "Pagamento e contrato", text: "Leva pagamento, contrato ou pendencia para o financeiro." },
      { title: "Primeira aula", text: "Depois de confirmado, prepara Agenda e Historico inicial." },
    ],
  },
  C7: {
    whenBullets: ["Interessado diz que esta caro, sem tempo ou inseguro.", "A pessoa compara com outro studio ou trava antes de fechar."],
    doesBullets: ["Identifica o tipo de objecao.", "Responde com argumentos aprovados e sem prometer fora da regra.", "Chama a equipe quando a negociacao precisa decisao."],
    outcomeBullets: ["A conversa comercial continua com qualidade.", "A equipe entra apenas quando existe chance real ou excecao."],
    inside: [
      { title: "Duvida de preco", text: "Explica valor e frequencia sem liberar desconto fora da regra." },
      { title: "Falta de tempo", text: "Mostra horarios possiveis ou ajusta a frequencia desejada." },
      { title: "Inseguranca", text: "Convida para experimentar ou falar com equipe quando precisa cuidado." },
    ],
  },
  D1: {
    whenBullets: ["Mensalidade esta perto de vencer.", "O studio quer lembrar sem constranger o aluno."],
    doesBullets: ["Envia lembrete no momento definido.", "Usa tom adequado e informacao de pagamento permitida.", "Registra resposta e encaminha pedido de link ou duvida."],
    outcomeBullets: ["Aluno lembra de pagar antes de virar atraso.", "O financeiro reduz cobrancas manuais repetitivas."],
    inside: [
      { title: "Momento certo", text: "Decide quando avisar conforme regra do studio." },
      { title: "Pede pagamento", text: "Pedido de Pix ou link vai para segunda via." },
      { title: "Economia", text: "Evita mensagem desnecessaria quando a regra manda segurar." },
    ],
  },
  D2: {
    whenBullets: ["Parcela venceu e o pagamento nao entrou.", "A cobranca muda conforme dias de atraso e historico."],
    doesBullets: ["Separa o atraso pelo tempo em aberto.", "Envia comunicacao adequada ou deixa pendencia para casos sensiveis.", "Avisa sobre bloqueio, excecao ou aprovacao quando necessario."],
    outcomeBullets: ["Aluno entende a pendencia sem constrangimento excessivo.", "Responsavel financeiro ganha fila clara de cobrancas importantes."],
    inside: [
      { title: "Tempo de atraso", text: "Poucos dias, atraso recorrente e limite critico mudam o tom." },
      { title: "Pedido do aluno", text: "Pagamento, segunda via, contestacao ou excecao seguem para o responsavel certo." },
      { title: "Caso sensivel", text: "Desconto, contestacao ou bloqueio vao para a equipe antes de qualquer decisao." },
    ],
  },
  D3: {
    whenBullets: ["Aluno pede Pix, link de pagamento ou segunda via.", "Outro fluxo financeiro precisa enviar caminho de pagamento."],
    doesBullets: ["Busca a cobranca correta.", "Envia somente o caminho permitido e atualizado.", "Registra o pedido e deixa pendencia quando falta informacao."],
    outcomeBullets: ["Aluno consegue pagar mais rapido.", "A equipe deixa de reenviar dados manualmente."],
    inside: [
      { title: "Pagamento correto", text: "Confere se o link ou Pix pertence a cobranca certa." },
      { title: "Dados seguros", text: "Nao inventa chave Pix, valor ou vencimento." },
      { title: "Nao encontrou", text: "Se nao encontra a cobranca, deixa pendencia para o responsavel." },
    ],
  },
  D5: {
    whenBullets: ["Plano esta perto de vencer ou aluno quer renovar.", "Pode ser mesma continuidade, troca de plano ou aprovacao."],
    doesBullets: ["Identifica plano atual, vencimento e uso.", "Mostra o caminho de renovacao permitido.", "Prepara pagamento, contrato ou pendencia para aprovacao."],
    outcomeBullets: ["Aluno recebe proposta clara de continuidade.", "O studio perde menos renovacoes por esquecimento."],
    inside: [
      { title: "Mesmo plano", text: "Segue renovacao simples quando nada mudou." },
      { title: "Mudanca", text: "Troca de frequencia, horario ou valor leva para o responsavel certo." },
      { title: "Pendencia", text: "Contrato, pagamento ou excecao ficam visiveis para equipe." },
    ],
  },
  D6: {
    whenBullets: ["Surge desconto, reembolso, pausa, cancelamento ou mudanca de vencimento.", "O pedido mexe em regra financeira sensivel."],
    doesBullets: ["Nao decide sozinho.", "Organiza pedido, historico e impacto financeiro.", "Leva para a pessoa responsavel aprovar ou negar."],
    outcomeBullets: ["Aluno recebe retorno mais seguro.", "A equipe evita excecoes liberadas sem controle."],
    inside: [
      { title: "Regra aprovada", text: "Quando o studio ja definiu a regra, prepara resposta para aprovacao." },
      { title: "Pedido sensivel", text: "Desconto, reembolso e pausa ficam com a pessoa responsavel." },
      { title: "Registro", text: "Qualquer aprovacao fica registrada para financeiro e gestao." },
    ],
  },
  D14: {
    whenBullets: ["Fim do mes, dono abre financeiro ou quer resumo rapido.", "Existem recebimentos, atrasos, renovacoes e pendencias espalhadas."],
    doesBullets: ["Agrupa os principais numeros do mes.", "Mostra dinheiro pendente e acoes possiveis.", "Deixa pendencia quando um ponto precisa de decisao."],
    outcomeBullets: ["Responsavel entende o financeiro sem montar planilha do zero.", "A operacao sabe onde cobrar, renovar ou investigar."],
    inside: [
      { title: "Resumo do mes", text: "Recebido, atrasado, renovacoes proximas e pendencias." },
      { title: "Onde agir", text: "Mostra onde cobrar, renovar, conciliar ou aprovar excecao." },
      { title: "Sem acao", text: "Quando esta tudo certo, apenas registra o fechamento." },
    ],
  },
  E1: {
    whenBullets: ["Aluno comeca a faltar mais que o proprio padrao.", "A queda aparece antes de um pedido claro de cancelamento."],
    doesBullets: ["Compara frequencia recente com historico do aluno.", "Prepara abordagem cuidadosa ou pendencia para equipe.", "Leva para Agenda, Historico ou equipe conforme causa provavel."],
    outcomeBullets: ["A equipe age antes que o aluno desapareca.", "O aluno percebe cuidado em vez de uma cobranca fria."],
    inside: [
      { title: "Sinais de queda", text: "Faltas, reposicoes acumuladas e queda recente aparecem no radar." },
      { title: "Caminho leve", text: "Mensagem de cuidado quando a regra permite contato." },
      { title: "Risco alto", text: "Insatisfacao, dor ou cancelamento vao para a equipe." },
    ],
  },
  E2: {
    whenBullets: ["Aluno ativo fica muitos dias sem aparecer.", "A janela de inatividade configurada foi atingida."],
    doesBullets: ["Separa alunos por tempo sem presenca e perfil.", "Envia retomada cuidadosa ou deixa pendencia.", "Encaminha resposta para Agenda, Retencao ou equipe."],
    outcomeBullets: ["Aluno recebe convite de retorno no momento certo.", "O studio reduz perdas silenciosas de alunos ativos."],
    inside: [
      { title: "Tempo sem vir", text: "Poucos dias, pausa media e abandono provavel mudam a abordagem." },
      { title: "Quer voltar", text: "Vai para Agenda; problema sensivel vai para a equipe." },
      { title: "Baixa chance", text: "Evita contato repetido quando a chance de retorno e baixa." },
    ],
  },
  E4: {
    whenBullets: ["Aluno fala em cancelar, pausar ou mostra insatisfacao.", "O risco e alto demais para uma resposta comum."],
    doesBullets: ["Pausa mensagens comerciais automáticas.", "Resume o risco, historico e motivo percebido.", "Chama a pessoa responsavel para tratar com cuidado."],
    outcomeBullets: ["Aluno nao recebe resposta fria em um momento delicado.", "Responsavel entra com contexto para tentar salvar a relacao."],
    inside: [
      { title: "Sinais de saida", text: "Cancelamento, pausa, reclamacao e queda forte viram prioridade." },
      { title: "Caso sensivel", text: "Vai para a pessoa responsavel com resumo claro." },
      { title: "Contexto completo", text: "Financeiro, agenda e historico entram no resumo quando importam." },
    ],
  },
  E5: {
    whenBullets: ["Existe ex-aluno elegivel para reativacao.", "O studio quer recuperar antigos alunos com criterio."],
    doesBullets: ["Separa quem faz sentido chamar.", "Prepara abordagem conforme motivo de saida e tempo parado.", "Acompanha resposta sem misturar com alunos ativos."],
    outcomeBullets: ["O studio recupera oportunidades antigas com controle.", "Ex-aluno recebe convite relevante, nao contato generico."],
    inside: [
      { title: "Tipo de ex-aluno", text: "Recente, antigo, pausado ou perdido por problema de agenda." },
      { title: "Mensagem certa", text: "Sugere abordagem, limite de tentativas e aprovacao quando precisa." },
      { title: "Quando responde", text: "Interesse vai para Vendas ou Agenda; sem interesse pausa contato." },
    ],
  },
  E6: {
    whenBullets: ["Alguem reclama, volta, faz experimental ou passa por experiencia importante.", "O studio precisa ouvir sem deixar feedback solto."],
    doesBullets: ["Pede feedback no momento certo.", "Entende se e elogio, duvida, reclamacao ou risco.", "Encaminha o que exige atencao para responsavel."],
    outcomeBullets: ["Aluno sente que foi ouvido.", "Problemas aparecem antes de virarem cancelamento ou reputacao ruim."],
    inside: [
      { title: "Pergunta curta", text: "Pede feedback depois de momentos importantes." },
      { title: "Tipo de resposta", text: "Elogio, duvida, problema de rotina ou insatisfacao." },
      { title: "Proximo cuidado", text: "Risco vai para Retencao; elogio fica registrado." },
    ],
  },
  E7: {
    whenBullets: ["Pausa ou trancamento tem data prevista para acabar.", "O aluno pode voltar, adiar ou cancelar de vez."],
    doesBullets: ["Acompanha a data de retorno.", "Chama o aluno antes do fim da pausa.", "Conecta com Agenda, Financeiro ou equipe conforme resposta."],
    outcomeBullets: ["Aluno nao fica esquecido depois da pausa.", "O studio aumenta a chance de recuperar a rotina."],
    inside: [
      { title: "Antes da data", text: "Lembra com antecedencia e pergunta intencao de retorno." },
      { title: "Quer voltar", text: "Leva para Agenda escolher horario e Financeiro se houver renovacao." },
      { title: "Nao consegue voltar", text: "Novo problema ou cancelamento vira atendimento humano." },
    ],
  },
  F1: {
    whenBullets: ["Gestor abre o sistema no comeco do dia.", "Existem pendencias em varias rotinas ao mesmo tempo."],
    doesBullets: ["Reune agenda, financeiro, vendas, retencao e casos com a equipe.", "Ordena pelo impacto e urgencia.", "Abre a rotina responsavel ou deixa pendencia quando precisa decisao."],
    outcomeBullets: ["Responsavel sabe por onde comecar.", "O dia deixa de depender de procurar problemas em varias telas."],
    inside: [
      { title: "Prioridades reais", text: "Vagas abertas, interessados quentes, atrasos, riscos e casos com a equipe." },
      { title: "Prioridade", text: "O que tem impacto maior aparece primeiro." },
      { title: "Proxima acao", text: "Caso simples abre a rotina certa; decisao fica pendente." },
    ],
  },
  F2: {
    whenBullets: ["Existem atrasos, vagas abertas, renovacoes ou vendas paradas.", "O dono quer entender onde tem dinheiro preso."],
    doesBullets: ["Calcula impacto financeiro por rotina.", "Mostra quais acoes destravam valor.", "Direciona para Agenda, Vendas, Financeiro ou Retencao."],
    outcomeBullets: ["Dono entende o custo real da desorganizacao.", "A equipe decide onde agir primeiro para recuperar valor."],
    inside: [
      { title: "Onde perde", text: "Vaga vazia, mensalidade atrasada, plano vencendo e interessado parado." },
      { title: "Maior impacto", text: "Mostra qual area explica mais dinheiro parado." },
      { title: "Proximo passo", text: "Leva para a rotina que resolve a perda principal." },
    ],
  },
  F3: {
    whenBullets: ["Alguma rotina precisa de aprovacao, excecao ou decisao da equipe.", "Casos ficam espalhados entre conversas, pendencias e responsaveis."],
    doesBullets: ["Agrupa aprovacoes, excecoes e conversas sensiveis.", "Mostra contexto e responsavel sugerido.", "Permite aprovar, editar, recusar ou encaminhar."],
    outcomeBullets: ["Nada fica perdido entre WhatsApp e sistema.", "O time sabe exatamente quais decisoes precisa tomar."],
    inside: [
      { title: "O que aparece", text: "Aprovacoes, excecoes, conversas sensiveis e dados faltando." },
      { title: "Aprovar ou ajustar", text: "Aprovar continua o caso; editar ajusta antes de enviar." },
      { title: "Encaminhar", text: "Caso pode ir para responsavel certo sem perder contexto." },
    ],
  },
  F4: {
    whenBullets: ["O mesmo problema aparece muitas vezes.", "Faltas, atrasos, remarcacoes ou duvidas repetidas viram padrao."],
    doesBullets: ["Identifica repeticao entre rotinas.", "Transforma casos soltos em alerta de gestao.", "Sugere ajuste de regra, mensagem ou processo."],
    outcomeBullets: ["O dono deixa de apagar incendio isolado.", "A operacao enxerga qual rotina precisa melhorar."],
    inside: [
      { title: "Problema repetido", text: "Turma vazia, aluno faltando, preco travando venda ou atraso recorrente." },
      { title: "O que mudar", text: "Sugere mudar regra, mensagem, responsavel ou prioridade." },
      { title: "Quem resolve", text: "Leva para a area que consegue resolver a causa." },
    ],
  },
  F5: {
    whenBullets: ["Chega o fechamento semanal.", "Gestor quer uma visao rapida da operacao."],
    doesBullets: ["Resume casos resolvidos, pendentes, perdas e economia.", "Mostra recomendacoes e pendencias importantes.", "Destaca vendas, agenda, financeiro, retencao e decisoes da equipe."],
    outcomeBullets: ["Gestor entende a semana sem perguntar para cada area.", "A operacao fecha o ciclo com prioridades claras."],
    inside: [
      { title: "Resumo da semana", text: "Casos resolvidos, pendentes, perdas, economia e recomendacoes." },
      { title: "Proximas acoes", text: "Enviar resumo, deixar pendencias ou sugerir ajustes." },
      { title: "Tudo certo", text: "Quando tudo esta em ordem, mostra que nao ha acao urgente." },
    ],
  },
  F8: {
    whenBullets: ["Dono quer saber se a Taliya esta funcionando bem.", "Existe fila, caso parado ou regra fraca atrasando a operacao."],
    doesBullets: ["Mostra volume, resolucao, pendencias e aprovacoes por rotina.", "Aponta gargalos por responsavel ou rotina.", "Recomenda ajuste de regra, equipe ou prioridade."],
    outcomeBullets: ["Responsavel entende se a operacao esta fluindo.", "Fica claro onde melhorar regra, processo ou atendimento humano."],
    inside: [
      { title: "Resumo por rotina", text: "Casos resolvidos, pendencias, passagem para equipe e tempo de resposta." },
      { title: "Onde trava", text: "Mostra rotina ou responsavel que esta acumulando fila." },
      { title: "Como melhorar", text: "Sugere revisar regra, aprovacao ou prioridade." },
    ],
  },
  G1: {
    whenBullets: ["Professor abre a turma antes da aula.", "Existem observacoes, objetivos, restricoes ou frequencia recente para considerar."],
    doesBullets: ["Reune contexto seguro de cada aluno.", "Mostra cuidados importantes para professor ou equipe autorizada.", "Pede anotacao futura quando falta contexto."],
    outcomeBullets: ["Professor entra na aula mais preparado.", "Aluno sente continuidade no acompanhamento."],
    inside: [
      { title: "Contexto do aluno", text: "Mostra presenca, observacao, objetivo, preferencia e cuidado registrado." },
      { title: "Cuidado importante", text: "Restricao relevante aparece para professor ou equipe autorizada." },
      { title: "Limite seguro", text: "Se o aluno pede orientacao clinica, o caso vai para a equipe." },
    ],
  },
  G2: {
    whenBullets: ["Aula termina ou professor adiciona observacao.", "A evolucao precisa ficar registrada de forma util."],
    doesBullets: ["Facilita nota por texto, voz transcrita ou campos guiados.", "Conecta observacao ao historico do aluno.", "Leva para Retencao, Agenda ou cuidado quando a nota indica risco."],
    outcomeBullets: ["A equipe nao perde informacoes importantes.", "O acompanhamento fica mais profissional e facil de consultar."],
    inside: [
      { title: "Como registra", text: "Pode ser texto, voz transcrita, anotacao simples ou presenca/falta." },
      { title: "Nota simples", text: "Observacao entra no historico sem atrapalhar a rotina da aula." },
      { title: "Sinal de atencao", text: "Queda de frequencia, horario ou restricao vao para a rotina certa." },
    ],
  },
  G3: {
    whenBullets: ["Existe dor, lesao, gravidez, restricao ou cuidado relevante.", "A informacao precisa aparecer internamente com seguranca."],
    doesBullets: ["Registra e destaca para professor ou equipe autorizada.", "Limita onde essa informacao aparece.", "Chama a equipe quando aluno pede orientacao ou ha decisao sensivel."],
    outcomeBullets: ["Aluno fica mais protegido.", "Professor e equipe trabalham com informacao segura e visivel."],
    inside: [
      { title: "Cuidado registrado", text: "Fica visivel antes da aula para quem precisa saber." },
      { title: "Limite seguro", text: "Nao responde sobre dor ou saude sem a equipe." },
      { title: "Pergunta sensivel", text: "Mensagem delicada no WhatsApp vai para a equipe." },
    ],
  },
  G4: {
    whenBullets: ["Chega revisao de objetivo, progresso ou percepcao do aluno.", "Notas anteriores indicam evolucao, estagnacao ou ajuste necessario."],
    doesBullets: ["Organiza registros anteriores.", "Mostra progresso e pontos parados.", "Sugere revisao ou leva para Retencao quando ha baixa evolucao."],
    outcomeBullets: ["Aluno percebe acompanhamento real.", "O studio ganha argumento de valor para permanencia."],
    inside: [
      { title: "Objetivo novo", text: "Meta criada ou revisada entra no historico do aluno." },
      { title: "Revisao pendente", text: "Objetivo vencido ou parado aparece para a equipe revisar." },
      { title: "Sinal de risco", text: "Baixa evolucao pode virar cuidado de Retencao." },
    ],
  },
  G5: {
    whenBullets: ["Outra rotina precisa entender o historico antes de agir.", "Atendimento, Agenda, Retencao ou Gestao precisam de contexto seguro."],
    doesBullets: ["Entrega apenas o contexto necessario para aquela acao.", "Protege informacao sensivel quando nao deve circular.", "Deixa pendencia quando falta contexto ou permissao."],
    outcomeBullets: ["As respostas ficam mais inteligentes.", "A equipe evita tratar aluno antigo como se fosse novo."],
    inside: [
      { title: "Quem precisa", text: "Atendimento, Agenda, Retencao e Gestao usam contexto quando ajuda a decidir." },
      { title: "Contexto seguro", text: "Resumo interno mostra so o necessario para aquela acao." },
      { title: "Sem permissao", text: "Informacao sensivel fica bloqueada ou vai para a equipe." },
    ],
  },
  G12: {
    whenBullets: ["Equipe abre o perfil do aluno ou precisa decidir rapido.", "Eventos de presenca, pagamento, conversa e evolucao estao espalhados."],
    doesBullets: ["Reune eventos importantes em uma linha do tempo.", "Mostra informacao conforme papel de quem acessa.", "Aponta lacunas ou conflitos que precisam de acao."],
    outcomeBullets: ["Responsavel entende o aluno em poucos minutos.", "Decisoes saem com contexto completo, nao por memoria."],
    inside: [
      { title: "Historico reunido", text: "Presenca, falta, reposicao, pagamento, conversa, objetivo e restricao." },
      { title: "Resumo util", text: "Mostra o que importa para equipe ou Taliya agir." },
      { title: "Falta ou conflito", text: "Informacao ausente ou divergente vira pendencia para a equipe." },
    ],
  },
};

const reviewedFlowSummaries: Record<string, string> = {
  A1: "Registra o contato e mantém o pedido inicial ligado ao cliente.",
  A2: "Consulta as informações registradas e sinaliza o que ainda precisa ser informado.",
  A3: "Reúne serviços, horários, documentos e recebimentos associados ao cliente.",
  A5: "Encaminha o pedido à pessoa responsável com o contexto organizado.",
  A10: "Cria um lembrete para retomar a conversa no momento combinado.",
  B1: "Marca o serviço na agenda e mantém o horário ligado ao cliente.",
  B2: "Cancela o horário e preserva o registro do serviço.",
  B3: "Atualiza o status do serviço na agenda.",
  B4: "Consulta os horários disponíveis para o serviço solicitado.",
  B5: "Remarca o serviço e mantém o histórico da alteração.",
  B12: "Cria um lembrete para acompanhar o próximo horário do serviço.",
  C1: "Organiza serviços avulsos, pacotes e planos com seus detalhes.",
  C2: "Monta um orçamento com cliente, serviço, valores e revisão.",
  C4: "Ajusta o orçamento e preserva as versões anteriores.",
  C5: "Registra quando a proposta aguarda retorno e permite retomar o assunto.",
  C6: "Relaciona a contratação informada ao serviço e ao cliente.",
  C7: "Mantém escopo, valor e condições junto do serviço combinado.",
  D1: "Registra o pagamento que você informou no serviço correspondente.",
  D2: "Consulta o que foi recebido e quanto falta receber, com base nos registros.",
  D3: "Cria um lembrete de cobrança e prepara uma mensagem para sua revisão.",
  D5: "Organiza pagamentos informados e seus status por serviço.",
  D6: "Atualiza um lançamento após a correção informada por você.",
  D14: "Reúne recebimentos registrados e mostra o saldo quando há dados para calculá-lo.",
  E1: "Cria um lembrete por texto ou voz com data e contexto.",
  E2: "Lista lembretes criados por data, cliente, serviço ou situação.",
  E4: "Altera o texto ou a data de um lembrete existente.",
  E5: "Marca como concluído o lembrete que você resolveu.",
  E6: "Relaciona o lembrete ao cliente, serviço ou documento correspondente.",
  E7: "Guarda a próxima ação e a data combinada para retomá-la.",
  F1: "Reúne os horários da agenda e os lembretes criados para hoje.",
  F2: "Resume o que entrou e o que falta receber com base nos valores registrados.",
  F3: "Lista os clientes com horários registrados no período solicitado.",
  F4: "Mostra os serviços registrados como prestados no período.",
  F5: "Reúne a atividade registrada em serviços, horários, orçamentos e recebimentos.",
  F8: "Fecha o dia com serviços concluídos, recebimentos, agenda de amanhã e lembretes criados.",
  G1: "Cria uma proposta ligada ao cliente e ao serviço.",
  G2: "Guarda o contrato no contexto do cliente e do serviço.",
  G3: "Localiza arquivos e documentos pelo cliente ou trabalho relacionado.",
  G4: "Consulta versões anteriores do orçamento sem perder o histórico.",
  G5: "Reúne os documentos relacionados ao cliente e aos seus serviços.",
  G12: "Mostra os registros do serviço, do orçamento aos recebimentos e arquivos.",
  F6: "Lista os orçamentos que constam aguardando resposta.",
  F7: "Lista serviços com valores a receber, quando o combinado e os pagamentos estão registrados.",
};

function narrative(when: string, does: string[], paths: Array<[string, string]>, result: string[]): FeaturedFlowNarrative {
  return { whenBullets: [when], doesBullets: does, inside: paths.map(([title, text]) => ({ title, text })), outcomeBullets: result };
}

const reviewedFlowNarrative: Record<string, FeaturedFlowNarrative> = {
  A1: narrative("Quando chega um novo contato ou você pede para cadastrar alguém.", ["A Taliya registra o nome e o contato informados.", "Relaciona o cadastro ao serviço ou conversa que você indicar."], [["Já existe cadastro?", "Mostra registros parecidos para você escolher antes de criar outro."], ["Falta um dado?", "Pergunta o que precisa para salvar corretamente."], ["Vínculo incerto", "Deixa o cliente sem vínculo até você indicar o serviço."]], ["O cliente fica cadastrado com os dados que você confirmou."]),
  A2: narrative("Quando você pede para consultar ou corrigir os dados de um cliente.", ["A Taliya procura o cadastro e mostra as informações registradas.", "Altera somente o dado que você pediu para atualizar."], [["Um cadastro encontrado", "Mostra o registro e segue com a consulta ou alteração."], ["Mais de um possível cliente", "Apresenta as opções para você escolher."], ["Nenhum cadastro encontrado", "Avisa e pergunta se você quer cadastrar a pessoa."]], ["Você encontra ou atualiza o cadastro sem completar lacunas por suposição."]),
  A3: narrative("Quando você quer retomar o que já foi combinado com um cliente.", ["A Taliya reúne serviços, horários, orçamentos, recebimentos e documentos registrados.", "Mostra os detalhes relacionados ao pedido que você fez."], [["Há histórico relacionado", "Apresenta os registros por tipo e data."], ["Não há registro sobre o assunto", "Diz o que não encontrou e mostra o que está disponível."], ["Há nomes parecidos", "Pede um dado simples para confirmar o cadastro."]], ["A conversa continua com o contexto que está registrado."]),
  A5: narrative("Quando você pede para falar com alguém da equipe ou surge uma decisão que depende de você.", ["A Taliya organiza o pedido e reúne o contexto já registrado.", "Deixa claro o que precisa da sua decisão."], [["O pedido está dentro do combinado", "Segue com a consulta ou registro solicitado."], ["Falta uma regra ou informação", "Pergunta antes de responder ou alterar um registro."], ["É uma decisão excepcional", "Encaminha o caso à pessoa responsável com o contexto disponível."]], ["A equipe recebe o assunto sem precisar reconstruir a conversa."]),
  A10: narrative("Quando você combina de voltar a falar com um cliente em outra data.", ["A Taliya cria um lembrete com assunto, data e cliente informados.", "Relaciona o lembrete ao cadastro correspondente."], [["Data e cliente estão claros", "Registra o lembrete."], ["Falta a data ou o horário", "Pergunta quando você quer retomar."], ["Já existe lembrete parecido", "Mostra o registro para você escolher entre atualizar ou criar outro."]], ["O retorno fica anotado para o momento combinado."]),
  B1: narrative("Quando você pede para marcar um serviço para um cliente.", ["A Taliya registra cliente, serviço, data e horário informados.", "Vincula o agendamento ao serviço correspondente."], [["As informações estão completas", "Registra o horário na agenda."], ["Falta cliente, serviço ou horário", "Pergunta o dado que falta antes de salvar."], ["O horário está ocupado", "Avisa e pede outra opção."]], ["O horário aparece na agenda ligado ao cliente e ao serviço."]),
  B2: narrative("Quando você pede para cancelar um horário já marcado.", ["A Taliya localiza o agendamento e atualiza o status para cancelado.", "Mantém o serviço e o histórico registrados."], [["Há um único horário correspondente", "Atualiza esse agendamento."], ["Há mais de um horário possível", "Pede que você escolha qual cancelar."], ["Você quer cancelar o serviço inteiro", "Confirma essa diferença antes de alterar o registro."]], ["A agenda mostra o cancelamento sem apagar o histórico do serviço."]),
  B3: narrative("Quando você informa uma mudança em um horário ou serviço agendado.", ["A Taliya localiza o registro e altera somente os dados que você mencionou.", "Mantém o vínculo com cliente e serviço."], [["O registro está identificado", "Aplica a mudança solicitada."], ["Há mais de um registro parecido", "Mostra as opções para você selecionar."], ["A mudança pode conflitar com outro horário", "Avisa antes de salvar e pede sua decisão."]], ["A agenda passa a mostrar a alteração que você confirmou."]),
  B4: narrative("Quando você pergunta quais horários estão disponíveis para um serviço.", ["A Taliya consulta a agenda no dia ou período informado.", "Apresenta os horários livres que encontrar."], [["Há horários livres", "Mostra opções para você escolher."], ["Não há horários livres", "Avisa e pergunta se quer consultar outro período."], ["O período não ficou claro", "Pergunta qual data ou faixa de horário consultar."]], ["Você escolhe entre as opções antes de marcar."]),
  B5: narrative("Quando você pede para mudar o dia ou horário de um serviço marcado.", ["A Taliya localiza o agendamento e atualiza a data ou o horário solicitado.", "Preserva o vínculo com o cliente, serviço e histórico."], [["O novo horário está disponível", "Atualiza o agendamento."], ["O horário escolhido está ocupado", "Avisa e pede outra opção."], ["Há mais de um agendamento possível", "Pede que você identifique qual deve mudar."]], ["O novo horário aparece na agenda e a mudança fica registrada."]),
  B12: narrative("Quando você quer lembrar de confirmar ou combinar um horário depois.", ["A Taliya cria um lembrete com cliente, assunto e data que você indicar.", "Vincula o lembrete ao serviço, quando houver esse registro."], [["Data e assunto foram informados", "Registra o lembrete."], ["Falta definir quando", "Pergunta a data ou o horário."], ["O horário ainda não foi escolhido", "Registra o lembrete sem criar um agendamento."]], ["O próximo passo fica anotado sem marcar um horário antes da hora."]),
  C1: narrative("Quando você cadastra o que oferece ou consulta os formatos de serviço.", ["A Taliya organiza cada serviço como avulso, pacote ou plano.", "Guarda valor, quantidade e frequência quando você os informar."], [["Avulso", "Registra um serviço por atendimento."], ["Pacote", "Registra a quantidade de atendimentos e a validade informadas."], ["Plano", "Registra a frequência e o valor recorrente que você definiu."]], ["Os três formatos ficam claros para usar em orçamentos e na agenda."]),
  C2: narrative("Quando você pede para preparar um orçamento para um cliente.", ["A Taliya reúne serviços, quantidades, valores e condições informados.", "Calcula o total somente com os itens preenchidos e mostra para revisão."], [["Os dados estão completos", "Prepara o orçamento para você conferir."], ["Falta serviço, quantidade ou valor", "Pergunta o que falta e não inventa preço."], ["Há vários itens", "Mostra os itens e o total discriminados."]], ["Você recebe um orçamento organizado para revisar antes de compartilhar."]),
  C4: narrative("Quando você informa que o cliente aprovou um orçamento ou pediu uma alteração.", ["A Taliya atualiza o status ou o detalhe que você indicou.", "Mantém as versões anteriores disponíveis."], [["O cliente aprovou", "Marca a proposta como aprovada."], ["O cliente pediu mudança", "Atualiza a proposta e salva uma nova versão para revisão."], ["A resposta não ficou clara", "Pergunta se deve registrar aprovação, recusa ou alteração."]], ["A situação atual do orçamento fica clara sem apagar versões anteriores."]),
  C5: narrative("Quando você quer encontrar orçamentos enviados que ainda aguardam resposta.", ["A Taliya lista as propostas com esse status, mostrando cliente e data registrados.", "Cria lembrete se você pedir quando quer retomar o contato."], [["Há propostas nesse status", "Mostra a lista encontrada."], ["Não há propostas", "Avisa que não encontrou registros para o filtro."], ["Você quer retomar uma proposta", "Pergunta a data do lembrete; não envia mensagem automaticamente."]], ["Você decide quais propostas retomar e quando."]),
  C6: narrative("Quando você informa que o cliente aprovou e pede para registrar o serviço.", ["A Taliya vincula o serviço ao cliente e ao orçamento correspondente.", "Registra o tipo e os detalhes que você confirmou."], [["O orçamento consta como aprovado", "Registra o serviço com os dados aprovados."], ["A aprovação não está registrada", "Mostra o status e pergunta como quer seguir."], ["Falta data ou horário", "Registra o serviço sem agendar até você informar."]], ["O serviço fica ligado ao cliente e ao orçamento que originou o combinado."]),
  C7: narrative("Quando você pede para alterar escopo, valor ou condições de uma proposta.", ["A Taliya localiza a proposta e aplica as mudanças informadas.", "Atualiza o total e mantém as versões anteriores consultáveis."], [["A proposta e a mudança estão claras", "Prepara uma nova versão para revisão."], ["Há mais de uma proposta possível", "Pede que você escolha qual alterar."], ["Falta preço ou condição", "Pergunta antes de atualizar o total."]], ["A proposta revisada fica pronta para conferir, com histórico preservado."]),
  D1: narrative("Quando você informa que recebeu um valor de um cliente.", ["A Taliya registra o valor recebido no serviço que você indicar.", "Atualiza o saldo somente se o valor combinado também estiver registrado."], [["Cliente e serviço estão identificados", "Registra o recebimento nesse serviço."], ["Falta identificar o serviço", "Mostra opções ou pergunta qual é."], ["O valor total não consta", "Registra o recebimento e informa que não pode calcular o saldo."]], ["O pagamento informado fica ligado ao serviço correto."]),
  D2: narrative("Quando você pergunta quanto ainda falta receber de um cliente ou serviço.", ["A Taliya consulta valor combinado e pagamentos registrados.", "Calcula a diferença quando os dois dados estão disponíveis e mostra a conta."], [["Os valores estão registrados", "Mostra total, recebido e saldo calculado."], ["Falta o valor combinado", "Mostra o que foi recebido e não estima o saldo."], ["Há vários serviços", "Lista as opções para você escolher qual consultar."]], ["Você vê de onde veio o saldo, sem estimativas sobre dados ausentes."]),
  D3: narrative("Quando você combina uma data para cobrar um saldo em aberto.", ["A Taliya cria um lembrete com cliente, serviço, valor e data informados.", "Pode preparar uma mensagem para você revisar se pedir."], [["Data e valor estão definidos", "Registra o lembrete de cobrança."], ["Falta a data", "Pergunta quando você quer cobrar."], ["Você pediu uma mensagem", "Prepara um rascunho para revisão; não envia sem você."]], ["O próximo contato de cobrança fica anotado e sob seu controle."]),
  D5: narrative("Quando você quer consultar pagamentos por cliente, serviço ou período.", ["A Taliya filtra os recebimentos que você registrou.", "Mostra valor, data e serviço relacionado quando esses dados existem."], [["Há pagamentos no filtro", "Lista os registros encontrados."], ["Não há pagamentos correspondentes", "Avisa que não encontrou lançamentos."], ["Falta definir período ou cliente", "Pergunta qual filtro usar."]], ["Você consulta pagamentos lançados sem misturá-los a valores não informados."]),
  D6: narrative("Quando você avisa que um recebimento foi lançado com valor ou informação incorreta.", ["A Taliya localiza o lançamento e mostra o que está registrado.", "Aplica a correção que você confirmar."], [["Há um único lançamento", "Mostra o registro para você confirmar a correção."], ["Há mais de um lançamento possível", "Pede que você escolha qual corrigir."], ["A correção muda um saldo calculado", "Mostra os valores antes de salvar."]], ["O histórico reflete a correção e o saldo, se houver dados para calculá-lo."]),
  D14: narrative("Quando você pede o histórico de recebimentos de um cliente ou período.", ["A Taliya reúne pagamentos registrados com seus serviços e datas.", "Mostra saldo somente quando o valor combinado está disponível."], [["Há lançamentos para o filtro", "Lista os pagamentos e valores encontrados."], ["Falta o valor total", "Mostra os pagamentos sem estimar saldo."], ["Há vários clientes ou serviços", "Pede que você escolha qual consultar."]], ["O histórico fica organizado a partir dos lançamentos existentes."]),
  E1: narrative("Quando você quer guardar uma tarefa para uma data ou horário.", ["A Taliya registra o texto e a data informados.", "Relaciona o lembrete ao cliente ou serviço que você indicar."], [["Texto e data estão claros", "Cria o lembrete."], ["Falta data ou assunto", "Pergunta o que falta."], ["Você pede repetição", "Confirma a frequência antes de registrar lembretes recorrentes."]], ["O lembrete fica disponível para consulta no momento combinado."]),
  E2: narrative("Quando você pergunta quais lembretes já criou.", ["A Taliya consulta os lembretes registrados e filtra por data ou contexto.", "Mostra o assunto e a data de cada resultado."], [["Há lembretes no período", "Lista os que você criou."], ["Não há lembretes na data", "Avisa que não encontrou registros."], ["Você não indicou período", "Pergunta se quer ver hoje, próximos dias ou outra data."]], ["Você encontra os lembretes existentes sem receber tarefas inferidas."]),
  E4: narrative("Quando você pede para alterar o texto, a data ou o horário de um lembrete.", ["A Taliya localiza o lembrete e muda somente o que você indicou.", "Mantém o vínculo com cliente ou serviço relacionado."], [["O lembrete está identificado", "Atualiza o registro."], ["Há lembretes parecidos", "Mostra as opções para você escolher."], ["Falta a nova data", "Pergunta quando quer reagendar."]], ["A próxima consulta mostra os dados atualizados."]),
  E5: narrative("Quando você informa que resolveu algo que estava anotado.", ["A Taliya localiza o lembrete e marca como concluído após sua confirmação."], [["Há um lembrete correspondente", "Atualiza o status para concluído."], ["Há mais de um possível", "Pede que você escolha qual encerrar."], ["O lembrete não foi encontrado", "Avisa e não altera outros registros."]], ["O lembrete deixa de aparecer como algo a fazer e continua no histórico."]),
  E6: narrative("Quando você combina de falar com alguém sobre serviço, orçamento ou documento.", ["A Taliya cria um lembrete com assunto, data e cliente informados.", "Liga o próximo passo ao serviço ou documento quando houver registro."], [["Cliente e data estão definidos", "Salva o lembrete com o contexto."], ["Há nomes parecidos", "Pede confirmação do cadastro."], ["Falta a data", "Pergunta quando você quer retomar o contato."]], ["O retorno fica ligado ao cliente e ao assunto combinado."]),
  E7: narrative("Quando você pergunta qual lembrete vem a seguir ou o que combinou de fazer.", ["A Taliya mostra os lembretes futuros que você registrou, em ordem de data."], [["Há lembretes próximos", "Mostra assunto, data e contexto disponível."], ["Não há lembretes futuros", "Diz que não encontrou próximos registros."], ["Você quer outro período", "Filtra a lista pela data indicada."]], ["Você retoma os próximos passos que anotou, sem tarefas presumidas."]),
  F1: narrative("Quando você pergunta como está o seu dia hoje.", ["A Taliya lista os horários registrados para hoje.", "Acrescenta os lembretes que você criou para essa data."], [["Há horários e lembretes", "Organiza os dois por horário."], ["Há apenas um tipo de registro", "Mostra o que está salvo sem inventar o restante."], ["Não há registros para hoje", "Avisa que agenda e lembretes estão vazios para a data."]], ["Você vê em uma mensagem os compromissos e lembretes registrados para hoje."]),
  F2: narrative("Quando você pergunta quanto recebeu em um período e quanto ainda falta receber.", ["A Taliya soma os recebimentos registrados.", "Calcula o que falta receber quando o valor combinado e os pagamentos estão registrados."], [["Os valores necessários estão registrados", "Mostra quanto entrou e quanto falta receber no período."], ["Falta o valor combinado", "Mostra o que entrou e avisa que não tem como calcular o restante."], ["Falta definir o período", "Pergunta qual mês ou intervalo consultar."]], ["Você vê os valores com base nos registros disponíveis."]),
  F3: narrative("Quando você pergunta quais clientes têm serviço marcado em um dia ou período.", ["A Taliya consulta a agenda e lista cliente, horário e serviço."], [["Há horários no período", "Mostra cada cliente e seu serviço."], ["Não há horários", "Avisa que não encontrou serviços marcados."], ["O período não está claro", "Pergunta qual data ou intervalo consultar."]], ["Você encontra quem está na agenda sem procurar registro por registro."]),
  F4: narrative("Quando você quer ver os serviços marcados como prestados em um período.", ["A Taliya filtra os serviços pelo status registrado e pelas datas solicitadas."], [["Há serviços marcados como prestados", "Lista os registros encontrados."], ["O status não foi atualizado", "Mostra o status salvo e não presume conclusão."], ["Não há resultados", "Avisa que não encontrou serviços prestados no período."]], ["A lista reflete os registros existentes, sem inferir serviços concluídos."]),
  F5: narrative("Quando você pede um panorama da atividade em um período.", ["A Taliya reúne serviços, horários, orçamentos, recebimentos e lembretes registrados.", "Separa os dados por tipo para facilitar a consulta."], [["O período está definido", "Mostra os registros encontrados nessa janela."], ["O período não está claro", "Pergunta quais datas consultar."], ["Uma frente não tem registros", "Informa que não encontrou dados daquela categoria."]], ["Você acompanha o que foi registrado, sem indicadores inventados."]),
  F6: narrative("Quando você pergunta quais orçamentos ainda aguardam resposta.", ["A Taliya consulta o status salvo e filtra as propostas nessa situação."], [["Há propostas aguardando resposta", "Lista cliente, data e valor se estiverem registrados."], ["Não há propostas nesse status", "Avisa que não encontrou orçamentos."], ["O status está desatualizado ou incerto", "Mostra o que consta no registro e não presume a resposta do cliente."]], ["Você encontra propostas registradas como aguardando resposta."]),
  F7: narrative("Quando você pergunta quais serviços ainda têm valor a receber.", ["A Taliya compara o valor combinado com os recebimentos lançados.", "Mostra apenas os valores que consegue calcular com esses dados."], [["Total e recebimentos estão registrados", "Mostra o saldo e os valores usados na conta."], ["Falta algum valor", "Não estima o saldo e informa qual dado está faltando."], ["Há vários serviços do mesmo cliente", "Separa os resultados por serviço."]], ["Você vê quais serviços têm saldo a receber com base nos valores registrados."]),
  F8: narrative("Quando você pede o fechamento do expediente.", ["A Taliya reúne serviços marcados como concluídos e recebimentos informados hoje.", "Mostra os horários de amanhã e lembretes que você criou."], [["Há registros para hoje e amanhã", "Organiza o fechamento por data e tipo."], ["Um status não foi atualizado", "Mostra o que consta sem presumir conclusão."], ["Não há horários ou lembretes para amanhã", "Avisa que não encontrou registros para esses itens."]], ["Você termina o dia com um resumo do que foi registrado e do que vem depois."]),
  G1: narrative("Quando você pede um orçamento ou proposta para um cliente.", ["A Taliya reúne serviços, quantidades, valores e condições informados.", "Prepara o documento para você revisar antes de compartilhar."], [["Os dados estão completos", "Gera o orçamento com itens e total discriminados."], ["Falta preço ou quantidade", "Pergunta antes de calcular o total."], ["O cliente não está identificado", "Pede confirmação antes de vincular a proposta."]], ["O orçamento fica relacionado ao cliente e pronto para conferência."]),
  G2: narrative("Quando você pede para guardar um contrato ou outro arquivo do trabalho.", ["A Taliya registra o arquivo que você anexar e relaciona ao cliente ou serviço indicado."], [["Arquivo e contexto estão definidos", "Guarda o documento no registro correspondente."], ["O arquivo não foi anexado", "Pede que você envie antes de registrar."], ["Há mais de um cliente ou serviço possível", "Pede que você escolha onde guardar."]], ["O documento fica ligado ao contexto certo para encontrar depois."]),
  G3: narrative("Quando você procura um orçamento ou arquivo já registrado.", ["A Taliya busca pelo cliente, serviço ou nome do documento que você informar."], [["Um documento corresponde", "Mostra o arquivo encontrado."], ["Mais de um corresponde", "Lista as opções para você escolher."], ["Nenhum corresponde", "Avisa que não encontrou o arquivo com esses dados."]], ["Você localiza documentos registrados sem procurar em várias conversas."]),
  G4: narrative("Quando você quer consultar uma versão anterior de um orçamento.", ["A Taliya mostra as versões salvas e identifica a versão atual."], [["Há versões anteriores", "Lista as versões disponíveis."], ["Só existe uma versão", "Mostra a atual e informa que não encontrou outras."], ["O orçamento não foi identificado", "Pede outro dado para localizar."]], ["As alterações ficam consultáveis sem confundir as versões."]),
  G5: narrative("Quando você quer encontrar documentos relacionados a um cliente.", ["A Taliya reúne os arquivos e orçamentos vinculados ao cadastro."], [["Há documentos relacionados", "Lista os arquivos por tipo e data."], ["Não há documentos registrados", "Avisa que não encontrou arquivos vinculados."], ["Há clientes com nomes parecidos", "Pede confirmação do cadastro."]], ["Você consulta os documentos no contexto do cliente correto."]),
  G12: narrative("Quando você quer retomar o histórico de um serviço.", ["A Taliya reúne orçamento, horários, recebimentos e documentos ligados ao serviço.", "Mostra os registros por data e tipo."], [["Há registros relacionados", "Organiza as informações encontradas em ordem cronológica."], ["Uma etapa não foi registrada", "Mostra a lacuna sem completar por suposição."], ["O serviço não está identificado", "Pede o cliente ou a descrição para localizar."]], ["Você acompanha o serviço a partir das informações disponíveis."]),
};

function channelsFor(channel: AgentOperationalFlow["channel"]): TaliyaLandingAgentFlow["channels"] {
  if (channel === "hibrido") return ["App", "WhatsApp"];
  if (channel === "sistema") return ["App"];
  return ["WhatsApp"];
}

function fallbackBullets(value: string) {
  return [sentence(value)];
}

function asLandingFlow(flowItem: AgentOperationalFlow): TaliyaLandingAgentFlow {
  const editorial = featuredFlowEditorial[flowItem.code];
  const narrative = reviewedFlowNarrative[flowItem.code] ?? featuredFlowNarrative[flowItem.code];

  return {
    ...flowItem,
    channel: "hibrido",
    mode: "copiloto",
    displayTitle: editorial?.displayTitle ?? flowItem.title,
    summary: reviewedFlowSummaries[flowItem.code] ?? featuredFlowSummaries[flowItem.code] ?? flowItem.result,
    channels: channelsFor(flowItem.channel),
    when: editorial?.when ?? flowItem.trigger,
    does: editorial?.does ?? flowItem.action,
    outcome: editorial?.outcome ?? flowItem.result,
    whenBullets: narrative?.whenBullets ?? fallbackBullets(editorial?.when ?? flowItem.trigger),
    doesBullets: narrative?.doesBullets ?? fallbackBullets(editorial?.does ?? flowItem.action),
    outcomeBullets: narrative?.outcomeBullets ?? fallbackBullets(editorial?.outcome ?? flowItem.result),
    inside: narrative?.inside ?? [],
  };
}

export const taliyaFeaturedAgentFlowsByAgent: Record<string, TaliyaLandingAgentFlow[]> = Object.fromEntries(
  Object.entries(taliyaAgentFlowsByAgent).map(([agentId, flows]) => {
    const featuredCodes = new Set(featuredFlowCodesByAgent[agentId] ?? []);
    return [agentId, flows.filter((flowItem) => featuredCodes.has(flowItem.code)).map(asLandingFlow)];
  }),
);

export const taliyaFeaturedAgentFlowTotal = Object.values(taliyaFeaturedAgentFlowsByAgent).reduce((total, flows) => total + flows.length, 0);
