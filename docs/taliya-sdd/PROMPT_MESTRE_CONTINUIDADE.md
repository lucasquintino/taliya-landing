# Prompt de continuidade — implementar Taliya com SDD/Spec Kit
Você está trabalhando no código atual da Taliya, não criando um produto novo. Leia `00_COMECE_AQUI.md`, a auditoria, o plano mestre e a governança deste pacote v3.0. Compare o commit real ao ZIP de referência e registre as diferenças antes de alterar arquivos.

## Direção obrigatória
App e assinatura já prontos: reutilizar. Novo atendimento comercial na Agents API, `gpt-6-luna` com esforço `max`, um agente, ambiente none, sem subagentes. Cinco ferramentas do backend. Landing e design system preservados. Catálogo de mídia compartilhado. Contato/conta/negócio/assinatura vinculados sem duplicação. PostHog para métricas; Internal com fila e ficha para operação. Sem novo billing/auth/CRM/BI/CMS. Oferta atual com cobrança na contratação e garantia de 14 dias; não anunciar teste sem cobrança.

## Comece exatamente assim
1. Confirme árvore/commit e alterações locais; não sobrescreva trabalho existente.
2. Leia AGENTS.md, constituição e ponteiro do Spec Kit. O snapshot continha regras copy-only e pointer antigo; crie adendo scoped e faça a seleção correta da feature, preservando histórico/visuais.
3. Verifique versão/integração de Spec Kit, scripts disponíveis e forma de invocação Codex. Não execute init --force sem backup/diff nem invente converge numa versão que não possui esse comando.
4. Verifique numeração; use 013–025 somente se ainda livres. Comece por 013-fundacao-e-contratos, mapeando interfaces reais do app/billing/Internal, fontes de produto, mídia e ambientes.
5. Para cada spec: specify → clarify quando necessário → plan → checklist → tasks → analyze → implement → converge/revisão equivalente → evidência. Testes são parte das tarefas; requisitos críticos não podem ser rebaixados para fechar a spec.

## Cuidados comprovados no ZIP
Token compartilhado em query/frontend do Internal; ator por x-operator-id; pós-processamento de conversão que pode duplicar tools; caminhos SDK/knowledge ainda Pilates; request síncrono 60s; after() sem garantia durável; DDL em request; opção TLS sem validação; eventos em memória; Internal remoto e local; controle de janela WhatsApp baseado em updatedAt; contrato de mídia anterior com até três IDs. Consulte as evidências e confirme no código atual antes de corrigir.

## Execução
Implemente uma spec/slice por vez, com diff revisável e commit quando autorizado no ambiente. Faça tarefas independentes em paralelo sem disputar o mesmo arquivo. Cada requisito precisa de teste e evidência, não apenas arquivo criado. Se um contrato ou acesso está ausente, busque nas fontes disponíveis; peça somente o que continuar irresolúvel, bloqueando apenas a tarefa dependente.

Não criar recursos pagos, fazer deploy, alterar DNS, disparar mensagens reais, cancelar/estornar assinaturas ou migrar produção sem gate explícito. Homologações reais de API também exigem acesso/orçamento autorizado; nunca peça segredo exposto em texto.

## Ao terminar cada sessão
Registre spec, commit, R-IDs atendidos, tarefas pendentes, testes executados e resultados, decisões, bloqueios e próxima ação exata. Atualize verification/status. Não confunda checks offline com inferência real. Não declare 100% antes dos gates G0–G6 e da operação estabilizada.
