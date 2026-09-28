import csv
from pathlib import Path

BASE = Path("specs/006-crm-operational-core")
SRC = BASE / "agents-flows-final-flow-contract-matrix.pt-BR.csv"
OUT = BASE / "agents-flows-detailed-mode-rules-matrix.pt-BR.csv"
REVIEW_OUT = BASE / "agents-flows-detailed-mode-rules-review.pt-BR.md"
LIFECYCLE_OUT = BASE / "agents-flows-lifecycle-mode-matrix.pt-BR.csv"
LIFECYCLE_REVIEW_OUT = BASE / "agents-flows-lifecycle-mode-review.pt-BR.md"


def parts(text):
    return [item.strip() for item in text.split(";") if item.strip()]


def allowed(row, mode):
    return mode in [item.strip() for item in row["modos_permitidos"].split(";")]


def s(items):
    seen = []
    for item in items:
        if item and item not in seen:
            seen.append(item)
    return "; ".join(seen)


def bullets(text):
    return [item.strip() for item in text.split(";") if item.strip()]


def write_bullets(lines, items):
    for item in bullets(items):
        clean = item.rstrip(".")
        lines.append(f"- {clean}.")


# id: (action, follows_when, stops_or_calls_when)
RULES = {
    "A1": ("classificar a conversa, abrir atendimento e mandar para a fila certa", "mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido; fila de atendimento esta definida; limite de respostas nao foi atingido", "contato nao foi identificado; mensagem mistura varios assuntos; pedido envolve desconto, saude, privacidade ou reclamacao; fila de atendimento nao tem responsavel; canal, cota, opt-out ou permissao bloqueia resposta"),
    "A2": ("responder duvidas permitidas usando a base aprovada", "pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal; limite por conversa nao foi atingido; fallback esta definido", "pergunta nao esta na base; aluno pede condicao comercial especial; mensagem pede dado privado; conversa ficou confusa ou agressiva; canal, cota, opt-out ou permissao bloqueia resposta"),
    "A3": ("reconhecer aluno existente e encaminhar atendimento com contexto", "telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos; fila destino esta definida; botao de ajuda permanece disponivel", "telefone atende mais de um aluno; cadastro esta duplicado; pedido exige alteracao sensivel; aluno contesta informacao do CRM; canal, cota ou permissao bloqueia acao"),
    "A4": ("responder fora de escopo e criar destino correto", "assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano; destino da tarefa ou caso esta definido; mensagem nao contem risco sensivel", "assunto parece reclamacao; mensagem envolve emergencia, saude ou dado pessoal; lead ou aluno insiste em humano; resposta padrao nao cobre o caso; canal, cota ou permissao bloqueia acao"),
    "A5": ("chamar humano com resumo, fila e prioridade", "gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada; resumo obrigatorio foi gerado; responsavel pode assumir o caso", "fila destino nao existe; prioridade nao pode ser definida; resumo ficou incompleto; caso exige dono ou admin especifico; canal, cota ou permissao bloqueia criacao"),
    "A6": ("registrar consentimento, opt-out ou preferencia de contato", "contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado; responsavel de revisao existe para caso ambiguo; auditoria pode ser registrada", "pedido e ambiguo; telefone e compartilhado; contato pede exclusao ou copia de dados; ha conflito entre responsavel e aluno; canal, cota ou permissao bloqueia confirmacao"),
    "A7": ("tratar identidade, audio, imagem ou midia recebida", "midia e legivel; tipo de midia e aceito; contato esta identificado; conteudo nao traz dado sensivel inesperado; responsavel de revisao esta definido", "midia esta ilegivel; documento parece sensivel; identidade nao confere; arquivo nao e aceito; canal, cota ou permissao bloqueia acao"),
    "A8": ("preparar pedido de privacidade ou dados para aprovacao", "solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados; SLA do caso esta definido; aprovador de privacidade esta definido", "identidade nao esta confirmada; pedido envolve exclusao ou exportacao ampla; ha menor ou responsavel envolvido; dado solicitado nao esta no escopo permitido; aprovacao vence ou permissao bloqueia"),
    "A9": ("validar telefone compartilhado antes de expor informacao", "telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida; responsavel de revisao esta definido; nenhum dado sensivel sera revelado antes da validacao", "mais de um aluno pode ser o solicitante; validacao falha; responsavel diverge do cadastro; pedido tenta acessar historico privado; aprovacao vence ou permissao bloqueia"),
    "A10": ("acompanhar SLA e ciclo de vida do atendimento", "conversa tem status claro; tempo de SLA esta definido; fila destino existe; prioridade foi definida; alerta ainda esta dentro da politica do studio", "SLA venceu; conversa ficou sem dono; prioridade ficou alta ou sensivel; fila destino nao existe; canal, cota ou permissao bloqueia alerta"),
    "B1": ("enviar confirmacao de presenca e registrar resposta", "aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou; template aprovado esta disponivel; limite por aula nao foi atingido", "aula foi alterada ou cancelada; aluno nao esta identificado; ja existe resposta conflitante; aluno pede excecao ou troca; WhatsApp, cota ou permissao bloqueia envio"),
    "B2": ("registrar falta avisada e encaminhar o proximo passo", "aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado; falta ainda nao foi registrada; mensagem usa template aprovado", "aviso chega fora do prazo; nao encontra aluno ou aula; falta ja foi registrada; aluno pede excecao, credito, cancelamento ou reclama; WhatsApp, cota ou permissao bloqueiam o envio"),
    "B3": ("detectar falta sem aviso e abrir recuperacao ou tarefa", "aula terminou; aluno estava previsto na chamada; presenca nao foi registrada; janela de tolerancia passou; responsavel de acompanhamento esta definido", "professor ainda nao fechou chamada; aluno avisou por outro canal; ha conflito de presenca; caso tem recorrencia ou risco de cancelamento; canal, cota ou permissao bloqueia contato"),
    "B4": ("usar vaga aberta para convidar aluno elegivel", "vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito; limite de convites nao foi atingido; convite usa mensagem aprovada", "vaga fecha antes da resposta; ha empate ou lote grande; aluno nao tem credito claro; convite pode furar prioridade; canal, cota ou permissao bloqueia envio"),
    "B5": ("preparar reposicao ou remarcacao para aprovacao", "credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido; impacto na agenda foi calculado; aprovador esta definido", "credito esta vencido ou contestado; aula destino esta lotada; mudanca afeta financeiro ou plano; ha conflito de horario; aprovacao vence ou permissao bloqueia"),
    "B6": ("gerenciar lista de espera e convites", "lista de espera existe; prioridade foi calculada; vaga compativel apareceu; limite de convites permite contato; responsavel por excecao esta definido", "prioridade empata; aluno nao responde no prazo; vaga deixa de existir; pedido envolve excecao de credito; canal, cota ou permissao bloqueia envio"),
    "B7": ("oferecer disponibilidade para aula experimental", "interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido; limite de tentativas nao foi atingido; mensagem aprovada esta disponivel", "interessado pede horario fora da regra; nao ha vaga compativel; lead ja tem experimental marcada; pedido envolve desconto ou excecao; canal, cota ou permissao bloqueia envio"),
    "B8": ("preparar mudanca de horario fixo para aprovacao", "aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado; mensagem de confirmacao esta pronta; aprovador esta definido", "novo horario gera conflito; aluno tem pendencia financeira ou credito afetado; mudanca impacta varios alunos; prazo minimo nao foi cumprido; aprovacao vence ou permissao bloqueia"),
    "B9": ("preparar cancelamento pelo studio e comunicado", "aula a cancelar existe; motivo foi informado; alunos afetados foram listados; reposicao ou credito foi calculado; aprovador esta definido", "cancelamento afeta muitos alunos; ha aluno de primeira aula ou experimental; reposicao ou credito nao esta claro; comunicado nao cobre o caso; aprovacao vence ou permissao bloqueia"),
    "B10": ("resolver conflito de capacidade com aprovacao", "turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado; prioridade do caso foi definida; aprovador esta definido", "capacidade real diverge da configurada; ha conflito entre alunos com direito similar; mudanca afeta grade ou professor; solucao exige remover aluno; aprovacao vence ou permissao bloqueia"),
    "B11": ("preparar ajuste de grade e simulacao de impacto", "mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado; comunicacao necessaria foi listada; aprovador esta definido", "simulacao encontra conflito; impacto financeiro ou contratual aparece; data de vigencia e curta demais; alunos afetados nao foram resolvidos; aprovacao vence ou permissao bloqueia"),
    "B12": ("tratar experimental sem comparecimento", "experimental estava marcada; lead nao compareceu; janela de tolerancia passou; cadencia comercial esta definida; limite de contato nao foi atingido", "lead avisou por outro canal; lead pede remarcacao fora da regra; nao ha nova vaga compativel; lead demonstra objecao sensivel; canal, cota ou permissao bloqueia contato"),
    "B13": ("preparar credito de reposicao para aprovacao", "falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada; destino de excecoes esta definido; aprovador esta definido", "credito e contestado; validade foge da politica; credito afeta plano ou financeiro; ha duplicidade de credito; aprovacao vence ou permissao bloqueia"),
    "B14": ("preparar correcao de presenca para aprovacao", "aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado; impacto da alteracao foi mostrado; aprovador esta definido", "motivo nao foi informado; correcao altera historico sensivel; ha conflito com professor ou aluno; impacto em credito ou financeiro aparece; aprovacao vence ou permissao bloqueia"),
    "B15": ("acompanhar primeira aula e checklist inicial", "aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido; orientacoes foram preparadas; nao ha restricao sensivel pendente", "aluno tem cuidado sem revisao; professor nao esta definido; aula muda de horario; aluno pede remarcacao ou excecao; canal, cota ou permissao bloqueia contato"),
    "B16": ("preparar aula especial ou workshop para aprovacao", "evento foi descrito; capacidade esta definida; prazo e data estao claros; template de comunicacao esta pronto; aprovador esta definido", "capacidade e regra de inscricao conflitam; evento afeta grade regular; preco ou beneficio nao esta definido; comunicacao impacta muitos alunos; aprovacao vence ou permissao bloqueia"),
    "C1": ("responder sobre valores e planos aprovados", "plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial; resposta usa template permitido; limite de conversa nao foi atingido", "lead pede desconto, promessa ou excecao; plano nao esta claro; pergunta mistura financeiro e contrato; resposta pode gerar compromisso comercial; canal, cota ou permissao bloqueia resposta"),
    "C2": ("marcar ou preparar aula experimental", "lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido; limite de tentativas permite contato; lead nao tem experimental duplicada", "lead pede horario indisponivel; nao ha vaga compativel; lead ja fez experimental recente; pedido envolve desconto ou excecao; canal, cota ou permissao bloqueia contato"),
    "C3": ("enviar lembrete de aula experimental", "experimental esta marcada; horario do lembrete chegou; lead tem canal permitido; template aprovado esta disponivel; lembrete ainda nao foi enviado", "aula foi remarcada ou cancelada; lead pediu opt-out; canal falhou; lead responde com objecao ou pedido de mudanca; cota ou permissao bloqueia envio"),
    "C4": ("acompanhar lead depois da aula experimental", "experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida; responsavel comercial esta atribuido; limite de contato nao foi atingido", "lead nao compareceu; professor registrou observacao sensivel; lead pede desconto ou condicao especial; lead demonstra reclamacao; canal, cota ou permissao bloqueia contato"),
    "C5": ("conduzir follow-up comercial dentro da cadencia", "lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato; responsavel comercial esta definido; limite de tentativas nao foi atingido", "lead pediu humano ou parar contato; lead tem objecao sensivel; lead pede desconto ou garantia; conversa esfriou alem do limite; canal, cota ou permissao bloqueia contato"),
    "C6": ("preparar pre-matricula para aprovacao", "lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido; responsavel comercial esta atribuido; aprovador esta definido", "dados obrigatorios faltam; plano ou valor diverge da proposta; ha desconto ou excecao; documento ou contrato nao esta pronto; aprovacao vence ou permissao bloqueia"),
    "C7": ("preparar resposta para objecoes comerciais", "objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido; impacto comercial foi mostrado; aprovador esta definido", "objecao envolve preco, desconto ou garantia; lead compara concorrente com promessa sensivel; resposta nao existe na base; risco de promessa indevida aparece; aprovacao vence ou permissao bloqueia"),
    "C8": ("qualificar origem e perfil do lead", "lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida; duplicidade foi verificada; responsavel esta definido", "lead duplicado; origem nao reconhecida; campos obrigatorios faltam; lead ja esta em outra etapa; canal, cota ou permissao bloqueia atualizacao"),
    "C9": ("preparar perda comercial e motivo", "lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido; impacto em relatorio foi calculado; aprovador existe quando perda for sensivel", "perda envolve reclamacao; lead ainda tem acao aberta; motivo e sensivel ou ambiguo; perda afetaria indicacao ou campanha; aprovacao vence ou permissao bloqueia"),
    "C10": ("preparar indicacao e beneficio para aprovacao", "indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado; duplicidade foi verificada; aprovador esta definido", "vinculo nao confere; beneficio foge da regra; indicado ja existe; indicacao envolve conflito comercial; aprovacao vence ou permissao bloqueia"),
    "C11": ("recuperar checkout ou abandono de matricula", "checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido; mensagem aprovada esta disponivel; lead nao pediu parar contato", "pagamento falhou com motivo financeiro; lead pede desconto ou condicao especial; checkout esta expirado; lead responde com reclamacao; canal, cota ou permissao bloqueia contato"),
    "C12": ("tratar demanda sem vaga e lista de interesse", "lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido; regra de promessa esta clara; mensagem nao promete vaga garantida", "lead exige prazo ou garantia; nao ha alternativa compativel; lead e prioridade comercial especial; promessa poderia ser indevida; canal, cota ou permissao bloqueia contato"),
    "C13": ("preparar conversao de interessado em aluno", "interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo; cadastro de aluno pode ser criado; aprovador esta definido", "dados obrigatorios faltam; plano ou valor nao confere; existe duplicidade de aluno; contrato ou pagamento falta; aprovacao vence ou permissao bloqueia"),
    "C14": ("preparar proposta de upsell ou upgrade", "aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado; responsavel comercial esta atribuido; aprovador esta definido", "mudanca impacta financeiro atual; ha desconto ou cortesia; aluno tem pendencia ou reclamacao; proposta foge da regra; aprovacao vence ou permissao bloqueia"),
    "C15": ("capturar lead de multiplos canais e criar ficha unica", "fonte e aceita; lead tem contato identificavel; duplicidade foi verificada; dono do lead esta definido; campos minimos foram preenchidos", "lead duplicado; fonte nao reconhecida; contato incompleto; lead ja pertence a outro responsavel; canal, cota ou permissao bloqueia criacao"),
    "D1": ("enviar lembrete de vencimento", "cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido; template aprovado esta disponivel; limite por cobranca nao foi atingido", "cobranca foi paga ou cancelada; aluno pediu opt-out; valor ou vencimento diverge; mensagem falha; canal, cota ou permissao bloqueia envio"),
    "D2": ("tratar pagamento atrasado e abrir cobranca ou tarefa", "movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel; nao ha disputa registrada", "aluno contesta valor; pedido envolve acordo, desconto ou prazo especial; pagamento pode ter sido feito; provedor apresenta falha; canal, cota ou permissao bloqueia contato"),
    "D3": ("preparar Pix ou link de pagamento para aprovacao", "movimentacao esta identificada; valor esta dentro do limite; template esta aprovado; provedor financeiro esta ok; aprovador esta definido", "valor excede limite; movimentacao esta divergente; aluno pede condicao especial; provedor retorna erro; aprovacao vence ou permissao bloqueia"),
    "D4": ("preparar confirmacao de pagamento para aprovacao", "movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem; responsavel financeiro esta definido; aprovador esta definido", "evidencia esta incompleta; valor nao confere; pagamento duplicado ou suspeito; provedor ainda nao conciliou; aprovacao vence ou permissao bloqueia"),
    "D5": ("preparar renovacao de plano", "plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado; template de renovacao esta aprovado; aprovador esta definido", "aluno tem pendencia financeira; plano mudou de preco ou regra; aluno pediu pausa ou cancelamento; contrato precisa atualizacao; aprovacao vence ou permissao bloqueia"),
    "D6": ("preparar excecao financeira para aprovacao", "tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado; prazo do caso esta definido; aprovador obrigatorio esta definido", "motivo esta incompleto; excecao ultrapassa limite; caso envolve contrato, bloqueio ou reclamacao; impacto em aluno ou turma nao esta claro; aprovacao vence ou permissao bloqueia"),
    "D7": ("tratar falha de pagamento", "falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel; nao ha disputa aberta", "falha persiste apos tentativas; aluno contesta cobranca; provedor retorna erro tecnico; caso exige bloqueio ou liberacao; canal, cota ou permissao bloqueia contato"),
    "D8": ("emitir ou preparar recibo/nota permitida", "pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem; responsavel esta definido; fallback para tarefa existe", "documento nao e permitido; dados fiscais faltam; pagamento nao esta conciliado; aluno pede documento especial; permissao ou provedor bloqueia emissao"),
    "D9": ("preparar pausa ou trancamento para aprovacao", "aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado; prazo esta definido; aprovador esta definido", "pedido afeta credito, contrato ou vencimento; aluno tem pendencia; motivo e sensivel; data solicitada conflita com regra; aprovacao vence ou permissao bloqueia"),
    "D10": ("preparar conciliacao interna para aprovacao", "movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido; impacto foi mostrado; aprovador esta definido", "confianca esta baixa; ha mais de um candidato; valor ou data divergem; provedor esta instavel; aprovacao vence ou permissao bloqueia"),
    "D11": ("preparar contrato ou termos para aprovacao", "template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido; responsavel esta atribuido; aprovador esta definido", "template nao cobre o caso; dados obrigatorios faltam; plano ou valor diverge; aluno pede clausula especial; aprovacao vence ou permissao bloqueia"),
    "D12": ("preparar bloqueio ou liberacao para aprovacao", "aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido; prazo de aprovacao esta definido; aprovador esta definido", "motivo esta incompleto; bloqueio afeta aula ja marcada; liberacao contraria regra financeira; ha reclamacao ou disputa; aprovacao vence ou permissao bloqueia"),
    "D13": ("preparar credito ou cortesia para aprovacao", "aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica; impacto financeiro foi calculado; aprovador esta definido", "valor excede limite; motivo e insuficiente; ha credito duplicado; cortesia afeta contrato ou plano; aprovacao vence ou permissao bloqueia"),
    "D14": ("preparar fechamento mensal financeiro", "periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas; responsavel financeiro esta definido; frequencia do resumo esta configurada", "ha divergencia de conciliacao; movimentacao sem dono; provedor financeiro falhou; pendencia critica apareceu; permissao ou cota bloqueia analise"),
    "D15": ("preparar encerramento ou alteracao efetiva de plano", "plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado; checklist esta completo; aprovador esta definido", "impacto financeiro nao esta claro; aluno tem aulas ou creditos pendentes; contrato precisa revisao; pedido envolve cancelamento sensivel; aprovacao vence ou permissao bloqueia"),
    "E1": ("detectar queda de frequencia e iniciar prevencao", "frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido; cadencia permite contato; nao ha caso sensivel aberto", "queda tem motivo ja registrado; aluno tem reclamacao ou saude/evento pessoal; risco de cancelamento aumentou; cadencia foi excedida; canal, cota ou permissao bloqueia contato"),
    "E2": ("identificar aluno inativo e preparar retomada", "dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido; limite de contato nao foi atingido; mensagem aprovada esta disponivel", "aluno pausou ou trancou; aluno pediu opt-out; ha pendencia financeira ou reclamacao; historico indica caso sensivel; canal, cota ou permissao bloqueia contato"),
    "E3": ("organizar retorno de aluno", "aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido; opcoes de horario existem; mensagem aprovada esta disponivel", "nao ha horario compativel; aluno tem pendencia financeira; retorno exige avaliacao ou cuidado; aluno pede condicao especial; canal, cota ou permissao bloqueia contato"),
    "E4": ("preparar caso de risco de cancelamento para aprovacao", "sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas; contexto foi resumido; aprovador esta definido", "aluno ja pediu cancelamento formal; caso envolve reclamacao ou saude; proposta de retencao exige beneficio; historico e sensivel; aprovacao vence ou permissao bloqueia"),
    "E5": ("preparar reativacao de ex-aluno para aprovacao", "ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada; responsavel esta definido; aprovador esta definido", "ex-aluno pediu opt-out; historico tem reclamacao sensivel; segmento nao permite campanha; beneficio ou condicao especial foi sugerido; aprovacao vence ou permissao bloqueia"),
    "E6": ("acompanhar satisfacao e abrir cuidado quando necessario", "janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido; mensagem aprovada esta disponivel; nao ha reclamacao aberta", "resposta indica reclamacao; nota baixa ou texto sensivel; aluno menciona saude, professor ou cobranca; ja existe caso aberto; canal, cota ou permissao bloqueia contato"),
    "E7": ("preparar retorno apos pausa", "fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem; responsavel esta definido; antecedencia configurada chegou", "aluno pede estender pausa; agenda nao tem vaga; ha pendencia financeira; retorno exige cuidado ou professor especifico; canal, cota ou permissao bloqueia contato"),
    "E8": ("preparar acao de risco por perfil para aprovacao", "segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida; responsavel esta definido; aprovador esta definido", "segmento e sensivel; acao pode parecer invasiva; dados usados nao estao permitidos; aluno tem caso aberto; aprovacao vence ou permissao bloqueia"),
    "E9": ("preparar pos-cancelamento para aprovacao", "cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido; mensagem nao reabre conflito; aprovador esta definido", "cancelamento teve reclamacao; aluno pediu nao ser contatado; motivo envolve saude ou evento pessoal; beneficio de retorno seria oferecido; aprovacao vence ou permissao bloqueia"),
    "E10": ("reconhecer marco de engajamento e acionar contato leve", "marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido; responsavel esta definido; limite de contato nao foi atingido", "aluno tem caso sensivel aberto; marco conflita com baixa frequencia; mensagem poderia soar inadequada; aluno pediu opt-out; canal, cota ou permissao bloqueia contato"),
    "E11": ("preparar caso de saude ou evento pessoal para aprovacao", "evento foi identificado; visibilidade esta definida; dono do caso foi atribuido; nenhum contato automatico sera feito sem revisao; aprovador esta definido", "informacao e sensivel ou incompleta; responsavel adequado nao esta claro; acao proposta pode expor dado privado; aluno pede sigilo; aprovacao vence ou permissao bloqueia"),
    "E12": ("preparar segmentacao de risco para aprovacao", "segmento foi definido; acao permitida foi escolhida; dados usados foram listados; responsavel esta definido; aprovador esta definido", "segmento usa dado sensivel; acao nao esta permitida; alunos afetados sao muitos; risco de contato indevido aparece; aprovacao vence ou permissao bloqueia"),
    "E13": ("preparar recuperacao de reclamacao para aprovacao", "reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas; resumo e proposta foram preparados; aprovador esta definido", "reclamacao envolve professor, saude ou financeiro; aluno esta irritado ou pede cancelamento; proposta exige beneficio; risco reputacional alto; aprovacao vence ou permissao bloqueia"),
    "F1": ("montar prioridades do dia", "fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido; tarefas e aprovacoes foram consolidadas; nada critico impede leitura", "fonte importante falhou; ha incidente critico; dado principal esta desatualizado; responsavel nao esta definido; permissao ou cota bloqueia resumo"),
    "F2": ("identificar dinheiro na mesa e abrir proxima acao", "oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido; acao sugerida nao altera financeiro sozinha; dados financeiros estao disponiveis", "valor esta incerto; caso depende de acordo ou desconto; movimentacao esta em disputa; responsavel nao existe; permissao ou cota bloqueia analise"),
    "F3": ("organizar fila humana e prioridades", "itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada; responsaveis existem; nenhum item exige permissao ausente", "item sem dono; prioridade conflita entre filas; incidente aberto exige pausa; aprovacao vencida acumulou; permissao ou cota bloqueia atualizacao"),
    "F4": ("detectar gargalos operacionais", "metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido; responsavel esta atribuido; acao sugerida e operacional", "dado esta incompleto; gargalo envolve financeiro, grade ou incidente; alerta e critico; responsavel nao definido; permissao ou cota bloqueia analise"),
    "F5": ("gerar resumo semanal", "periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos; dados principais estao atualizados; nenhum incidente impede resumo", "fonte de dados falhou; secoes obrigatorias vazias; destinatario sem permissao; incidente critico em aberto; cota ou permissao bloqueia envio"),
    "F6": ("detectar qualidade de dados e abrir tarefa de correcao", "tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada; responsavel esta definido; correcao automatica nao altera dado sensivel", "correcao pode fundir cadastros; dado envolve historico protegido; conflito nao tem dono claro; volume e alto demais; permissao ou cota bloqueia analise"),
    "F7": ("monitorar creditos, limites e cotas", "uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido; limite comercial foi lido do billing; mensagem interna esta pronta", "cota atingiu limite critico; billing diverge do uso; responsavel nao definido; addon ou upgrade precisa decisao; permissao bloqueia leitura"),
    "F8": ("monitorar performance dos agentes", "metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido; indicadores configurados existem; acao sugerida nao altera politica sozinha", "queda forte de performance; falha ou incidente correlacionado; amostra insuficiente; acao exige mudar fluxo ou politica; permissao ou cota bloqueia analise"),
    "F9": ("preparar revisao de permissoes ou auditoria para aprovacao", "evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido; impacto foi resumido; aprovador esta definido", "evento e critico; mudanca de permissao seria necessaria; ha suspeita de acesso indevido; dados de auditoria incompletos; aprovacao vence ou permissao bloqueia"),
    "F10": ("detectar capacidade e crescimento", "ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido; acao sugerida nao altera grade sozinha; dados de agenda estao atualizados", "capacidade ultrapassa limite; crescimento exige nova turma ou horario; dados de agenda conflitam; impacto financeiro aparece; permissao ou cota bloqueia analise"),
    "F11": ("tratar falhas, webhooks e retries seguros", "falha tecnica foi identificada; severidade esta definida; retry seguro e permitido; responsavel esta atribuido; log tecnico esta disponivel", "retry pode duplicar efeito; falha persiste; severidade e alta; provedor esta indisponivel; permissao ou limite bloqueia mitigacao"),
    "F12": ("preparar importacao ou migracao para aprovacao", "lote foi identificado; amostra foi validada; impacto em dados foi resumido; responsavel esta definido; aprovador esta definido", "duplicidades ou conflitos aparecem; lote e grande demais; campos obrigatorios faltam; rollback nao esta claro; aprovacao vence ou permissao bloqueia"),
    "F13": ("rodar teste de fluxo em simulacao", "cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real; responsavel por revisao esta definido; resultado pode ser salvo", "cenario usa dado real sensivel; teste tenta publicar acao; resultado falha preflight; fluxo tem dependencia indisponivel; permissao ou cota bloqueia teste"),
    "F14": ("tratar incidente de automacao e correcao operacional", "incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo; responsavel esta atribuido; execucao relacionada foi encontrada", "incidente afeta varios fluxos; auto-pausa nao e permitida; correcao exige rollback; falha envolve integracao externa; permissao bloqueia mitigacao"),
    "F15": ("preparar mudanca de politica ou regra operacional", "politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita; comunicacao interna esta pronta; aprovador esta definido", "impacto afeta muitos fluxos; simulacao mostra conflito; vigencia e curta demais; comunicacao nao foi revisada; aprovacao vence ou permissao bloqueia"),
    "G1": ("preparar contexto antes da aula para professor", "aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso; contexto nao inclui dado protegido indevido; professor pode receber o resumo", "aluno tem restricao sensivel; professor sem permissao para dado; historico esta incompleto; aula foi alterada; permissao ou cota bloqueia resumo"),
    "G2": ("lembrar e organizar observacao pos-aula", "aula terminou; professor foi identificado; tipos de nota permitidos estao definidos; lembrete esta dentro do horario; nota ainda nao foi registrada", "professor nao tem permissao; nota envolve restricao ou cuidado; aula nao foi fechada; aluno teve evento sensivel; canal, cota ou permissao bloqueia lembrete"),
    "G3": ("preparar restricao ou cuidado para aprovacao", "aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida; dono do caso esta atribuido; aprovador esta definido", "informacao e sensivel ou incompleta; visibilidade nao esta clara; acao pode expor dado privado; professor ou responsavel diverge; aprovacao vence ou permissao bloqueia"),
    "G4": ("acompanhar objetivo e evolucao do aluno", "aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida; professor ou responsavel esta atribuido; historico permitido esta disponivel", "evolucao envolve saude ou restricao; professor sem permissao; dado historico esta conflitante; acao exige contato sensivel; permissao ou cota bloqueia resumo"),
    "G5": ("preparar contexto permitido para agente", "escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro; aprovador esta definido; nenhum dado protegido sera liberado sem aprovacao", "escopo amplo demais; dados incluem historico protegido; objetivo de uso nao esta claro; politica de privacidade conflita; aprovacao vence ou permissao bloqueia"),
    "G6": ("preparar documentos ou anamnese para aprovacao", "documento exigido foi identificado; aluno foi identificado; responsavel esta definido; visibilidade esta clara; aprovador esta definido", "documento sensivel ou incompleto; anamnese exige revisao humana; arquivo nao e permitido; dados conflitam com historico; aprovacao vence ou permissao bloqueia"),
    "G7": ("preparar correcao de historico para aprovacao", "evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado; impacto da correcao foi mostrado; aprovador esta definido", "motivo esta incompleto; correcao afeta dado protegido; professor ou aluno divergem; evento original nao pode ser localizado; aprovacao vence ou permissao bloqueia"),
    "G8": ("preparar repasse entre professores", "professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados; visibilidade do historico permite repasse; mensagem interna esta pronta", "professor destino sem permissao; resumo inclui dado protegido; aula ou professor mudou; contexto esta incompleto; permissao ou cota bloqueia repasse"),
    "G9": ("enviar lembrete para professor", "professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido; conteudo nao inclui dado protegido indevido; lembrete ainda nao foi enviado", "professor sem canal ou permissao; lembrete duplicado; conteudo depende de dado protegido; aula foi alterada; canal, cota ou permissao bloqueia envio"),
    "G10": ("preparar compartilhamento de contexto", "destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro; preview foi gerado; aprovador esta definido", "destinatario nao tem permissao; dados incluem historico protegido; objetivo e ambiguo; aluno pediu restricao de compartilhamento; aprovacao vence ou permissao bloqueia"),
    "G11": ("preparar permissao de historico", "papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado; responsavel esta atribuido; aprovador esta definido", "escopo amplo demais; papel nao deveria ver dado protegido; conflito com permissao global; evento de auditoria e sensivel; aprovacao vence ou permissao bloqueia"),
    "G12": ("organizar linha do tempo do aluno", "aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido; responsavel esta atribuido; historico pode ser exibido sem dado indevido", "evento protegido aparece; historico conflita ou esta incompleto; usuario nao tem permissao; filtro mostra dado sensivel; permissao ou cota bloqueia exibicao"),
}


def build():
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    missing = [row["id"] for row in rows if row["id"] not in RULES]
    if missing:
        raise SystemExit(f"Missing detailed rules: {missing}")

    fields = [
        "id", "agente", "rotina", "fluxo", "teto", "modo_padrao_pagina",
        "manual_como_funciona", "copiloto_como_funciona", "autonomo_aprovacao_como_funciona",
        "autonomo_excecoes_segue_sozinho_quando", "autonomo_excecoes_chama_equipe_quando",
        "autonomo_conclui_sozinho_quando", "autonomo_para_quando", "se_parar",
        "ajustes_relacionados", "requisitos_readonly",
    ]

    out_rows = []
    for row in rows:
        action, normal_text, exception_text = RULES[row["id"]]
        normal = parts(normal_text)
        exception = parts(exception_text)
        flow = row["fluxo"][:1].lower() + row["fluxo"][1:]
        manual = f"A Taliya cria uma tarefa para {action}; inclui no contexto: {s(normal[:3])}; a equipe executa e registra o resultado."
        copiloto = f"A Taliya sugere {action}; mostra como base: {s(normal[:3])}; a equipe decide se aceita, edita ou descarta."
        aprovacao = (
            f"A Taliya prepara {flow}, valida: {s(normal[:4])}; depois pede aprovacao antes de concluir."
            if allowed(row, "Autonomo com aprovacao")
            else "bloqueado: este modo nao esta habilitado para este fluxo."
        )
        excecoes_ok = s(normal) if allowed(row, "Autonomo com excecoes") else "bloqueado: acima do teto deste fluxo."
        excecoes_handoff = s(exception) if allowed(row, "Autonomo com excecoes") else "bloqueado: acima do teto deste fluxo."
        autonomo_ok = (
            s(normal + ["nenhuma regra exige aprovacao ou chamada humana"])
            if allowed(row, "Autonomo")
            else "bloqueado: acima do teto deste fluxo."
        )
        autonomo_stop = (
            s(exception + ["canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao"])
            if allowed(row, "Autonomo")
            else "bloqueado: acima do teto deste fluxo."
        )
        out_rows.append({
            "id": row["id"],
            "agente": row["agente"],
            "rotina": row["rotina"],
            "fluxo": row["fluxo"],
            "teto": row["teto"],
            "modo_padrao_pagina": row["modo_padrao_pagina"],
            "manual_como_funciona": manual,
            "copiloto_como_funciona": copiloto,
            "autonomo_aprovacao_como_funciona": aprovacao,
            "autonomo_excecoes_segue_sozinho_quando": excecoes_ok,
            "autonomo_excecoes_chama_equipe_quando": excecoes_handoff,
            "autonomo_conclui_sozinho_quando": autonomo_ok,
            "autonomo_para_quando": autonomo_stop,
            "se_parar": row["fallback"],
            "ajustes_relacionados": row["ajustes_do_studio"],
            "requisitos_readonly": row["requisitos_fixos"],
        })

    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    write_review(out_rows)
    write_lifecycle(rows, out_rows)
    print(f"wrote {OUT} rows={len(out_rows)}")
    print(f"wrote {REVIEW_OUT}")
    print(f"wrote {LIFECYCLE_OUT} rows={len(out_rows) * 5}")
    print(f"wrote {LIFECYCLE_REVIEW_OUT}")


def write_review(rows):
    lines = [
        "# Taliya CRM - Revisao Completa Das Regras Por Modo",
        "",
        "Status: documento de revisao v0.1.",
        "Data: 2026-05-22.",
        "",
        "Este documento e a versao legivel da matriz `agents-flows-detailed-mode-rules-matrix.pt-BR.csv`.",
        "Ele existe para revisar os 96 fluxos sem depender de planilha.",
        "",
        "Cada fluxo mostra o que aparece no bloco dinamico `Como funciona neste modo`.",
        "Ajustes do studio continuam limitados ao que realmente muda o comportamento do fluxo.",
        "",
        "## Como Ler",
        "",
        "- `Modo padrao` e o que aparece primeiro na pagina do fluxo.",
        "- `Teto` e o maximo de autonomia permitido para aquele fluxo.",
        "- Modos marcados como `bloqueado` devem aparecer desabilitados na UI.",
        "- `Ajustes relacionados` sao os controles editaveis daquele fluxo.",
        "- `Requisitos readonly` sao checagens fixas/preflight; nao sao configuracoes do studio.",
        "",
    ]

    current_agent = None
    current_routine = None

    for row in rows:
        if row["agente"] != current_agent:
            current_agent = row["agente"]
            current_routine = None
            lines.extend(["", f"## Agente: {current_agent}", ""])

        if row["rotina"] != current_routine:
            current_routine = row["rotina"]
            lines.extend(["", f"### Rotina: {current_routine}", ""])

        lines.extend([
            f"#### {row['fluxo']}",
            "",
            f"- ID interno: `{row['id']}`.",
            f"- Modo padrao: `{row['modo_padrao_pagina']}`.",
            f"- Teto: `{row['teto']}`.",
            "",
            "**Manual**",
            "",
            row["manual_como_funciona"],
            "",
            "**Copiloto**",
            "",
            row["copiloto_como_funciona"],
            "",
            "**Autonomo com aprovacao**",
            "",
            row["autonomo_aprovacao_como_funciona"],
            "",
            "**Autonomo com excecoes**",
            "",
            "Segue sozinho quando:",
            "",
        ])
        write_bullets(lines, row["autonomo_excecoes_segue_sozinho_quando"])
        lines.extend(["", "Chama equipe quando:", ""])
        write_bullets(lines, row["autonomo_excecoes_chama_equipe_quando"])
        lines.extend([
            "",
            "**Autonomo**",
            "",
            "Conclui sozinho quando:",
            "",
        ])
        write_bullets(lines, row["autonomo_conclui_sozinho_quando"])
        lines.extend(["", "Para quando:", ""])
        write_bullets(lines, row["autonomo_para_quando"])
        lines.extend([
            "",
            "**Se parar**",
            "",
            row["se_parar"],
            "",
            "**Ajustes relacionados**",
            "",
        ])
        write_bullets(lines, row["ajustes_relacionados"])
        lines.extend(["", "**Requisitos readonly**", ""])
        write_bullets(lines, row["requisitos_readonly"])
        lines.append("")

    REVIEW_OUT.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def blocked(text):
    return text.startswith("bloqueado:")


def write_lifecycle(source_rows, detail_rows):
    source_by_id = {row["id"]: row for row in source_rows}
    modes = [
        "Manual",
        "Copiloto",
        "Autonomo com aprovacao",
        "Autonomo com excecoes",
        "Autonomo",
    ]
    fields = [
        "id", "agente", "rotina", "fluxo", "modo", "status",
        "inicio", "meio", "fim", "ajustes_afetados", "encadeamento",
    ]
    lifecycle_rows = []

    for row in detail_rows:
        source = source_by_id[row["id"]]
        action, normal_text, exception_text = RULES[row["id"]]
        normal = parts(normal_text)
        exception = parts(exception_text)
        trigger = f"surge um caso para {action}"
        entities = s(normal[:3])
        common_conditions = s(normal[:5])
        exception_conditions = s(exception[:5])
        continuation = source["onde_continua"]
        fallback = row["se_parar"]
        adjustments = row["ajustes_relacionados"]

        for mode in modes:
            status = "habilitado" if allowed(source, mode) else "bloqueado"
            if mode == "Manual":
                inicio = (
                    f"O fluxo comeca quando {trigger}. "
                    f"A Taliya identifica o caso e organiza o contexto principal: {entities}."
                )
                meio = (
                    f"A Taliya cria tarefa, checklist ou caso para a equipe {action}. "
                    f"A decisao e a execucao principal ficam com o humano."
                )
                fim = (
                    f"O fluxo termina quando a equipe registra o resultado. "
                    f"A Taliya salva auditoria e, se nao puder seguir, {fallback}"
                )
            elif mode == "Copiloto":
                inicio = (
                    f"O fluxo comeca quando {trigger}. "
                    f"A Taliya identifica o contexto e mostra a base da sugestao: {entities}."
                )
                meio = (
                    f"A Taliya sugere {action}, prepara texto/resumo/proximo passo e mostra os dados usados. "
                    f"A equipe pode aceitar, editar ou descartar antes de executar."
                )
                fim = (
                    f"Se a equipe aceitar, a acao e registrada conforme a decisao humana. "
                    f"Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em {continuation}."
                )
            elif mode == "Autonomo com aprovacao":
                if not allowed(source, mode):
                    inicio = f"Este modo fica bloqueado para {row['fluxo']}."
                    meio = "A Taliya nao prepara publicacao neste modo porque ele esta acima do teto do fluxo."
                    fim = "O usuario deve escolher um modo permitido para este fluxo."
                else:
                    inicio = (
                        f"O fluxo comeca quando {trigger}. "
                        f"A Taliya identifica o caso, confere {entities} e prepara a revisao."
                    )
                    meio = (
                        f"A Taliya valida {s(normal[:4])} e prepara {action}. "
                        f"Antes de concluir, mostra impacto/preview e pede aprovacao."
                    )
                    fim = (
                        f"Se aprovado, a acao e concluida e auditada. "
                        f"Se recusado, vencido ou incompleto, {fallback}"
                    )
            elif mode == "Autonomo com excecoes":
                if not allowed(source, mode):
                    inicio = f"Este modo fica bloqueado para {row['fluxo']}."
                    meio = "A Taliya nao executa com excecoes porque o teto deste fluxo e menor."
                    fim = "O usuario deve escolher um modo permitido para este fluxo."
                else:
                    inicio = (
                        f"O fluxo comeca quando {trigger}. "
                        f"A Taliya identifica o caso e valida os dados principais: {entities}."
                    )
                    meio = (
                        f"A Taliya executa sozinha quando {common_conditions}. "
                        f"Ela chama a equipe quando {exception_conditions}."
                    )
                    fim = (
                        f"No caso comum, a acao `{action}` fica registrada e auditada. "
                        f"Se houver excecao, {fallback}"
                    )
            else:
                if not allowed(source, mode):
                    inicio = f"Este modo fica bloqueado para {row['fluxo']}."
                    meio = "A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo."
                    fim = "Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados."
                else:
                    inicio = (
                        f"O fluxo comeca quando {trigger}. "
                        f"A Taliya identifica o caso e confirma {entities}."
                    )
                    meio = (
                        f"A Taliya conclui {action} quando {common_conditions}. "
                        f"Ela para quando {exception_conditions}."
                    )
                    fim = (
                        f"A acao e concluida, a auditoria fica salva e a continuidade segue em {continuation}. "
                        f"Se houver bloqueio, {fallback}"
                    )

            lifecycle_rows.append({
                "id": row["id"],
                "agente": row["agente"],
                "rotina": row["rotina"],
                "fluxo": row["fluxo"],
                "modo": mode,
                "status": status,
                "inicio": inicio,
                "meio": meio,
                "fim": fim,
                "ajustes_afetados": adjustments,
                "encadeamento": continuation,
            })

    with LIFECYCLE_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(lifecycle_rows)

    lines = [
        "# Taliya CRM - Revisao Inicio Meio Fim Por Modo",
        "",
        "Status: documento de revisao v0.1.",
        "Data: 2026-05-22.",
        "",
        "Este documento e a versao legivel de `agents-flows-lifecycle-mode-matrix.pt-BR.csv`.",
        "",
        "Cada fluxo aparece com os cinco modos. Modos acima do teto ficam marcados como bloqueados.",
        "",
    ]
    current_agent = None
    current_routine = None
    current_flow = None
    for row in lifecycle_rows:
        if row["agente"] != current_agent:
            current_agent = row["agente"]
            current_routine = None
            current_flow = None
            lines.extend(["", f"## Agente: {current_agent}", ""])
        if row["rotina"] != current_routine:
            current_routine = row["rotina"]
            current_flow = None
            lines.extend(["", f"### Rotina: {current_routine}", ""])
        if row["fluxo"] != current_flow:
            current_flow = row["fluxo"]
            lines.extend(["", f"#### {current_flow}", ""])
        lines.extend([
            f"**{row['modo']}** ({row['status']})",
            "",
            f"- Inicio: {row['inicio']}",
            f"- Meio: {row['meio']}",
            f"- Fim: {row['fim']}",
            f"- Ajustes afetados: {row['ajustes_afetados']}",
            f"- Encadeamento: {row['encadeamento']}",
            "",
        ])

    LIFECYCLE_REVIEW_OUT.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
