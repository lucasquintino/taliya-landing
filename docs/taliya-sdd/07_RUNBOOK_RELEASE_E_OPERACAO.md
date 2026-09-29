# Runbook de release e operação
## Antes do release
Backup restaurável ensaiado; migrações compatíveis; fontes e URLs reais; responsáveis de operação; auth staff; contrato billing verificado; materiais aprovados; orçamento autorizado; fontes remotas versionadas; checklist segurança/privacidade; casos críticos e build/tipos/lint/testes aprovados. Aprovação explícita para produção registrada.

## Migração
Inventariar leads antigos com product_version e origem. Não converter todos em clientes atuais, não juntar por e-mail declarado e não importar mensagens de sistema antigas. Identificar sessões em andamento; encerrar ou migrar com resumo mínimo autorizado. Fazer dry-run e relatório de contagens antes de escrever. Índices/DDL entram pelo pipeline de migração, não por consulta do visitante.

## Liberação gradual proposta
Interno controlado → 5% das conversas elegíveis → 25% → 100%. Checkout direto nunca fica preso ao percentual do agente. Gate inicial: pelo menos 24 h e 50 turnos monitorados por estágio, sem falha crítica; quando o volume for insuficiente, aguardar ou documentar avaliação controlada adicional, sem rotular sintéticos como tráfego real. Estabilização final proposta de 48 h após atingir 100%, com revisão de dados/custos/incidentes.

Percentual de tráfego não é percentual de trabalho concluído. Qualquer incidente de dados/financeiro/pausa humana interrompe o rollout imediatamente. Erros técnicos >1% num conjunto de pelo menos 100 turnos ou latência acima da meta sustentada exigem investigação; uma única falha crítica já bloqueia, independentemente da amostra.

## Rollback
Desligar geração comercial v2 por flag operacional independente de PostHog; manter ajuda estática, cadastro/assinatura e solicitação humana. Não reativar roteiros de Pilates. Interromper novas sessões/ações não executadas, preservar recibos e reconciliar itens já aceitos. Migrações expand/contract não apagam dados na reversão. Só retornar envio proativo após revalidação de elegibilidade.

## Incidentes
**OpenAI fora:** manter jornada direta, informar indisponibilidade, preservar input aceito e oferecer humano; não confirmar efeito sem recibo.
**PostHog fora/teto:** preservar domínio e outbox onde a política permite; alertar atraso/lacuna. PostHog pode descartar após limite; não alegar replay automático de dados recusados. Conciliar e reingerir somente de forma permitida, deduplicada e documentada. [P1]
**Banco fora:** não aceitar falso cadastro; fail closed nas escritas e status operacional claro.
**Webhook/efeito duvidoso:** consultar autoridade e recibos antes de repetir; não reiniciar compra como primeira tentativa de reparo.
**Humano assume:** pausar entrada/ações/entrega com versão, confirmar solicitação apenas pelo recibo e investigar mensagens tardias.
**Privacidade:** interromper coleta/envio afetado, preservar evidência restrita, acionar responsável e seguir procedimento aprovado; não apagar prova financeira exigida sem revisão.

## Rotina e responsáveis
Operação: fila e pendências diariamente. Responsável de produto/conteúdo: revisar material e fonte ao mudar recurso/preço. Engenharia: fila/erros/latência/custo e versões de dependências. Financeiro/operação: reconciliação de receita/cancelamento/estorno com billing. Analytics: integridade/frescor semanal e alteração controlada de definições. Frequências são proposta operacional a implantar no sistema da equipe, não automações criadas pelo ChatGPT.

## Handoff final
Guia de editar fonte/catálogo; guia da fila/ficha; guia de leitura dos seis painéis; procedimentos de takeover, replay seguro, restauração, rollback e exclusão; donos, permissões e alertas; changelog de decisões; registros de autorização e conclusão de cada spec.
