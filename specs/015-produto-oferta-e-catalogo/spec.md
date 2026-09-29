# 015 — Fonte única de produto, oferta, billing e materiais

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Produto + frontend/backend.
**Dependências:** 013, 014.

## Resultado
Construir o billing Asaas ausente sobre identidade/negócio existentes e fazer landing, agente e materiais descreverem o mesmo produto e a mesma oferta vigente. A correção de escopo está em `../../docs/taliya-sdd/DECISAO_BILLING_2026-09-29.md`.

## Requisitos verificáveis
### R015-01
Criar catálogo versionado de capacidades publicadas, limites e FAQ.

**Aceite:** Somente recursos confirmados entram; equipes/booking e outros recursos antigos não são presumidos por aparecer em documento histórico.
**Verificação:** C015-01.

### R015-02
Publicar uma oferta versionada no novo backend de billing e consumi-la por contrato central, sem preço duplicado no prompt.

**Aceite:** Mensal/anual, cobrança inicial e garantia de 14 dias são coerentes; nenhum teste sem cartão é vendido.
**Verificação:** C015-02.

### R015-03
Catalogar mídia com aprovação, origem e classificação de prova social.

**Aceite:** Cada material publicado possui ID, tipo, URL autorizada, versão, resumo/transcrição, direitos e status; UGC encenado não vira depoimento.
**Verificação:** C015-03.

### R015-04
Definir comportamento quando informações ou materiais faltam.

**Aceite:** A informação ausente é explicitada; o agente não inventa preço, link, prazo ou mídia e o CTA depende de destino válido.
**Verificação:** C015-04.

### R015-05
Versionar e propagar atualizações.

**Aceite:** Oferta nova é consultada no momento relevante; material retirado não é emitido em sessão antiga; compatibilidade e freshness ficam registradas.
**Verificação:** C015-05.

### R015-06
Implementar contratação direta autenticada com cartão recorrente e Pix Automático mensal/anual, sem depender da IA.

**Aceite:** Preço/versão vêm do servidor; identidade e negócio são verificados; tentativas repetidas não criam cobrança duplicada; cartão usa checkout hospedado e Pix usa autorização específica, ambos com cobrança inicial conforme a oferta aprovada. Conta/eligibilidade Asaas são homologadas antes de ativar.
**Verificação:** C015-06.

### R015-07
Processar eventos financeiros de forma autenticada, idempotente e recuperável, projetando acesso somente após confirmação do backend.

**Aceite:** Webhook persiste `event.id` antes do aceite; replay/fora de ordem não duplicam efeito; retorno do navegador ou fala da IA não liberam acesso; pagamento inicial Pix e autorização recorrente são estados independentes.
**Verificação:** C015-07.

### R015-08
Permitir gestão e reconciliação de assinatura, cancelamento e garantia de 14 dias com estados explícitos.

**Aceite:** Solicitação de reembolso não é confirmação; timeout após efeito externo é reconciliado antes de repetir; renovação/falha/cancelamento preservam acesso conforme fatos pagos e política aprovada, com testes sandbox antes da publicação.
**Verificação:** C015-08.

## Limites
Não reconstruir app/Auth, não implantar/ativar cobrança sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Construir billing no backend existente e preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints publicados, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
