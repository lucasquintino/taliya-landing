import csv
import importlib.util
from pathlib import Path

BASE = Path("specs/006-crm-operational-core")
SRC = BASE / "agents-flows-final-flow-contract-matrix.pt-BR.csv"
DETAIL = BASE / "agents-flows-detailed-mode-rules-matrix.pt-BR.csv"
OUT = BASE / "agents-flows-96-complete-detail-matrix.pt-BR.csv"
REVIEW = BASE / "agents-flows-96-complete-detail-review.pt-BR.md"
RULES_PATH = Path("scripts/generate-taliya-detailed-mode-rules.py")


spec = importlib.util.spec_from_file_location("rules_module", RULES_PATH)
rules_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rules_module)
RULES = rules_module.RULES


STARTS = {
    "A1": "O fluxo comeca quando uma nova mensagem chega por WhatsApp, inbox ou outro canal conectado e ainda nao tem destino claro.",
    "A2": "O fluxo comeca quando um lead, aluno ou responsavel faz uma pergunta que pode estar na base aprovada do studio.",
    "A3": "O fluxo comeca quando uma conversa parece vir de aluno existente e precisa ser ligada ao cadastro certo antes de continuar.",
    "A4": "O fluxo comeca quando a pessoa pede algo que nao pertence ao escopo operacional do CRM do studio.",
    "A5": "O fluxo comeca quando uma conversa precisa sair da automacao e ir para uma pessoa da equipe.",
    "A6": "O fluxo comeca quando o contato pede consentimento, opt-out ou mudanca de preferencia de comunicacao.",
    "A7": "O fluxo comeca quando a conversa recebe audio, imagem, documento ou outra midia que precisa ser interpretada com cuidado.",
    "A8": "O fluxo comeca quando alguem pede acesso, exclusao, copia ou revisao de dados pessoais.",
    "A9": "O fluxo comeca quando o mesmo telefone pode representar mais de um aluno, responsavel ou cadastro.",
    "A10": "O fluxo comeca quando uma conversa, fila ou atendimento precisa ser acompanhado por prazo, dono e status.",
    "B1": "O fluxo comeca quando chega o horario de confirmar presenca de alunos em uma aula publicada.",
    "B2": "O fluxo comeca quando o aluno avisa que nao vai comparecer a uma aula.",
    "B3": "O fluxo comeca quando a aula termina e um aluno previsto nao apareceu nem avisou antes.",
    "B4": "O fluxo comeca quando uma vaga abre em uma aula e pode ser oferecida a alguem elegivel.",
    "B5": "O fluxo comeca quando um aluno precisa repor ou remarcar uma aula dentro das regras do studio.",
    "B6": "O fluxo comeca quando existe lista de espera e uma vaga compativel pode ser distribuida.",
    "B7": "O fluxo comeca quando um interessado precisa receber horarios possiveis para aula experimental.",
    "B8": "O fluxo comeca quando um aluno pede ou precisa mudar seu horario fixo.",
    "B9": "O fluxo comeca quando o studio precisa cancelar uma aula e comunicar os alunos afetados.",
    "B10": "O fluxo comeca quando a agenda encontra conflito de capacidade, lotacao ou direito de vaga.",
    "B11": "O fluxo comeca quando o studio quer alterar grade, horarios, professores ou vigencia da agenda.",
    "B12": "O fluxo comeca quando um lead marcado para aula experimental nao comparece.",
    "B13": "O fluxo comeca quando uma falta, remarcacao ou decisao operacional pode gerar credito de reposicao.",
    "B14": "O fluxo comeca quando alguem pede para corrigir uma presenca ja registrada.",
    "B15": "O fluxo comeca quando um aluno esta perto da primeira aula e precisa de acompanhamento inicial.",
    "B16": "O fluxo comeca quando o studio cria ou altera uma aula especial, workshop ou evento.",
    "C1": "O fluxo comeca quando lead ou aluno pergunta sobre valores, planos ou condicoes comerciais aprovadas.",
    "C2": "O fluxo comeca quando um lead quer marcar uma aula experimental.",
    "C3": "O fluxo comeca quando chega o horario de lembrar um lead sobre a aula experimental marcada.",
    "C4": "O fluxo comeca depois que uma aula experimental acontece e o lead precisa de acompanhamento comercial.",
    "C5": "O fluxo comeca quando um lead entra em uma etapa de follow-up comercial permitida pela cadencia.",
    "C6": "O fluxo comeca quando o lead aceita avancar para pre-matricula.",
    "C7": "O fluxo comeca quando o lead traz uma objecao comercial que precisa de resposta cuidadosa.",
    "C8": "O fluxo comeca quando um lead precisa ser qualificado por origem, perfil e dados minimos.",
    "C9": "O fluxo comeca quando um lead deve ser marcado como perdido ou sem continuidade comercial.",
    "C10": "O fluxo comeca quando uma indicacao ou beneficio de indicacao precisa ser analisado.",
    "C11": "O fluxo comeca quando um checkout, proposta ou matricula fica abandonado antes de concluir.",
    "C12": "O fluxo comeca quando um lead quer uma turma, horario ou vaga que o studio nao tem disponivel agora.",
    "C13": "O fluxo comeca quando um interessado esta pronto para virar aluno no CRM.",
    "C14": "O fluxo comeca quando um aluno pode receber proposta de upgrade, upsell ou mudanca de plano.",
    "C15": "O fluxo comeca quando um lead entra por canal, formulario, importacao ou origem externa.",
    "D1": "O fluxo comeca quando uma cobranca esta perto do vencimento.",
    "D2": "O fluxo comeca quando uma cobranca passa do vencimento e precisa de acao financeira.",
    "D3": "O fluxo comeca quando a equipe precisa enviar Pix, link ou instrucao de pagamento.",
    "D4": "O fluxo comeca quando um aluno informa pagamento e a confirmacao precisa ser conferida.",
    "D5": "O fluxo comeca quando um plano esta perto de renovar ou precisa iniciar novo ciclo.",
    "D6": "O fluxo comeca quando aparece pedido financeiro fora da regra comum.",
    "D7": "O fluxo comeca quando o provedor ou o CRM identifica falha de pagamento.",
    "D8": "O fluxo comeca quando o aluno precisa de recibo, nota ou documento financeiro permitido.",
    "D9": "O fluxo comeca quando o aluno pede pausa, trancamento ou interrupcao temporaria.",
    "D10": "O fluxo comeca quando um pagamento precisa ser conciliado com uma movimentacao interna.",
    "D11": "O fluxo comeca quando contrato, termo ou documento precisa ser preparado para aluno ou plano.",
    "D12": "O fluxo comeca quando o studio precisa bloquear ou liberar acesso por motivo financeiro.",
    "D13": "O fluxo comeca quando alguem pede credito, cortesia ou ajuste financeiro excepcional.",
    "D14": "O fluxo comeca quando chega o periodo de fechamento financeiro do mes.",
    "D15": "O fluxo comeca quando plano de aluno precisa ser encerrado ou alterado de forma efetiva.",
    "E1": "O fluxo comeca quando a frequencia de um aluno cai abaixo do padrao esperado.",
    "E2": "O fluxo comeca quando um aluno ativo fica inativo por tempo relevante.",
    "E3": "O fluxo comeca quando um aluno demonstra interesse em voltar.",
    "E4": "O fluxo comeca quando aparecem sinais de risco de cancelamento.",
    "E5": "O fluxo comeca quando um ex-aluno entra em segmento permitido para reativacao.",
    "E6": "O fluxo comeca quando chega a janela de medir satisfacao ou cuidado com o aluno.",
    "E7": "O fluxo comeca quando uma pausa esta perto de terminar.",
    "E8": "O fluxo comeca quando um perfil ou segmento indica risco de evasao.",
    "E9": "O fluxo comeca depois que um cancelamento foi registrado e ainda pode haver cuidado pos-cancelamento.",
    "E10": "O fluxo comeca quando um aluno atinge um marco de engajamento permitido.",
    "E11": "O fluxo comeca quando aparece informacao de saude, evento pessoal ou cuidado sensivel.",
    "E12": "O fluxo comeca quando o studio quer usar segmentacao de risco para acao operacional.",
    "E13": "O fluxo comeca quando uma reclamacao precisa de recuperacao de confianca.",
    "F1": "O fluxo comeca quando chega o horario de montar as prioridades operacionais do dia.",
    "F2": "O fluxo comeca quando o CRM identifica oportunidade financeira parada ou dinheiro na mesa.",
    "F3": "O fluxo comeca quando ha tarefas, aprovacoes ou casos humanos acumulados.",
    "F4": "O fluxo comeca quando indicadores mostram gargalo operacional.",
    "F5": "O fluxo comeca quando a semana fecha e o studio precisa de resumo executivo.",
    "F6": "O fluxo comeca quando o CRM detecta dado incompleto, duplicado ou inconsistente.",
    "F7": "O fluxo comeca quando uso, creditos, limites ou cotas precisam ser monitorados.",
    "F8": "O fluxo comeca quando indicadores de agentes precisam ser acompanhados.",
    "F9": "O fluxo comeca quando evento de permissao ou auditoria exige revisao.",
    "F10": "O fluxo comeca quando ocupacao, capacidade ou crescimento chegam perto de limite relevante.",
    "F11": "O fluxo comeca quando integracao, webhook ou tentativa tecnica falha.",
    "F12": "O fluxo comeca quando uma importacao ou migracao precisa ser validada.",
    "F13": "O fluxo comeca quando alguem testa um fluxo antes de publicar ou alterar operacao.",
    "F14": "O fluxo comeca quando uma automacao falha, gera incidente ou precisa de correcao operacional.",
    "F15": "O fluxo comeca quando politica, regra ou comportamento operacional precisa mudar.",
    "G1": "O fluxo comeca antes de uma aula, quando o professor precisa de contexto permitido.",
    "G2": "O fluxo comeca depois da aula, quando uma observacao precisa ser registrada.",
    "G3": "O fluxo comeca quando restricao, cuidado ou informacao sensivel precisa ser revisada.",
    "G4": "O fluxo comeca quando objetivo ou evolucao do aluno precisa ser acompanhado.",
    "G5": "O fluxo comeca quando algum agente precisa de contexto de historico permitido.",
    "G6": "O fluxo comeca quando documento, anamnese ou arquivo do aluno precisa de revisao.",
    "G7": "O fluxo comeca quando alguem pede correcao de historico.",
    "G8": "O fluxo comeca quando professor precisa repassar contexto para outro professor.",
    "G9": "O fluxo comeca quando professor precisa receber lembrete operacional.",
    "G10": "O fluxo comeca quando contexto do aluno precisa ser compartilhado com alguem.",
    "G11": "O fluxo comeca quando permissao de historico precisa ser alterada ou revisada.",
    "G12": "O fluxo comeca quando a linha do tempo do aluno precisa ser organizada ou exibida.",
}


ALIASES = {
    "B3": "Falta sem aviso",
    "B12": "Experimental sem comparecimento",
}


ENDINGS = {
    "A1": "A conversa fica classificada, o atendimento abre na fila correta e o historico mostra por que aquele destino foi escolhido. Se houver conflito de assunto, identidade ou fila, a conversa vira caso humano no Inbox.",
    "A2": "A resposta aprovada e enviada na conversa e a pergunta fica registrada como atendida pela base permitida. Se a pergunta sair da base, pedir dado privado ou exigir condicao especial, nasce uma tarefa de resposta para a equipe.",
    "A3": "A conversa fica ligada ao cadastro certo e o atendimento segue com contexto do aluno permitido para aquela fila. Se houver telefone compartilhado, duplicidade ou pedido sensivel, a Taliya segura os dados e cria revisao humana.",
    "A4": "A pessoa recebe a resposta padrao de fora do escopo e, quando fizer sentido, o pedido vira tarefa/caso no destino configurado. Se o texto indicar reclamacao, emergencia, saude ou dado pessoal, o caso vai para humano.",
    "A5": "O humano recebe a conversa com resumo, prioridade e fila definida. Se a Taliya nao conseguir escolher fila, prioridade ou responsavel, o caso fica em pendencia operacional ate alguem assumir.",
    "A6": "A preferencia de contato, consentimento ou opt-out fica registrado no contato e passa a valer para os proximos envios. Se o pedido for ambiguo, envolver telefone compartilhado ou pedir dados pessoais, a revisao vai para responsavel.",
    "A7": "A midia fica vinculada ao atendimento com classificacao segura e destino de revisao quando precisar. Se o arquivo for ilegivel, sensivel, nao aceito ou a identidade nao conferir, a Taliya nao usa o conteudo e abre revisao.",
    "A8": "O pedido de privacidade vira uma aprovacao com solicitante, tipo de dado, escopo e SLA. Se aprovado, a equipe executa a resposta de dados; se recusado ou vencido, o caso fica pendente para o responsavel de privacidade.",
    "A9": "O telefone compartilhado fica marcado e nenhum dado sensivel e exposto antes da validacao. Se a validacao nao separar claramente aluno, responsavel e permissao, o atendimento fica com humano.",
    "A10": "A conversa recebe status, dono, prazo e alerta de SLA. Se o SLA vencer, ficar sem dono ou virar assunto sensivel, aparece em Hoje/Tarefas para continuidade humana.",
    "B1": "A confirmacao e enviada, a resposta do aluno atualiza a aula e quem nao respondeu fica visivel para acompanhamento. Se aula, aluno, resposta ou envio tiver conflito, a pendencia fica na aula.",
    "B2": "A falta avisada fica registrada na aula, a mensagem permitida e enviada e o caso abre a proxima tarefa de reposicao quando configurado. Se prazo, aluno, aula, credito ou envio nao fecharem, a equipe decide o proximo passo.",
    "B3": "A ausencia sem aviso fica marcada depois da janela de tolerancia e abre acompanhamento de recuperacao ou retencao. Se a chamada do professor, aviso paralelo ou historico do aluno nao baterem, a equipe revisa antes de contato.",
    "B4": "A vaga aberta gera convite para o aluno elegivel conforme prioridade e limite de convites. Se houver empate, lote grande, credito duvidoso ou risco de furar fila, a oferta fica parada para decisao.",
    "B5": "A reposicao ou remarcacao vira pedido de aprovacao com credito, vaga, prazo e impacto na agenda. Se aprovado, a agenda muda; se recusado ou vencido, a solicitacao fica como tarefa em reposicoes.",
    "B6": "A lista de espera recebe convite para a vaga compativel e o status do aluno muda conforme resposta ou prazo. Se prioridade, vaga, credito ou envio nao fecharem, a equipe assume a distribuicao.",
    "B7": "O interessado recebe horarios de experimental que existem de verdade e a resposta segue para agendamento comercial. Se nao houver vaga, houver experimental duplicada ou pedido especial, o comercial recebe tarefa.",
    "B8": "A mudanca de horario fixo vira aprovacao com novo horario, impacto em capacidade e mensagem de confirmacao. Se aprovada, o cadastro do aluno e a grade sao atualizados; se nao, fica tarefa para ajuste humano.",
    "B9": "O cancelamento pelo studio vira aprovacao com aula, motivo, alunos afetados e comunicado. Se aprovado, alunos recebem orientacao e reposicao/credito; se nao, a aula permanece sem alteracao automatica.",
    "B10": "O conflito de capacidade vira aprovacao com quem foi afetado, prioridade e alternativa proposta. Se aprovado, a correcao ajusta vaga/turma; se nao, o conflito fica aberto para coordenacao.",
    "B11": "O ajuste de grade vira simulacao aprovada com vigencia, aulas, alunos, professores e comunicacao. Se aprovado, a grade muda na data definida; se houver conflito, a simulacao volta para revisao.",
    "B12": "O nao comparecimento ao experimental abre follow-up comercial ou remarcacao dentro da cadencia. Se o lead avisou por outro canal, pediu excecao ou nao ha vaga, o comercial decide a abordagem.",
    "B13": "O credito de reposicao vira aprovacao com origem, validade e politica aplicada. Se aprovado, o credito aparece para uso em reposicao; se contestado ou duplicado, fica com o responsavel.",
    "B14": "A correcao de presenca vira aprovacao com aula, aluno, motivo e impacto. Se aprovada, a chamada e atualizada preservando historico anterior; se houver impacto em credito/financeiro, fica pendente.",
    "B15": "A primeira aula recebe checklist, orientacao e responsavel definidos. Se houver cuidado, restricao, troca de aula ou professor indefinido, a equipe recebe tarefa antes do contato.",
    "B16": "A aula especial ou workshop vira aprovacao com data, capacidade, regra de inscricao e comunicacao. Se aprovado, o evento entra na agenda; se conflitar com grade, preco ou beneficio, fica em revisao.",
    "C1": "O lead recebe valores e planos somente da base aprovada e a conversa fica pronta para proxima etapa comercial. Se pedir desconto, promessa ou condicao fora da base, o comercial assume.",
    "C2": "A aula experimental e marcada ou preparada com horario real, responsavel e dados do lead. Se horario, vaga, duplicidade ou excecao comercial nao fecharem, vira tarefa para o comercial.",
    "C3": "O lembrete do experimental e enviado uma vez no horario configurado e o status do lead mostra que foi lembrado. Se a aula mudou, o lead pediu opt-out ou respondeu com mudanca, o fluxo para.",
    "C4": "Depois da experimental, o lead entra no acompanhamento comercial correto com presenca e proxima acao. Se houve falta, observacao sensivel, desconto ou reclamacao, o comercial decide.",
    "C5": "O follow-up e enviado dentro da cadencia e a etapa comercial avanca conforme resposta ou ausencia de resposta. Se o lead pediu humano, desconto, garantia ou parar contato, o fluxo para.",
    "C6": "A pre-matricula vira aprovacao com plano, checklist, dados e responsavel. Se aprovada, segue para matricula/contrato; se faltarem dados, valor ou documento, fica pendente.",
    "C7": "A objecao comercial vira resposta revisada com limite de promessa e impacto. Se aprovada, a resposta vai para o lead; se envolver desconto, garantia ou promessa indevida, fica com humano.",
    "C8": "O lead recebe origem, perfil, dono e campos minimos preenchidos. Se houver duplicidade, origem desconhecida ou etapa conflitante, a ficha fica pendente para limpeza.",
    "C9": "A perda comercial vira aprovacao com motivo e impacto nos relatorios. Se aprovada, o lead sai da cadencia; se ainda houver acao aberta ou motivo sensivel, o comercial revisa.",
    "C10": "A indicacao vira aprovacao com indicador, indicado, regra de vinculo e beneficio calculado. Se aprovada, o beneficio entra no processo correto; se houver duplicidade ou conflito, fica pendente.",
    "C11": "O abandono de checkout recebe recuperacao dentro da cadencia e o lead continua no funil. Se houve falha financeira, desconto, reclamacao ou checkout expirado, o comercial assume.",
    "C12": "A demanda sem vaga entra em lista de interesse sem promessa de vaga garantida. Se o lead exigir prazo, garantia ou tratamento especial, o comercial decide a resposta.",
    "C13": "A conversao de interessado em aluno vira aprovacao com plano, cadastro e checklist. Se aprovada, o aluno e criado no CRM; se contrato, pagamento, duplicidade ou dado faltar, fica pendente.",
    "C14": "O upsell ou upgrade vira proposta aprovada com plano destino e impacto financeiro. Se aprovada, a proposta e enviada ou aplicada conforme regra; se houver desconto, pendencia ou reclamacao, fica com humano.",
    "C15": "O lead de canal externo entra como ficha unica com origem, dono e campos minimos. Se duplicar, vier incompleto ou pertencer a outro responsavel, vai para revisao.",
    "D1": "O lembrete de vencimento e enviado antes do prazo e a cobranca mostra tentativa registrada. Se a cobranca foi paga, cancelada, diverge ou o aluno pediu opt-out, nao envia.",
    "D2": "O atraso abre cobranca ou tarefa financeira conforme tentativas permitidas. Se o aluno contestar, pedir acordo/desconto ou o provedor falhar, a equipe financeira assume.",
    "D3": "O Pix ou link vira aprovacao com valor, cobranca, provedor e mensagem. Se aprovado, a instrucao e enviada; se valor/provedor/condicao divergirem, fica pendente.",
    "D4": "A confirmacao de pagamento vira aprovacao com evidencia, aluno, valor e movimentacao. Se aprovada, a cobranca e baixada; se evidencia, valor ou conciliacao nao baterem, fica com financeiro.",
    "D5": "A renovacao vira aprovacao com novo ciclo, plano e comunicacao. Se aprovada, o plano renova; se houver pendencia, pausa, cancelamento ou contrato novo, fica pendente.",
    "D6": "A excecao financeira vira aprovacao com tipo, motivo, impacto e prazo. Se aprovada, a excecao e aplicada; se ultrapassar limite ou envolver contrato/reclamacao, fica com responsavel.",
    "D7": "A falha de pagamento gera contato ou tarefa conforme tentativas permitidas. Se a falha persistir, virar disputa ou depender do provedor, o financeiro assume.",
    "D8": "O recibo ou nota permitida e emitido/preparado e vinculado ao aluno. Se dados fiscais, permissao ou provedor nao fecharem, fica tarefa financeira.",
    "D9": "A pausa ou trancamento vira aprovacao com periodo, motivo, impacto no plano e retorno previsto. Se aprovada, o plano muda; se impactar financeiro ou contrato, fica pendente.",
    "D10": "A conciliacao interna vira aprovacao com candidato, confianca, valor, data e impacto. Se aprovada, movimentacao e pagamento ficam vinculados; se houver divergencia, fica com financeiro.",
    "D11": "Contrato ou termo vira aprovacao com aluno, plano, versao e dados usados. Se aprovado, o documento segue para envio/assinatura; se faltar dado ou versao, fica pendente.",
    "D12": "Bloqueio ou liberacao vira aprovacao com motivo, aluno, impacto e comunicacao. Se aprovado, o acesso muda; se houver contestacao, pagamento recente ou excecao, fica com humano.",
    "D13": "Credito ou cortesia vira aprovacao com motivo, valor, validade e impacto. Se aprovado, o beneficio aparece no financeiro; se fugir da politica, fica com responsavel.",
    "D14": "O fechamento mensal separa consolidados, pendencias e alertas financeiros para o responsavel. Se conciliacao, provedor ou dado falhar, o fechamento fica incompleto e gera tarefa.",
    "D15": "Encerramento ou alteracao de plano vira aprovacao com data efetiva, impacto financeiro e comunicacao. Se aprovado, o plano muda; se houver contrato, saldo ou pendencia, fica travado.",
    "E1": "A queda de frequencia abre contato preventivo ou tarefa de cuidado conforme regra. Se houver recorrencia, reclamacao, saude ou canal bloqueado, a equipe assume.",
    "E2": "O aluno inativo entra em retomada permitida com responsavel e limite de contato. Se pausou, pediu opt-out, tem pendencia ou caso sensivel, o fluxo para.",
    "E3": "O retorno do aluno organiza opcoes de agenda e proximo contato. Se nao houver horario, houver pendencia financeira ou cuidado especial, a equipe decide.",
    "E4": "O risco de cancelamento vira aprovacao com contexto, dono e automacoes conflitantes pausadas. Se aprovado, a acao de retencao segue; se for cancelamento formal ou caso sensivel, fica com responsavel.",
    "E5": "A reativacao de ex-aluno vira aprovacao com segmento, mensagem e responsavel. Se aprovada, o contato e liberado; se houver opt-out, reclamacao ou beneficio especial, fica bloqueado.",
    "E6": "A satisfacao e coletada ou acompanhada e, se houver sinal ruim, abre cuidado. Se a resposta citar reclamacao, saude, professor ou cobranca, vai para humano.",
    "E7": "O retorno apos pausa prepara contato e opcoes de agenda antes do fim da pausa. Se o aluno pedir extensao, nao houver vaga ou houver pendencia, vira tarefa.",
    "E8": "A acao por perfil de risco vira aprovacao com segmento, dados usados e abordagem. Se aprovada, a acao segue; se parecer invasiva ou usar dado sensivel, fica bloqueada.",
    "E9": "O pos-cancelamento vira aprovacao com janela, motivo e mensagem cuidadosa. Se aprovado, o contato e liberado; se houve reclamacao, saude ou pedido de nao contato, fica bloqueado.",
    "E10": "O marco de engajamento gera contato leve ou registro positivo. Se houver caso sensivel, baixa frequencia ou opt-out, a mensagem nao sai.",
    "E11": "Saude ou evento pessoal vira aprovacao com visibilidade, dono e cuidado proposto. Se aprovado, apenas a acao permitida segue; se houver sigilo ou dado incompleto, fica com humano.",
    "E12": "A segmentacao de risco vira aprovacao com dados usados, alunos afetados e acao permitida. Se aprovada, a acao segue; se usar dado sensivel ou volume alto, fica bloqueada.",
    "E13": "A reclamacao vira aprovacao com resumo, dono, proposta e automacoes pausadas. Se aprovada, a recuperacao segue; se envolver professor, saude, financeiro ou beneficio, fica com responsavel.",
    "F1": "As prioridades do dia aparecem em Hoje com tarefas, aprovacoes e alertas ordenados. Se fonte critica falhar ou dado estiver desatualizado, o resumo marca pendencia.",
    "F2": "A oportunidade financeira vira proxima acao para responsavel sem alterar dinheiro sozinha. Se valor, disputa, desconto ou responsavel nao fecharem, fica tarefa.",
    "F3": "A fila humana fica ordenada por prioridade, dono e prazo. Se item sem dono, aprovacao vencida ou incidente aparecer, a operacao recebe alerta.",
    "F4": "O gargalo operacional vira alerta com metrica, causa provavel e responsavel. Se tocar financeiro, grade, incidente ou dado incompleto, vira investigacao humana.",
    "F5": "O resumo semanal e enviado/gerado para destinatarios permitidos com secoes configuradas. Se fonte, permissao ou incidente critico falhar, o resumo fica pendente.",
    "F6": "A falha de qualidade de dados abre tarefa de correcao com prioridade e campo afetado. Se envolver fusao, historico protegido ou alto volume, vai para revisao.",
    "F7": "Uso, creditos e cotas recebem alerta nos limites configurados e aparecem em Uso/Cotas. Se billing divergir ou upgrade/add-on exigir decisao, vai para admin.",
    "F8": "A performance dos agentes vira relatorio ou alerta com indicador afetado. Se queda forte, amostra insuficiente ou incidente correlacionado aparecer, abre investigacao.",
    "F9": "Permissao ou evento de auditoria vira aprovacao com impacto e responsavel. Se houver suspeita de acesso indevido ou mudanca de permissao, nao aplica sem aprovacao.",
    "F10": "Capacidade e crescimento viram alerta com ocupacao, limite e acao sugerida. Se exigir nova turma, horario ou impacto financeiro, fica para decisao.",
    "F11": "Falha tecnica ou webhook recebe retry seguro quando permitido e registro no log da integracao. Se houver risco de duplicar efeito, provedor instavel ou severidade alta, vai para incidente.",
    "F12": "Importacao ou migracao vira aprovacao com amostra, conflitos, impacto e rollback. Se aprovada, o lote segue; se houver duplicidade ou campo faltando, fica bloqueado.",
    "F13": "O teste roda em simulacao, mostra caminho do fluxo e nao publica acao real. Se usar dado sensivel, falhar preflight ou tentar executar de verdade, o teste para.",
    "F14": "O incidente de automacao pausa ou mitiga o fluxo quando permitido e abre a execucao relacionada. Se afetar varios fluxos, exigir rollback ou depender de integracao, vai para incidente humano.",
    "F15": "Mudanca de politica vira aprovacao com simulacao, vigencia e comunicacao. Se aprovada, a nova versao fica pronta para publicar; se houver conflito, volta para revisao.",
    "G1": "O professor recebe contexto permitido antes da aula sem dado protegido indevido. Se houver restricao sensivel, permissao faltando ou aula alterada, o resumo nao sai.",
    "G2": "Depois da aula, o professor recebe lembrete e a observacao permitida entra no historico. Se a nota envolver cuidado, restricao ou evento sensivel, vai para revisao.",
    "G3": "Restricao ou cuidado vira aprovacao com aluno, visibilidade, dono e acao proposta. Se aprovada, o historico protegido e atualizado; se houver dado incompleto, fica pendente.",
    "G4": "Objetivo ou evolucao fica acompanhado no historico permitido e gera proximo cuidado quando configurado. Se tocar saude, restricao ou permissao de professor, vai para revisao.",
    "G5": "O contexto para outro agente vira aprovacao com escopo, dados e finalidade. Se aprovado, o agente recebe apenas o permitido; se amplo ou protegido demais, fica bloqueado.",
    "G6": "Documento ou anamnese vira aprovacao com aluno, arquivo, visibilidade e responsavel. Se aprovado, fica disponivel no historico permitido; se sensivel/incompleto, vai para revisao.",
    "G7": "A correcao de historico vira aprovacao preservando valor anterior, motivo e impacto. Se aprovada, o historico muda com rastro; se houver divergencia, fica pendente.",
    "G8": "O repasse entre professores envia resumo permitido para o professor destino. Se incluir dado protegido, destino sem permissao ou contexto incompleto, o repasse para.",
    "G9": "O lembrete do professor e enviado no horario/frequencia configurado e marcado como feito. Se aula mudou, canal falhou ou conteudo depender de dado protegido, nao envia.",
    "G10": "O compartilhamento de contexto vira aprovacao com destinatario, dados e finalidade. Se aprovado, o contexto e compartilhado; se houver restricao ou permissao faltando, fica bloqueado.",
    "G11": "Permissao de historico vira aprovacao com papel, escopo e impacto. Se aprovada, a visibilidade muda; se conflitar com permissao global ou dado protegido, fica pendente.",
    "G12": "A linha do tempo do aluno fica organizada com eventos permitidos e filtro seguro. Se aparecer evento protegido, conflito ou falta de permissao, a exibicao restringe e abre revisao.",
}


def split_items(text):
    return [item.strip() for item in text.split(";") if item.strip()]


def as_sentence(items):
    items = split_items(items) if isinstance(items, str) else list(items)
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return "; ".join(items[:-1]) + "; " + items[-1]


def first_items(text, limit=3):
    return split_items(text)[:limit]


def display_flow(row):
    return ALIASES.get(row["id"], row["fluxo"])


def continuation_text(destination):
    return destination.replace("; ", ", ")


def checklist_text(items):
    return "; ".join(items)


def build_inicio(rid, normal_text):
    checks = checklist_text(first_items(normal_text, 4))
    return f"{STARTS[rid]} Checagens deste fluxo: {checks}."


def build_meio(mode, action, normal_text, exception_text):
    normal = as_sentence(normal_text)
    exceptions = as_sentence(exception_text)
    if mode == "Autonomo":
        resolve = (
            f"Trabalho do agente: {action}. Conclui sem fila humana se: {normal}."
        )
        calls = (
            f"Para e cria pendencia para a equipe se: {exceptions}."
        )
    elif mode == "Autonomo com excecoes":
        resolve = (
            f"Trabalho do agente: {action}. Segue sem equipe se: {normal}."
        )
        calls = (
            f"Chama a equipe se: {exceptions}."
        )
    elif mode == "Autonomo com aprovacao":
        resolve = (
            f"Pedido de aprovacao: {action}. O pedido mostra dados, impacto e proximo passo usando: {normal}."
        )
        calls = (
            f"Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: {exceptions}."
        )
    elif mode == "Copiloto":
        resolve = (
            f"Sugestao do copiloto: {action}. A sugestao usa: {normal}."
        )
        calls = (
            f"A equipe aceita, edita ou ignora. Vira pendencia se: {exceptions}."
        )
    else:
        resolve = (
            f"Tarefa manual: {action}. A tarefa mostra: {normal}."
        )
        calls = (
            f"A execucao fica com a equipe. A tarefa ganha alerta se: {exceptions}."
        )
    return resolve, calls


def build_fim(mode, action, destination, fallback):
    destination = continuation_text(destination)
    if mode == "Autonomo":
        return (
            f"Quando tudo passa pelos limites publicados, a Taliya conclui `{action}`, salva o registro no CRM e grava auditoria. "
            f"Depois, o proximo passo fica em {destination}; dali, a rotina ou fila responsavel continua com as proprias regras. Se nao conseguir concluir, {fallback}"
        )
    if mode == "Autonomo com excecoes":
        return (
            f"Se nao precisar chamar a equipe, a Taliya conclui `{action}`, salva o registro no CRM e grava auditoria. "
            f"Depois, o proximo passo fica em {destination}; dali, a rotina ou fila responsavel continua com as proprias regras. Se sair dos limites, {fallback}"
        )
    if mode == "Autonomo com aprovacao":
        return (
            f"O fluxo termina quando a aprovacao e aceita, recusada ou vence. Se for aceita, a Taliya aplica a acao aprovada, salva o registro no CRM e grava auditoria. "
            f"Se for recusada ou vencer, {fallback} O proximo passo fica em {destination}; dali, a rotina ou fila responsavel continua com as proprias regras."
        )
    if mode == "Copiloto":
        return (
            f"O fluxo termina quando a equipe aceita, edita ou descarta a sugestao. Se aceitar, a acao de `{action}` fica registrada no CRM com auditoria. "
            f"Se precisar continuar depois, o proximo passo fica em {destination}; dali, a rotina ou fila responsavel continua com as proprias regras. Se a Taliya nao conseguir sugerir com seguranca, {fallback}"
        )
    return (
        f"O fluxo termina quando a equipe executa ou encerra a tarefa. A Taliya salva o status, o motivo e a auditoria no CRM. "
        f"O proximo passo fica em {destination}; dali, a rotina ou fila responsavel continua com as proprias regras. Se faltarem dados para a equipe agir, {fallback}"
    )


def build():
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    details = {row["id"]: row for row in csv.DictReader(DETAIL.open(encoding="utf-8"))}
    fields = [
        "id", "agente", "rotina", "fluxo", "titulo_ui", "modo_padrao", "teto",
        "objetivo", "inicio", "meio_resolve", "meio_chama_equipe", "fim",
        "ajustes_do_studio", "requisitos_readonly", "encadeamento", "simulacao",
    ]
    out_rows = []
    for row in rows:
        rid = row["id"]
        action, normal_text, exception_text = RULES[rid]
        detail = details[rid]
        title = display_flow(row)
        resolves = normal_text
        calls = exception_text
        mode = row["modo_padrao_pagina"]
        inicio = build_inicio(rid, normal_text)
        meio_resolve, meio_chama = build_meio(mode, action, resolves, calls)
        fim = ENDINGS[rid]
        out_rows.append({
            "id": rid,
            "agente": row["agente"],
            "rotina": row["rotina"],
            "fluxo": row["fluxo"],
            "titulo_ui": title,
            "modo_padrao": mode,
            "teto": row["teto"],
            "objetivo": action,
            "inicio": inicio,
            "meio_resolve": meio_resolve,
            "meio_chama_equipe": meio_chama,
            "fim": fim,
            "ajustes_do_studio": row["ajustes_do_studio"],
            "requisitos_readonly": row["requisitos_fixos"],
            "encadeamento": row["onde_continua"],
            "simulacao": row["simulacao_obrigatoria"],
        })

    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    write_review(out_rows)
    print(f"wrote {OUT} rows={len(out_rows)}")
    print(f"wrote {REVIEW}")


def write_review(rows):
    lines = [
        "# Taliya CRM - 96 Fluxos Detalhados",
        "",
        "Status: auditoria semantica completa v0.3.",
        "Data: 2026-05-22.",
        "",
        "Este documento detalha os 96 fluxos no padrao completo definido para `Falta com aviso`.",
        "",
        "Cada fluxo tem objetivo, Inicio, Meio, Fim, ajustes, requisitos, encadeamento e simulacao.",
        "",
        "A revisao v0.3 ajusta Inicio/Meio/Fim para o modo padrao real de cada fluxo e remove finais genericos:",
        "",
        "- Autonomo conclui sozinho dentro dos limites e para quando nao consegue concluir.",
        "- Autonomo com excecoes resolve sozinho o caso valido e chama a equipe quando sai dos limites.",
        "- Autonomo com aprovacao monta pedido, mostra impacto e so aplica depois da aprovacao.",
        "- O Fim descreve o resultado real daquele fluxo e o que acontece quando ele nao fecha.",
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
            f"#### {row['titulo_ui']}",
            "",
            f"- ID interno: `{row['id']}`.",
            f"- Nome canonico: `{row['fluxo']}`.",
            f"- Modo padrao: `{row['modo_padrao']}`.",
            f"- Teto: `{row['teto']}`.",
            f"- Objetivo: {row['objetivo']}.",
            "",
            "**Inicio**",
            "",
            row["inicio"],
            "",
            "**Meio**",
            "",
            row["meio_resolve"],
            "",
            row["meio_chama_equipe"],
            "",
            "**Fim**",
            "",
            row["fim"],
            "",
            "**Ajustes do studio**",
            "",
        ])
        for item in split_items(row["ajustes_do_studio"]):
            lines.append(f"- {item}.")
        lines.extend(["", "**Requisitos readonly**", ""])
        for item in split_items(row["requisitos_readonly"]):
            lines.append(f"- {item}.")
        lines.extend([
            "",
            "**Encadeamento**",
            "",
            row["encadeamento"],
            "",
            "**Simulacao deve mostrar**",
            "",
            row["simulacao"],
            "",
        ])

    REVIEW.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
