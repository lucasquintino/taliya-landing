# 018 — Landing, widget e integração à assinatura

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Frontend + design/QA.
**Dependências:** 015, 017.

## Resultado
Permitir contratar diretamente ou receber ajuda sem mudar a identidade visual aprovada.

## Requisitos verificáveis
### R018-01
Separar CTA de contratação de CTA de dúvidas.

**Aceite:** Começar agora abre o fluxo existente; tirar dúvidas abre chat. Escolha mensal/anual e contexto permitidos são preservados.
**Verificação:** C018-01.

### R018-02
Preservar design system e composição com ajustes localizados.

**Aceite:** Diferenças desktop/mobile são aprovadas; nenhum redesign geral, substituição de carrosséis/tabs ou reconstrução do app.
**Verificação:** C018-02.

### R018-03
Cobrir todos os estados do atendimento.

**Aceite:** Fechado/aberto/vazio/enviando/esperando/erro/offline/reconectando/humano possuem comportamento testado, sem spinner infinito.
**Verificação:** C018-03.

### R018-04
Manter navegação segura e acessível.

**Aceite:** URLs vêm do backend; teclado, foco, leitura, toque e retorno após login funcionam; tokens não entram em analytics/referrer.
**Verificação:** C018-04.

### R018-05
Alinhar FAQ, oferta, SEO e conteúdo legível.

**Aceite:** Metadados/structured data e rotas não anunciam legado; privadas ficam protegidas e noindex; não há promessa de indexação garantida.
**Verificação:** C018-05.

## Limites
Não reconstruir app/billing, não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
