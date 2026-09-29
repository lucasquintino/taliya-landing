# 019 — Vídeos, demonstrações e UGCs na experiência

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Conteúdo + frontend.
**Dependências:** 015.

## Resultado
Integrar a biblioteca aprovada à landing e ao agente com reprodução e medição coerentes.

## Requisitos verificáveis
### R019-01
Publicar um conjunto inicial útil sem inventar material pronto.

**Aceite:** Catálogo entregue contém explicação geral, demonstrações prioritárias reais e UGCs aprovados; indisponíveis ficam ocultos.
**Verificação:** C019-01.

### R019-02
Mostrar no máximo um material por resposta e permitir contratação sem assistir.

**Aceite:** Cards reutilizam o DS; o agente seleciona ID aprovado e o vídeo não cria barreira ao checkout.
**Verificação:** C019-02.

### R019-03
Otimizar carregamento e privacidade do player.

**Aceite:** Thumbnail/lazy load, reprodução voluntária, legendas e alternativa textual; embeds não burlam preferência de cookies.
**Verificação:** C019-03.

### R019-04
Medir recomendação, exposição e reprodução separadamente.

**Aceite:** video_completed exige observação verificável do player; link externo sem telemetria não registra conclusão.
**Verificação:** C019-04.

### R019-05
Manter manutenção operacional simples.

**Aceite:** Autor de conteúdo edita catálogo versionado com revisão; publicação/retirada é auditável; não há CMS/editor novo obrigatório.
**Verificação:** C019-05.

## Limites
Não reconstruir app/billing, não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
