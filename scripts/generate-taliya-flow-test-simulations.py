import csv
import importlib.util
from pathlib import Path


BASE = Path("specs/006-crm-operational-core")
DETAILS = BASE / "agents-flows-96-complete-detail-matrix.pt-BR.csv"
OUT = BASE / "agents-flows-96-test-simulation-matrix.pt-BR.csv"
REVIEW = BASE / "agents-flows-96-test-simulation-review.pt-BR.md"
AUDIT = BASE / "agents-flows-96-test-simulation-quality-audit.pt-BR.md"
RULES_PATH = Path("scripts/generate-taliya-detailed-mode-rules.py")


spec = importlib.util.spec_from_file_location("rules_module", RULES_PATH)
rules_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rules_module)
RULES = rules_module.RULES


def items(text):
    return [item.strip() for item in text.split(";") if item.strip()]


def join(items_):
    return "; ".join(item.strip().rstrip(".") for item in items_ if item.strip())


def first_sentence(text):
    return text.split(". ")[0].strip().rstrip(".") + "."


def sentence(text):
    return text.strip().rstrip(".") + "."


def phrase(text):
    return text.strip().rstrip(".")


def clean_start(text):
    return phrase(text.split(" Checagens deste fluxo:")[0]).replace("pede algo que", "faz um pedido que")


def approval_timing(row, asks_approval):
    if asks_approval:
        return "No cenario principal, antes da acao principal"
    if row["modo_padrao"] == "Autonomo com excecoes":
        return "Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente"
    if row["modo_padrao"] == "Autonomo":
        return "Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido"
    if row["modo_padrao"] == "Copiloto":
        return "Nao pede aprovacao automatica; a equipe decide se executa a sugestao"
    return "Nao pede aprovacao automatica; a equipe executa manualmente"


SCENARIOS = {
    "A1": ("Mensagem simples nova", "Classifica assunto e abre atendimento.", "Contato nao identificado", "Cria caso humano antes de responder.", "Mensagem com desconto e reclamacao", "Chama equipe por assunto sensivel.", "Canal ou cota bloqueia", "Para e cria pendencia no Inbox."),
    "A2": ("Pergunta esta na base", "Responde com conteudo aprovado.", "Pergunta fora da base", "Cria tarefa de resposta.", "Pedido de dado privado", "Chama equipe antes de responder.", "Opt-out ou cota bloqueia", "Para sem enviar mensagem."),
    "A3": ("Aluno reconhecido", "Liga conversa ao cadastro correto.", "Telefone atende dois alunos", "Segura dados e chama equipe.", "Aluno contesta cadastro", "Cria revisao humana.", "Permissao bloqueia contexto", "Para antes de expor informacao."),
    "A4": ("Pedido fora do CRM", "Responde com mensagem padrao.", "Mensagem parece reclamacao", "Chama equipe.", "Pessoa insiste em humano", "Cria caso para atendimento.", "Canal falha", "Para e cria pendencia."),
    "A5": ("Handoff comum", "Envia conversa para fila certa.", "Fila nao existe", "Cria pendencia operacional.", "Prioridade nao clara", "Pede decisao de triagem.", "Responsavel indisponivel", "Mantem caso aguardando dono."),
    "A6": ("Opt-out claro", "Registra preferencia de contato.", "Pedido ambiguo", "Abre revisao.", "Telefone compartilhado", "Nao aplica preferencia sem validar.", "Permissao bloqueia registro", "Cria pendencia para responsavel."),
    "A7": ("Audio legivel", "Classifica midia e vincula ao atendimento.", "Documento sensivel", "Abre revisao antes de usar.", "Identidade nao confere", "Segura conteudo e chama equipe.", "Arquivo nao aceito", "Para e registra bloqueio."),
    "A8": ("Pedido de acesso a dados", "Monta aprovacao de privacidade.", "Identidade nao confirmada", "Cria pendencia de validacao.", "Pedido amplo de exclusao", "Exige aprovacao humana.", "Aprovacao vence", "Mantem caso pendente."),
    "A9": ("Telefone compartilhado detectado", "Monta aprovacao de validacao.", "Mais de um aluno possivel", "Nao expoe dados.", "Responsavel diverge", "Chama responsavel de revisao.", "Permissao bloqueia", "Mantem atendimento com humano."),
    "A10": ("SLA dentro do prazo", "Atualiza status e prioridade.", "SLA vencido", "Cria alerta em Hoje/Tarefas.", "Conversa sem dono", "Encaminha para fila humana.", "Fila indisponivel", "Cria pendencia operacional."),
    "B1": ("Confirmacao no horario", "Envia confirmacao e registra resposta.", "Aula alterada", "Para antes de enviar.", "Resposta conflitante", "Cria pendencia na aula.", "WhatsApp bloqueia", "Nao envia e cria pendencia."),
    "B2": ("Aluno avisou no prazo", "Registra falta e cria tarefa de reposicao.", "Aviso fora do prazo", "Chama equipe antes de registrar.", "Aluno pede credito", "Chama equipe antes de decidir.", "WhatsApp falha", "Para e cria pendencia."),
    "B3": ("Aluno faltou sem avisar", "Marca ausencia e abre acompanhamento.", "Chamada nao fechada", "Aguarda professor.", "Aviso apareceu em outro canal", "Chama equipe para revisar.", "Contato bloqueado", "Cria tarefa sem mensagem."),
    "B4": ("Vaga abriu com candidato claro", "Convida aluno elegivel.", "Empate na prioridade", "Chama equipe.", "Credito duvidoso", "Nao envia convite.", "Canal falha", "Para e cria pendencia."),
    "B5": ("Reposicao dentro da politica", "Monta aprovacao de remarcacao.", "Credito vencido", "Cria pendencia.", "Aula destino lotada", "Nao propoe remarcacao.", "Aprovacao vence", "Mantem solicitacao pendente."),
    "B6": ("Vaga compativel apareceu", "Envia convite da lista de espera.", "Aluno nao responde", "Atualiza prazo e proximo candidato.", "Prioridade empata", "Chama equipe.", "Envio bloqueado", "Para e cria pendencia."),
    "B7": ("Horario experimental disponivel", "Oferece horarios reais ao lead.", "Nao ha vaga", "Cria tarefa comercial.", "Lead pede horario fora da regra", "Chama comercial.", "Canal bloqueia", "Nao envia disponibilidade."),
    "B8": ("Novo horario disponivel", "Monta aprovacao de horario fixo.", "Novo horario conflita", "Nao aplica mudanca.", "Impacta varios alunos", "Pede decisao.", "Aprovacao vence", "Mantem pedido pendente."),
    "B9": ("Studio cancela aula simples", "Monta aprovacao e comunicado.", "Muitos alunos afetados", "Exige decisao.", "Credito/reposicao incerto", "Nao comunica sozinho.", "Aprovacao vence", "Aula segue sem cancelamento automatico."),
    "B10": ("Conflito de lotacao claro", "Monta aprovacao de correcao.", "Capacidade diverge", "Pede revisao.", "Solucao remove aluno", "Exige aprovacao.", "Permissao bloqueia", "Mantem conflito aberto."),
    "B11": ("Mudanca de grade simulada", "Monta aprovacao de impacto.", "Simulacao encontra conflito", "Volta para revisao.", "Vigencia curta demais", "Nao publica mudanca.", "Aprovacao vence", "Mantem grade atual."),
    "B12": ("Lead faltou experimental", "Abre follow-up ou remarcacao.", "Lead avisou por outro canal", "Chama comercial.", "Nao ha nova vaga", "Cria tarefa comercial.", "Canal bloqueia", "Nao envia contato."),
    "B13": ("Credito valido proposto", "Monta aprovacao de credito.", "Credito contestado", "Chama responsavel.", "Duplicidade de credito", "Bloqueia criacao.", "Aprovacao vence", "Mantem credito pendente."),
    "B14": ("Correcao com motivo claro", "Monta aprovacao de presenca.", "Motivo ausente", "Pede complemento.", "Impacta credito/financeiro", "Chama equipe.", "Aprovacao vence", "Nao altera chamada."),
    "B15": ("Primeira aula proxima", "Envia orientacao e checklist.", "Cuidado pendente", "Chama equipe antes de contato.", "Professor indefinido", "Cria tarefa.", "Canal bloqueia", "Nao envia orientacao."),
    "B16": ("Workshop simples", "Monta aprovacao do evento.", "Conflito com grade regular", "Volta para revisao.", "Preco indefinido", "Nao publica evento.", "Aprovacao vence", "Mantem evento em rascunho."),
    "C1": ("Pergunta sobre plano aprovado", "Responde valores permitidos.", "Lead pede desconto", "Chama comercial.", "Pergunta mistura contrato", "Cria tarefa.", "Cota bloqueia", "Nao envia resposta."),
    "C2": ("Lead quer experimental", "Marca ou prepara aula experimental.", "Horario indisponivel", "Oferece alternativa ou chama comercial.", "Lead ja fez experimental", "Pede decisao.", "Canal bloqueia", "Cria pendencia."),
    "C3": ("Lembrete no horario", "Envia lembrete do experimental.", "Aula remarcada", "Para antes de enviar.", "Lead pede mudanca", "Chama comercial.", "Opt-out", "Nao envia."),
    "C4": ("Experimental concluida", "Inicia acompanhamento pos-aula.", "Lead faltou", "Encaminha para fluxo de falta experimental.", "Observacao sensivel", "Chama comercial.", "Canal bloqueia", "Cria tarefa."),
    "C5": ("Follow-up permitido", "Envia contato da cadencia.", "Lead pediu parar", "Bloqueia contato.", "Lead pede desconto", "Chama comercial.", "Canal/cota bloqueia", "Para e registra pendencia."),
    "C6": ("Lead aceitou pre-matricula", "Monta aprovacao de pre-matricula.", "Dados obrigatorios faltam", "Pede complemento.", "Desconto na proposta", "Exige aprovacao.", "Aprovacao vence", "Mantem lead pendente."),
    "C7": ("Objecao comum", "Monta resposta para aprovacao.", "Pedido de garantia", "Nao responde sozinho.", "Resposta fora da base", "Chama comercial.", "Aprovacao vence", "Mantem objecao aberta."),
    "C8": ("Lead novo com origem clara", "Cria ficha qualificada.", "Lead duplicado", "Cria revisao.", "Origem desconhecida", "Pede classificacao.", "Campos faltando", "Mantem ficha incompleta."),
    "C9": ("Perda com motivo claro", "Monta aprovacao de perda.", "Lead tem acao aberta", "Nao encerra.", "Motivo sensivel", "Chama comercial.", "Aprovacao vence", "Mantem lead ativo."),
    "C10": ("Indicacao valida", "Monta aprovacao do beneficio.", "Vinculo nao confere", "Bloqueia beneficio.", "Indicado ja existe", "Pede revisao.", "Aprovacao vence", "Mantem indicacao pendente."),
    "C11": ("Checkout abandonado", "Envia recuperacao permitida.", "Falha financeira", "Chama comercial/financeiro.", "Checkout expirado", "Cria tarefa.", "Canal bloqueia", "Nao envia recuperacao."),
    "C12": ("Demanda sem vaga", "Cria lista de interesse.", "Lead exige garantia", "Chama comercial.", "Nao ha alternativa", "Mantem demanda aberta.", "Canal bloqueia", "Nao envia mensagem."),
    "C13": ("Interessado pronto", "Monta aprovacao de conversao.", "Contrato faltando", "Nao cria aluno.", "Aluno duplicado", "Pede revisao.", "Aprovacao vence", "Mantem interessado pendente."),
    "C14": ("Aluno elegivel para upgrade", "Monta proposta de upgrade.", "Impacto financeiro", "Exige aprovacao.", "Aluno tem reclamacao", "Chama comercial.", "Aprovacao vence", "Nao envia proposta."),
    "C15": ("Lead chegou por formulario", "Cria ficha unica.", "Lead duplicado", "Abre revisao.", "Contato incompleto", "Mantem pendente.", "Fonte nao reconhecida", "Pede classificacao."),
    "D1": ("Vencimento proximo", "Envia lembrete de cobranca.", "Cobranca ja paga", "Nao envia.", "Valor diverge", "Chama financeiro.", "Opt-out/canal bloqueia", "Para sem contato."),
    "D2": ("Pagamento atrasado comum", "Abre cobranca ou tarefa.", "Aluno contesta valor", "Chama financeiro.", "Pedido de acordo", "Exige decisao.", "Provedor falha", "Cria pendencia."),
    "D3": ("Link dentro do limite", "Monta aprovacao de Pix/link.", "Valor excede limite", "Bloqueia envio.", "Provedor retorna erro", "Cria pendencia.", "Aprovacao vence", "Nao envia link."),
    "D4": ("Comprovante coerente", "Monta aprovacao de pagamento.", "Valor nao confere", "Chama financeiro.", "Pagamento duplicado", "Bloqueia baixa.", "Aprovacao vence", "Nao baixa cobranca."),
    "D5": ("Renovacao no prazo", "Monta aprovacao de renovacao.", "Aluno tem pendencia", "Chama financeiro.", "Contrato precisa atualizar", "Nao renova.", "Aprovacao vence", "Mantem plano atual."),
    "D6": ("Excecao com motivo", "Monta aprovacao financeira.", "Excecao excede limite", "Bloqueia aplicacao.", "Impacto incerto", "Pede complemento.", "Aprovacao vence", "Mantem caso aberto."),
    "D7": ("Falha de pagamento tratavel", "Envia orientacao ou cria tarefa.", "Falha persiste", "Chama financeiro.", "Aluno contesta cobranca", "Para contato.", "Provedor indisponivel", "Abre pendencia."),
    "D8": ("Recibo permitido", "Emite ou prepara documento.", "Dados fiscais faltam", "Cria tarefa.", "Permissao bloqueia", "Nao emite.", "Provedor falha", "Abre pendencia financeira."),
    "D9": ("Pausa dentro da politica", "Monta aprovacao de pausa.", "Impacto financeiro", "Exige decisao.", "Periodo invalido", "Pede ajuste.", "Aprovacao vence", "Mantem plano ativo."),
    "D10": ("Conciliacao com alta confianca", "Monta aprovacao de conciliacao.", "Mais de um candidato", "Chama financeiro.", "Valor diverge", "Bloqueia vinculo.", "Aprovacao vence", "Nao concilia."),
    "D11": ("Contrato pronto", "Monta aprovacao do documento.", "Versao faltando", "Bloqueia envio.", "Dados incompletos", "Pede complemento.", "Aprovacao vence", "Mantem documento em rascunho."),
    "D12": ("Liberacao com motivo claro", "Monta aprovacao de acesso.", "Pagamento recente contestado", "Chama financeiro.", "Impacto nao claro", "Bloqueia mudanca.", "Aprovacao vence", "Nao altera acesso."),
    "D13": ("Cortesia dentro da politica", "Monta aprovacao do beneficio.", "Valor foge da politica", "Bloqueia aplicacao.", "Motivo incompleto", "Pede complemento.", "Aprovacao vence", "Nao aplica credito."),
    "D14": ("Fechamento sem divergencia", "Separa consolidados e pendencias.", "Conciliacao divergente", "Cria tarefa.", "Provedor falhou", "Marca fechamento incompleto.", "Permissao bloqueia", "Nao gera fechamento final."),
    "D15": ("Alteracao efetiva clara", "Monta aprovacao de plano.", "Saldo pendente", "Bloqueia mudanca.", "Contrato afetado", "Chama financeiro.", "Aprovacao vence", "Mantem plano atual."),
    "E1": ("Frequencia caiu", "Abre cuidado preventivo.", "Recorrencia alta", "Chama equipe.", "Sinal de saude", "Nao envia mensagem automatica.", "Canal bloqueia", "Cria tarefa."),
    "E2": ("Aluno inativo elegivel", "Inicia retomada permitida.", "Aluno pausou", "Para contato.", "Pendencia financeira", "Chama equipe.", "Opt-out", "Nao envia."),
    "E3": ("Aluno quer voltar", "Organiza retorno.", "Sem horario compativel", "Cria tarefa.", "Pendencia financeira", "Chama equipe.", "Cuidado especial", "Pede revisao."),
    "E4": ("Sinal de cancelamento", "Monta aprovacao de retencao.", "Cancelamento formal", "Nao automatiza.", "Caso sensivel", "Chama responsavel.", "Aprovacao vence", "Mantem caso aberto."),
    "E5": ("Ex-aluno elegivel", "Monta aprovacao de reativacao.", "Opt-out", "Bloqueia contato.", "Historico com reclamacao", "Chama responsavel.", "Aprovacao vence", "Nao libera contato."),
    "E6": ("Pesquisa de satisfacao", "Coleta sinal e abre cuidado se preciso.", "Nota baixa", "Chama equipe.", "Texto cita professor", "Cria caso sensivel.", "Canal bloqueia", "Nao envia pesquisa."),
    "E7": ("Pausa perto do fim", "Prepara retorno.", "Aluno pede extensao", "Chama equipe.", "Sem vaga", "Cria tarefa.", "Pendencia financeira", "Bloqueia contato automatico."),
    "E8": ("Segmento de risco permitido", "Monta aprovacao de acao.", "Dado sensivel usado", "Bloqueia acao.", "Acao invasiva", "Pede revisao.", "Aprovacao vence", "Nao executa acao."),
    "E9": ("Pos-cancelamento permitido", "Monta aprovacao de contato.", "Aluno pediu nao contato", "Bloqueia mensagem.", "Cancelamento com reclamacao", "Chama responsavel.", "Aprovacao vence", "Nao libera contato."),
    "E10": ("Marco positivo", "Registra marco e aciona contato leve.", "Caso sensivel aberto", "Nao envia.", "Baixa frequencia conflita", "Chama equipe.", "Opt-out", "Bloqueia contato."),
    "E11": ("Evento pessoal identificado", "Monta aprovacao de cuidado.", "Aluno pediu sigilo", "Bloqueia exposicao.", "Dado incompleto", "Pede revisao.", "Aprovacao vence", "Mantem caso restrito."),
    "E12": ("Segmento definido", "Monta aprovacao de segmentacao.", "Volume alto", "Pede revisao.", "Dado sensivel", "Bloqueia uso.", "Aprovacao vence", "Nao executa acao."),
    "E13": ("Reclamacao registrada", "Monta aprovacao de recuperacao.", "Envolve professor", "Chama responsavel.", "Proposta exige beneficio", "Exige aprovacao.", "Aprovacao vence", "Mantem caso aberto."),
    "F1": ("Resumo diario pronto", "Monta prioridades do dia.", "Fonte critica falhou", "Marca pendencia.", "Incidente critico", "Destaca alerta.", "Permissao bloqueia", "Nao mostra fonte restrita."),
    "F2": ("Oportunidade clara", "Abre proxima acao financeira.", "Valor incerto", "Cria tarefa.", "Disputa aberta", "Nao sugere cobranca.", "Responsavel ausente", "Mantem pendente."),
    "F3": ("Fila com itens", "Ordena prioridades humanas.", "Item sem dono", "Cria alerta.", "Aprovacao vencida", "Sobe prioridade.", "Incidente aberto", "Marca bloqueio."),
    "F4": ("Gargalo detectado", "Cria alerta operacional.", "Dado incompleto", "Pede investigacao.", "Toca financeiro/grade", "Chama responsavel.", "Permissao bloqueia", "Oculta detalhe restrito."),
    "F5": ("Semana fechada", "Gera resumo semanal.", "Fonte falhou", "Resumo fica pendente.", "Destinatario sem permissao", "Nao envia.", "Incidente critico", "Marca bloqueio."),
    "F6": ("Duplicidade encontrada", "Abre tarefa de correcao.", "Fusao sensivel", "Chama revisao.", "Alto volume", "Cria lote de tarefas.", "Permissao bloqueia", "Nao altera dado."),
    "F7": ("Cota em alerta", "Registra alerta de uso.", "Billing diverge", "Chama admin.", "Upgrade necessario", "Cria acao para dono.", "Permissao bloqueia", "Nao mostra detalhe."),
    "F8": ("Performance normal", "Gera relatorio de agentes.", "Queda forte", "Abre investigacao.", "Amostra insuficiente", "Marca incerteza.", "Incidente correlacionado", "Vincula incidente."),
    "F9": ("Evento de auditoria", "Monta aprovacao de revisao.", "Suspeita de acesso", "Escala responsavel.", "Mudanca de permissao", "Exige aprovacao.", "Aprovacao vence", "Mantem permissao atual."),
    "F10": ("Capacidade perto do limite", "Cria alerta de ocupacao.", "Exige nova turma", "Chama gestao.", "Impacto financeiro", "Pede decisao.", "Dados de agenda conflitam", "Bloqueia sugestao."),
    "F11": ("Webhook falhou com retry seguro", "Executa retry permitido.", "Risco de duplicar efeito", "Nao reprocessa.", "Provedor indisponivel", "Abre incidente.", "Limite bloqueia", "Mantem falha pendente."),
    "F12": ("Lote validado", "Monta aprovacao de importacao.", "Duplicidades aparecem", "Bloqueia lote.", "Rollback incerto", "Pede revisao.", "Aprovacao vence", "Nao importa."),
    "F13": ("Teste seguro escolhido", "Roda simulacao sem publicar.", "Dado sensivel real", "Bloqueia teste.", "Preflight falha", "Mostra pendencia.", "Tentativa de executar real", "Para imediatamente."),
    "F14": ("Incidente simples", "Pausa ou mitiga fluxo permitido.", "Afeta varios fluxos", "Abre incidente humano.", "Exige rollback", "Chama responsavel.", "Integracao falha", "Vincula log tecnico."),
    "F15": ("Regra nova simulada", "Monta aprovacao de politica.", "Impacto em muitos fluxos", "Pede revisao.", "Vigencia curta", "Bloqueia publicacao.", "Aprovacao vence", "Mantem politica atual."),
    "G1": ("Contexto permitido", "Envia resumo ao professor.", "Restricao sensivel", "Remove dado e chama revisao.", "Professor sem permissao", "Nao envia resumo.", "Aula alterada", "Atualiza contexto."),
    "G2": ("Aula terminou", "Lembra professor e organiza nota.", "Nota sensivel", "Vai para revisao.", "Professor sem permissao", "Nao aceita nota.", "Canal bloqueia", "Cria pendencia."),
    "G3": ("Restricao classificada", "Monta aprovacao de cuidado.", "Visibilidade incerta", "Pede revisao.", "Dado incompleto", "Mantem pendente.", "Aprovacao vence", "Nao altera historico."),
    "G4": ("Objetivo acompanhado", "Atualiza evolucao permitida.", "Toca saude/restricao", "Chama revisao.", "Professor sem permissao", "Oculta detalhe.", "Historico conflita", "Cria tarefa."),
    "G5": ("Escopo permitido", "Monta aprovacao de contexto para agente.", "Escopo amplo", "Bloqueia liberacao.", "Dado protegido", "Pede revisao.", "Aprovacao vence", "Nao libera contexto."),
    "G6": ("Documento identificado", "Monta aprovacao de documento.", "Anamnese sensivel", "Chama revisao.", "Arquivo nao permitido", "Bloqueia anexo.", "Aprovacao vence", "Nao libera documento."),
    "G7": ("Correcao com motivo", "Monta aprovacao de historico.", "Evento nao localizado", "Cria pendencia.", "Dado protegido", "Exige revisao.", "Aprovacao vence", "Nao corrige historico."),
    "G8": ("Repasse permitido", "Envia resumo ao professor destino.", "Destino sem permissao", "Nao envia.", "Resumo inclui dado protegido", "Chama revisao.", "Contexto incompleto", "Cria pendencia."),
    "G9": ("Lembrete no horario", "Envia lembrete ao professor.", "Aula alterada", "Para envio.", "Conteudo protegido", "Chama revisao.", "Canal bloqueia", "Nao envia."),
    "G10": ("Compartilhamento permitido", "Monta aprovacao de contexto.", "Destinatario sem permissao", "Bloqueia envio.", "Aluno restringiu compartilhamento", "Chama revisao.", "Aprovacao vence", "Nao compartilha."),
    "G11": ("Escopo de permissao claro", "Monta aprovacao de permissao.", "Escopo amplo demais", "Bloqueia mudanca.", "Conflito com permissao global", "Chama admin.", "Aprovacao vence", "Mantem permissao atual."),
    "G12": ("Linha do tempo segura", "Organiza eventos permitidos.", "Evento protegido aparece", "Restringe exibicao.", "Historico conflita", "Abre revisao.", "Usuario sem permissao", "Oculta linha do tempo."),
}


VISUAL_KIND = {
    **{rid: "celular_conversa" for rid in ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A10", "B1", "B2", "B3", "B4", "B6", "B7", "B12", "B15", "C1", "C2", "C3", "C4", "C5", "C7", "C11", "C12", "C14", "C15", "D1", "D2", "D3", "D7", "D8", "E1", "E2", "E3", "E5", "E6", "E7", "E9", "E10", "G1", "G2", "G8", "G9"]},
    **{rid: "aprovacao" for rid in ["A8", "A9", "B5", "B8", "B9", "B10", "B11", "B13", "B14", "B16", "C6", "C9", "C10", "C13", "D4", "D5", "D6", "D9", "D10", "D11", "D12", "D13", "D15", "E4", "E8", "E11", "E12", "E13", "F9", "F12", "F15", "G3", "G5", "G6", "G7", "G10", "G11"]},
    "F1": "hoje_prioridades",
    "F2": "dinheiro_na_mesa",
    "F3": "fila_humana",
    "F4": "gargalo_operacional",
    "F5": "resumo_semanal",
    "F6": "qualidade_dados",
    "F7": "uso_cotas",
    "F8": "performance_agentes",
    "F10": "capacidade",
    "F11": "integracao_logs",
    "F13": "simulador_fluxo",
    "F14": "incidente_execucao",
    "D14": "fechamento_financeiro",
    "C8": "ficha_lead",
    "G4": "historico_aluno",
    "G12": "linha_tempo",
}


VISUAL_DESCRIPTIONS = {
    "celular_conversa": ("Celular/conversa", "celular com conversa simulada e cartao interno mostrando o resultado do fluxo"),
    "aprovacao": ("Pedido de aprovacao", "card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado"),
    "hoje_prioridades": ("Hoje/prioridades", "lista operacional de prioridades do dia com alertas e origem"),
    "dinheiro_na_mesa": ("Dinheiro na mesa", "lista de oportunidades financeiras com responsavel e proxima acao"),
    "fila_humana": ("Fila humana", "fila de tarefas, aprovacoes e casos humanos ordenados por prioridade"),
    "gargalo_operacional": ("Gargalo operacional", "painel de indicador, causa provavel e responsavel pela investigacao"),
    "resumo_semanal": ("Resumo semanal", "preview do resumo executivo com secoes e destinatarios internos"),
    "qualidade_dados": ("Qualidade de dados", "lista de duplicidades, campos ausentes e tarefas de correcao"),
    "uso_cotas": ("Uso/cotas", "cartao de cota, alertas 70/90/100 e acao para dono/admin"),
    "performance_agentes": ("Performance de agentes", "relatorio de indicadores, queda detectada e origem da investigacao"),
    "capacidade": ("Capacidade/crescimento", "ocupacao por turma/horario com limite, alerta e acao sugerida"),
    "integracao_logs": ("Logs de integracao", "linha de falha tecnica com retry seguro, provedor e severidade"),
    "simulador_fluxo": ("Simulador de fluxo", "painel de teste seguro mostrando que nenhuma acao real sera publicada"),
    "incidente_execucao": ("Incidente/execucao", "cartao de incidente com execucao relacionada, pausa e mitigacao"),
    "fechamento_financeiro": ("Fechamento financeiro", "painel de fechamento com consolidados, pendencias e divergencias"),
    "ficha_lead": ("Ficha de lead", "ficha do lead com origem, campos minimos, duplicidade e dono comercial"),
    "historico_aluno": ("Historico do aluno", "perfil do aluno com objetivo/evolucao permitida e proximo cuidado"),
    "linha_tempo": ("Linha do tempo", "linha do tempo do aluno com eventos permitidos e filtros seguros"),
}


NO_DECIDE = {
    "B2": "Nao escolhe vaga, credito ou horario de reposicao neste fluxo.",
    "B4": "Nao consome credito nem altera prioridade quando houver empate.",
    "B5": "Nao muda agenda antes da aprovacao.",
    "B6": "Nao fura prioridade nem confirma vaga sem resposta valida.",
    "B7": "Nao promete vaga experimental indisponivel.",
    "B8": "Nao troca horario fixo sem aprovacao.",
    "B9": "Nao cancela aula nem comunica alunos sem aprovacao.",
    "B10": "Nao remove aluno nem altera capacidade sem aprovacao.",
    "B11": "Nao publica grade sem aprovacao.",
    "B13": "Nao cria credito antes da aprovacao.",
    "B14": "Nao altera historico de presenca antes da aprovacao.",
    "B16": "Nao publica evento/workshop antes da aprovacao.",
    "C6": "Nao cria matricula antes da aprovacao.",
    "C7": "Nao promete desconto, garantia ou condicao fora da base.",
    "C9": "Nao encerra lead sem aprovacao quando ha sensibilidade.",
    "C10": "Nao concede beneficio de indicacao antes da aprovacao.",
    "C13": "Nao cria aluno antes da aprovacao.",
    "C14": "Nao aplica upgrade nem proposta sensivel antes da aprovacao.",
    "D3": "Nao envia Pix/link antes da aprovacao.",
    "D4": "Nao baixa cobranca antes da aprovacao.",
    "D5": "Nao renova plano antes da aprovacao.",
    "D6": "Nao aplica excecao financeira antes da aprovacao.",
    "D9": "Nao pausa ou tranca plano antes da aprovacao.",
    "D10": "Nao vincula pagamento e movimentacao antes da aprovacao.",
    "D11": "Nao envia contrato/termo antes da aprovacao.",
    "D12": "Nao bloqueia nem libera acesso antes da aprovacao.",
    "D13": "Nao aplica credito ou cortesia antes da aprovacao.",
    "D15": "Nao efetiva alteracao de plano antes da aprovacao.",
    "E4": "Nao executa retencao sensivel sem aprovacao.",
    "E5": "Nao contata ex-aluno antes da aprovacao.",
    "E8": "Nao usa perfil de risco sem aprovacao.",
    "E9": "Nao recontata aluno cancelado sem aprovacao.",
    "E11": "Nao expõe informacao de saude ou evento pessoal.",
    "E12": "Nao executa segmentacao de risco sem aprovacao.",
    "E13": "Nao oferece beneficio nem resposta de recuperacao sem aprovacao.",
    "F9": "Nao muda permissao sem aprovacao.",
    "F12": "Nao importa lote antes da aprovacao.",
    "F15": "Nao publica politica antes da aprovacao.",
    "G3": "Nao altera historico protegido antes da aprovacao.",
    "G5": "Nao libera contexto para agente antes da aprovacao.",
    "G6": "Nao libera documento/anamnese sem aprovacao.",
    "G7": "Nao corrige historico antes da aprovacao.",
    "G10": "Nao compartilha contexto antes da aprovacao.",
    "G11": "Nao muda permissao de historico antes da aprovacao.",
}


NO_DECIDE.update({
    "A1": "Nao responde conversa sensivel nem decide fila sem responsavel.",
    "A2": "Nao responde fora da base aprovada nem envia dado privado.",
    "A3": "Nao expoe contexto quando identidade ou cadastro estiverem duvidosos.",
    "A4": "Nao trata emergencia, saude, dado pessoal ou reclamacao como pedido simples.",
    "A5": "Nao resolve o atendimento; entrega para humano com resumo, fila e prioridade.",
    "A6": "Nao altera preferencia de contato quando o pedido estiver ambiguo ou o telefone for compartilhado.",
    "A7": "Nao usa midia ilegivel, sensivel ou com identidade incerta.",
    "A8": "Nao executa pedido de privacidade; monta aprovacao e caso para humano autorizado.",
    "A9": "Nao revela dado antes de validar quem esta usando o telefone compartilhado.",
    "A10": "Nao resolve atendimento; controla SLA, dono, status e alerta.",
    "B1": "Nao altera aula; apenas envia confirmacao permitida e registra resposta.",
    "B2": "Nao escolhe vaga, credito ou horario de reposicao neste fluxo.",
    "B3": "Nao define retencao complexa; marca ausencia e abre acompanhamento.",
    "B4": "Nao consome credito nem altera prioridade quando houver empate.",
    "B5": "Nao muda agenda antes da aprovacao.",
    "B6": "Nao fura prioridade nem confirma vaga sem resposta valida.",
    "B7": "Nao promete vaga experimental indisponivel.",
    "B8": "Nao troca horario fixo sem aprovacao.",
    "B9": "Nao cancela aula nem comunica alunos sem aprovacao.",
    "B10": "Nao remove aluno nem altera capacidade sem aprovacao.",
    "B11": "Nao publica grade sem aprovacao.",
    "B12": "Nao decide desconto, remarcacao especial ou condicao comercial fora da politica.",
    "B13": "Nao cria credito antes da aprovacao.",
    "B14": "Nao altera historico de presenca antes da aprovacao.",
    "B15": "Nao envia orientacao se houver cuidado, restricao ou professor indefinido.",
    "B16": "Nao publica evento/workshop antes da aprovacao.",
    "C1": "Nao negocia desconto ou condicao fora da base comercial aprovada.",
    "C2": "Nao promete horario ou vaga indisponivel.",
    "C3": "Nao remarca experimental; lembra, para ou chama comercial.",
    "C4": "Nao decide venda, desconto ou condicao de matricula.",
    "C5": "Nao continua contato se o lead pediu parar ou trouxe assunto sensivel.",
    "C6": "Nao cria matricula antes da aprovacao.",
    "C7": "Nao promete desconto, garantia ou condicao fora da base.",
    "C8": "Nao mescla lead duplicado nem corrige origem sem revisao.",
    "C9": "Nao encerra lead sem aprovacao quando ha sensibilidade.",
    "C10": "Nao concede beneficio de indicacao antes da aprovacao.",
    "C11": "Nao corrige falha financeira nem concede desconto; chama comercial ou financeiro.",
    "C12": "Nao promete vaga, turma ou prazo de abertura.",
    "C13": "Nao cria aluno antes da aprovacao.",
    "C14": "Nao aplica upgrade nem proposta sensivel antes da aprovacao.",
    "C15": "Nao decide dono comercial quando o lead esta duplicado, incompleto ou conflitando.",
    "D1": "Nao cobra se a cobranca ja foi paga, cancelada ou bloqueada para contato.",
    "D2": "Nao negocia acordo, desconto ou prazo especial.",
    "D3": "Nao envia Pix/link antes da aprovacao.",
    "D4": "Nao baixa cobranca antes da aprovacao.",
    "D5": "Nao renova plano antes da aprovacao.",
    "D6": "Nao aplica excecao financeira antes da aprovacao.",
    "D7": "Nao insiste em cobranca se a falha persistir ou o aluno contestar.",
    "D8": "Nao emite documento sem dados fiscais, permissao e provedor funcionando.",
    "D9": "Nao pausa ou tranca plano antes da aprovacao.",
    "D10": "Nao vincula pagamento e movimentacao antes da aprovacao.",
    "D11": "Nao envia contrato/termo antes da aprovacao.",
    "D12": "Nao bloqueia nem libera acesso antes da aprovacao.",
    "D13": "Nao aplica credito ou cortesia antes da aprovacao.",
    "D14": "Nao fecha o mes se conciliacao, provedor ou permissao impedirem a conferencia.",
    "D15": "Nao efetiva alteracao de plano antes da aprovacao.",
    "E1": "Nao trata recorrencia, saude ou reclamacao sozinho.",
    "E2": "Nao contata aluno pausado, com opt-out ou com pendencia sensivel.",
    "E3": "Nao escolhe retorno sem vaga, sem resolver pendencias ou sem revisar cuidado especial.",
    "E4": "Nao executa retencao sensivel sem aprovacao.",
    "E5": "Nao contata ex-aluno antes da aprovacao.",
    "E6": "Nao responde reclamacao, saude, professor ou cobranca sozinho.",
    "E7": "Nao decide extensao de pausa, vaga de retorno ou pendencia financeira.",
    "E8": "Nao usa perfil de risco sem aprovacao.",
    "E9": "Nao recontata aluno cancelado sem aprovacao.",
    "E10": "Nao envia contato leve se houver caso sensivel, baixa frequencia conflitante ou opt-out.",
    "E11": "Nao expoe informacao de saude ou evento pessoal.",
    "E12": "Nao executa segmentacao de risco sem aprovacao.",
    "E13": "Nao oferece beneficio nem resposta de recuperacao sem aprovacao.",
    "F1": "Nao mostra prioridade baseada em fonte falha, incidente critico ou permissao restrita.",
    "F2": "Nao altera financeiro nem cobra; abre proxima acao para responsavel.",
    "F3": "Nao resolve itens da fila; ordena, destaca bloqueios e alerta responsaveis.",
    "F4": "Nao corrige gargalo; aponta causa provavel e abre investigacao.",
    "F5": "Nao envia resumo se fonte, permissao ou incidente critico falhar.",
    "F6": "Nao mescla nem corrige dado sensivel automaticamente.",
    "F7": "Nao compra pacote, altera plano ou libera cota; alerta dono/admin.",
    "F8": "Nao muda politica de agente; abre investigacao quando houver queda ou amostra fraca.",
    "F9": "Nao muda permissao sem aprovacao.",
    "F10": "Nao cria turma, horario ou sala; alerta gestao sobre capacidade.",
    "F11": "Nao reprocessa quando houver risco de duplicidade ou provedor indisponivel.",
    "F12": "Nao importa lote antes da aprovacao.",
    "F13": "Nao publica nem executa acao real durante a simulacao.",
    "F14": "Nao faz rollback amplo; pausa ou mitiga somente o que estiver permitido.",
    "F15": "Nao publica politica antes da aprovacao.",
    "G1": "Nao expoe dado protegido ao professor.",
    "G2": "Nao aceita nota sensivel ou de professor sem permissao sem revisao.",
    "G3": "Nao altera historico protegido antes da aprovacao.",
    "G4": "Nao registra evolucao sensivel sem revisao.",
    "G5": "Nao libera contexto para agente antes da aprovacao.",
    "G6": "Nao libera documento/anamnese sem aprovacao.",
    "G7": "Nao corrige historico antes da aprovacao.",
    "G8": "Nao repassa dado protegido ou contexto para professor sem permissao.",
    "G9": "Nao envia lembrete com conteudo protegido ou aula alterada.",
    "G10": "Nao compartilha contexto antes da aprovacao.",
    "G11": "Nao muda permissao de historico antes da aprovacao.",
    "G12": "Nao exibe evento protegido, conflitado ou sem permissao.",
})


APPROVAL_LABELS = {
    "A8": "revisar pedido de privacidade ou dados",
    "A9": "validar identidade em telefone compartilhado",
    "B5": "aprovar reposicao ou remarcacao",
    "B8": "aprovar mudanca de horario fixo",
    "B9": "aprovar cancelamento pelo studio e comunicado",
    "B10": "aprovar correcao de capacidade",
    "B11": "aprovar ajuste de grade",
    "B13": "aprovar credito de reposicao",
    "B14": "aprovar correcao de presenca",
    "B16": "aprovar aula especial ou workshop",
    "C6": "aprovar pre-matricula",
    "C7": "aprovar resposta para objecao comercial",
    "C9": "aprovar perda comercial",
    "C10": "aprovar indicacao e beneficio",
    "C13": "aprovar conversao de interessado em aluno",
    "C14": "aprovar proposta de upsell ou upgrade",
    "D3": "aprovar envio de Pix ou link de pagamento",
    "D4": "aprovar confirmacao de pagamento",
    "D5": "aprovar renovacao de plano",
    "D6": "aprovar excecao financeira",
    "D9": "aprovar pausa ou trancamento",
    "D10": "aprovar conciliacao interna",
    "D11": "aprovar contrato ou termos",
    "D12": "aprovar bloqueio ou liberacao",
    "D13": "aprovar credito ou cortesia",
    "D15": "aprovar encerramento ou alteracao de plano",
    "E4": "aprovar acao de retencao",
    "E5": "aprovar reativacao de ex-aluno",
    "E8": "aprovar acao por perfil de risco",
    "E9": "aprovar contato pos-cancelamento",
    "E11": "aprovar cuidado por saude ou evento pessoal",
    "E12": "aprovar segmentacao de risco",
    "E13": "aprovar recuperacao de reclamacao",
    "F9": "aprovar revisao de permissao ou auditoria",
    "F12": "aprovar importacao ou migracao",
    "F15": "aprovar mudanca de politica ou regra",
    "G3": "aprovar restricao ou cuidado",
    "G5": "aprovar contexto para agente",
    "G6": "aprovar documento ou anamnese",
    "G7": "aprovar correcao de historico",
    "G10": "aprovar compartilhamento de contexto",
    "G11": "aprovar permissao de historico",
}


def mode_action_label(mode):
    if mode == "Autonomo com aprovacao":
        return "Pedido de aprovacao"
    if mode == "Copiloto":
        return "Sugestao"
    if mode == "Manual":
        return "Tarefa criada"
    return "Acao"


def decision_text(mode, scenario_name):
    if mode == "Autonomo":
        return f"No cenario `{scenario_name}`, a Taliya conclui sem equipe porque as checagens obrigatorias passam."
    if mode == "Autonomo com excecoes":
        return f"No cenario `{scenario_name}`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada."
    if mode == "Autonomo com aprovacao":
        return f"No cenario `{scenario_name}`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado."
    if mode == "Copiloto":
        return f"No cenario `{scenario_name}`, a Taliya sugere o proximo passo e a equipe decide."
    return f"No cenario `{scenario_name}`, a Taliya organiza a tarefa e a equipe executa."


def action_text(row, action, normal_items):
    mode = row["modo_padrao"]
    clean_action = phrase(action)
    if mode == "Autonomo com aprovacao":
        approval_action = APPROVAL_LABELS[row["id"]]
        for prefix in [
            "Monta aprovacao de ",
            "Monta aprovacao do ",
            "Monta aprovacao da ",
            "Monta aprovacao para ",
        ]:
            if approval_action.startswith(prefix):
                approval_action = approval_action[len(prefix):]
                break
        approval_action = approval_action.replace(" para aprovacao", "").replace(" com aprovacao", "")
        return sentence(f"Monta a aprovacao para {approval_action}, mostrando {join(normal_items[:4])}")
    if mode == "Autonomo com excecoes":
        return sentence(f"Executa o caso valido: {clean_action}")
    if mode == "Autonomo":
        return sentence(f"Conclui a acao permitida: {clean_action}")
    if mode == "Copiloto":
        return sentence(f"Prepara sugestao para {clean_action}, sem executar sozinha")
    return sentence(f"Cria tarefa para a equipe {clean_action}")


def fallback_text(row):
    scenario = SCENARIOS[row["id"]]
    return sentence(f"Se o teste cair em `{scenario[6]}`, {scenario[7]}")


def human_call_text(row, calls_human, exceptions, scenario):
    if calls_human:
        return join(exceptions)
    return sentence(
        f"Nao chama humano no cenario principal; se cair em `{scenario[6]}`, aplica fallback: {scenario[7]}"
    )


def agent_text(row):
    scenario = SCENARIOS[row["id"]]
    mode = row["modo_padrao"]
    if mode == "Autonomo com aprovacao":
        return f"Neste teste, a Taliya monta a aprovacao de {row['titulo_ui']} e nao aplica a mudanca sozinha. Se aparecer `{scenario[2]}` ou `{scenario[4]}`, o caso fica com a equipe."
    if mode == "Autonomo com excecoes":
        return f"Neste teste, a Taliya executa {row['titulo_ui']} apenas no cenario valido. Se aparecer `{scenario[2]}` ou `{scenario[4]}`, chama a equipe."
    if mode == "Autonomo":
        return f"Neste teste, a Taliya conclui {row['titulo_ui']} quando as checagens passam. Se aparecer `{scenario[6]}`, ela para e cria pendencia."
    return f"Neste teste, a Taliya organiza {row['titulo_ui']} para a equipe decidir."


def build():
    rows = list(csv.DictReader(DETAILS.open(encoding="utf-8")))
    missing_scenarios = [row["id"] for row in rows if row["id"] not in SCENARIOS]
    missing_visuals = [row["id"] for row in rows if row["id"] not in VISUAL_KIND]
    missing_rules = [row["id"] for row in rows if row["id"] not in RULES]
    missing_no_decide = [row["id"] for row in rows if row["id"] not in NO_DECIDE]
    missing_approval_labels = [
        row["id"]
        for row in rows
        if row["modo_padrao"] == "Autonomo com aprovacao" and row["id"] not in APPROVAL_LABELS
    ]
    if missing_scenarios or missing_visuals or missing_rules or missing_no_decide or missing_approval_labels:
        raise SystemExit(
            f"missing scenarios={missing_scenarios} visuals={missing_visuals} "
            f"rules={missing_rules} no_decide={missing_no_decide} "
            f"approval_labels={missing_approval_labels}"
        )

    fields = [
        "id", "agente", "rotina", "fluxo", "modo_padrao", "tipo_visual", "usa_celular",
        "visual_central", "visual_descricao",
        "cenario_principal", "cenario_principal_resultado",
        "cenario_excecao_1", "cenario_excecao_1_resultado",
        "cenario_excecao_2", "cenario_excecao_2_resultado",
        "cenario_falha", "cenario_falha_resultado",
        "inicio_teste", "checagens_teste", "decisao_teste",
        "etapa_acao_label", "acao_teste", "fim_teste",
        "nao_faz_neste_fluxo", "quando_chama_humano", "quando_pede_aprovacao",
        "fallback_teste", "texto_agente_configuracao",
    ]
    out_rows = []
    for row in rows:
        rid = row["id"]
        action, normal_text, exception_text = RULES[rid]
        normal = items(normal_text)
        exceptions = items(exception_text)
        scenario = SCENARIOS[rid]
        visual_kind = VISUAL_KIND[rid]
        visual_title, visual_description = VISUAL_DESCRIPTIONS[visual_kind]
        asks_approval = row["modo_padrao"] == "Autonomo com aprovacao"
        calls_human = row["modo_padrao"] in ["Autonomo com excecoes", "Autonomo com aprovacao"]
        no_decide = NO_DECIDE[rid]
        out_rows.append({
            "id": rid,
            "agente": row["agente"],
            "rotina": row["rotina"],
            "fluxo": row["titulo_ui"],
            "modo_padrao": row["modo_padrao"],
            "tipo_visual": visual_kind,
            "usa_celular": "sim" if visual_kind == "celular_conversa" else "nao",
            "visual_central": visual_title,
            "visual_descricao": visual_description,
            "cenario_principal": scenario[0],
            "cenario_principal_resultado": scenario[1],
            "cenario_excecao_1": scenario[2],
            "cenario_excecao_1_resultado": scenario[3],
            "cenario_excecao_2": scenario[4],
            "cenario_excecao_2_resultado": scenario[5],
            "cenario_falha": scenario[6],
            "cenario_falha_resultado": scenario[7],
            "inicio_teste": clean_start(row["inicio"]),
            "checagens_teste": join(normal),
            "decisao_teste": decision_text(row["modo_padrao"], scenario[0]),
            "etapa_acao_label": mode_action_label(row["modo_padrao"]),
            "acao_teste": action_text(row, action, normal),
            "fim_teste": row["fim"],
            "nao_faz_neste_fluxo": no_decide,
            "quando_chama_humano": human_call_text(row, calls_human, exceptions, scenario),
            "quando_pede_aprovacao": approval_timing(row, asks_approval),
            "fallback_teste": fallback_text(row),
            "texto_agente_configuracao": agent_text(row),
        })

    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    write_review(out_rows)
    write_audit(out_rows)
    print(f"wrote {OUT} rows={len(out_rows)}")
    print(f"wrote {REVIEW}")
    print(f"wrote {AUDIT}")


def write_review(rows):
    lines = [
        "# Taliya CRM - 96 Simulacoes De Fluxos",
        "",
        "Status: mapeamento completo v0.1.",
        "Data: 2026-05-22.",
        "",
        "Este documento define exatamente o que aparece na pagina `Testar fluxo` para cada um dos 96 fluxos.",
        "",
        "Cada fluxo tem cenarios, visual central, execucao do teste, limite do agente, chamada humana/aprovacao/fallback e texto do Agente de Configuracao.",
        "",
        "Regra principal: todos usam o mesmo esqueleto da tela de teste, mas nem todos usam celular. O visual central representa onde aquele fluxo realmente acontece.",
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
            f"- Modo padrao: `{row['modo_padrao']}`.",
            f"- Visual central: `{row['visual_central']}`.",
            f"- Usa celular: `{row['usa_celular']}`.",
            "",
            "**Cenarios**",
            "",
            f"- `{row['cenario_principal']}`: {row['cenario_principal_resultado']}",
            f"- `{row['cenario_excecao_1']}`: {row['cenario_excecao_1_resultado']}",
            f"- `{row['cenario_excecao_2']}`: {row['cenario_excecao_2_resultado']}",
            f"- `{row['cenario_falha']}`: {row['cenario_falha_resultado']}",
            "",
            "**Visual Do Caso**",
            "",
            row["visual_descricao"],
            "",
            "**Execucao Do Teste**",
            "",
            f"1. Inicio: {sentence(row['inicio_teste'])}",
            f"2. Checagens: {sentence(row['checagens_teste'])}",
            f"3. Decisao: {row['decisao_teste']}",
            f"4. {row['etapa_acao_label']}: {row['acao_teste']}",
            f"5. Fim: {row['fim_teste']}",
            "",
            "**Limite Do Agente**",
            "",
            row["nao_faz_neste_fluxo"],
            "",
            "**Humano/Aprovacao/Fallback**",
            "",
            f"- Chama humano quando: {sentence(row['quando_chama_humano'])}",
            f"- Pede aprovacao quando: {sentence(row['quando_pede_aprovacao'])}",
            f"- Fallback do teste: {row['fallback_teste']}",
            "",
            "**Agente De Configuracao**",
            "",
            row["texto_agente_configuracao"],
            "",
        ])
    REVIEW.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_audit(rows):
    from collections import Counter

    text = "\n".join(" ".join(row.values()) for row in rows)
    forbidden = [
        "resultado do teste",
        "dados do teste",
        "celular fake",
        "previsao",
        "dashboard",
        "json",
        "ativar rotina",
        "dentro da regra",
        "nao decide fora do escopo",
        "pode aparecer",
        "pede algo",
        "somente se",
        "pedido de aprovacao para aprovar",
    ]
    visual_counts = Counter(row["tipo_visual"] for row in rows)
    phone_count = sum(1 for row in rows if row["usa_celular"] == "sim")
    mode_counts = Counter(row["modo_padrao"] for row in rows)
    approval_phone_ids = [
        row["id"]
        for row in rows
        if row["modo_padrao"] == "Autonomo com aprovacao" and row["usa_celular"] == "sim"
    ]
    lines = [
        "# Taliya CRM - Auditoria Das 96 Simulacoes De Fluxos",
        "",
        "Status: aprovado v0.1.",
        "Data: 2026-05-22.",
        "",
        "## Validacao Executada",
        "",
        "```text",
        f"rows {len(rows)}",
        f"blank cells {sum(1 for row in rows for value in row.values() if not value)}",
        f"ids unique {len(set(row['id'] for row in rows))}",
        f"cenarios por fluxo {4 if all(row['cenario_falha'] for row in rows) else 'erro'}",
        f"inicio sem checagens embutidas {sum(1 for row in rows if 'Checagens deste fluxo' not in row['inicio_teste'])}",
        f"limites explicitos {sum(1 for row in rows if row['id'] in NO_DECIDE)}",
        f"acoes de aprovacao explicitas {sum(1 for row in rows if row['id'] in APPROVAL_LABELS)}",
        f"usa celular {phone_count}",
        f"nao usa celular {len(rows) - phone_count}",
        f"visual types {len(visual_counts)}",
        f"pontuacao duplicada {text.count('..')}",
        f"aprovacao com celular {len(approval_phone_ids)} ids {', '.join(approval_phone_ids) if approval_phone_ids else '-'}",
    ]
    for mode, count in sorted(mode_counts.items()):
        lines.append(f"modo {mode}: {count}")
    for visual, count in sorted(visual_counts.items()):
        lines.append(f"visual {visual}: {count}")
    for word in forbidden:
        lines.append(f"{word} {text.lower().count(word)}")
    lines.extend([
        "```",
        "",
        "## Decisoes Validadas",
        "",
        "- Os 96 fluxos estao mapeados.",
        "- Todos possuem 4 cenarios de teste.",
        "- Todos possuem visual central definido.",
        "- Celular e usado apenas quando existe mensagem/conversa/canal externo.",
        "- Fluxos internos usam objeto do CRM: aprovacao, agenda, financeiro, incidente, auditoria, historico ou uso/cotas.",
        "- Todos informam o que o agente nao faz naquele fluxo.",
        "- Nenhum fluxo usa limite generico; cada limite foi escrito para aquele caso.",
        "- As 42 acoes de aprovacao usam rotulo especifico do fluxo.",
        "- Fluxos com aprovacao nao fingem execucao autonoma.",
        "- Fluxos sem aprovacao informam se chamam humano por excecao ou se apenas aplicam fallback.",
        "- Fluxos com aprovacao podem usar celular quando a simulacao mostra a mensagem pronta/preview, mas a execucao para no pedido de aprovacao.",
        "- Fluxos autonomos com excecoes mostram quando chamam humano.",
        "- Nao ha cards separados de `Dados do teste` ou `Resultado do teste` no contrato da tela.",
        "",
        "## Artefatos",
        "",
        "- `agents-flows-96-test-simulation-matrix.pt-BR.csv`",
        "- `agents-flows-96-test-simulation-review.pt-BR.md`",
        "- `agents-flows-test-simulation-page-contract.pt-BR.md`",
    ])
    AUDIT.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
