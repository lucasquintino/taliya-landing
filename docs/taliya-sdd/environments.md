# Ambientes, materiais e dependências — 013

- Landing local: /Users/lucasquintino/Projects/taliya-copiloto-landing, listener 3001;
  cwd do PID confirmado via lsof. Runtime Python 8088 sem listener observado.
- App local de trabalho: /Users/lucasquintino/Downloads/copiloto-github; alterações
  de outra execução preservadas. Não executar reset de banco, build nativo ou pipeline remoto.
- Internal: fonte remota inspecionada em clone read-only; 401 público confirma alcance,
  não identidade de staff, fonte de dados ou SHA ativo. Últimos 3 deploys GitHub falharam.
- GitHub read-only disponível via gh; nenhuma escrita remota executada.
- Credenciais necessárias (somente nomes): DATABASE_URL, TALIYA_AGENT_RUNTIME_URL,
  TALIYA_AGENT_RUNTIME_HMAC_SECRET, OPENAI_API_KEY; projeto/Auth do app, credencial
  staff e contrato billing; PostHog host/projeto/chave/consentimento/orçamento.
  Presença/validade dessas credenciais não foi inferida de .env.example.
- Não ativar PostHog, Agents API, webhooks, mensagens, recursos pagos ou billing.
- Baseline local desktop 1440x1000 e mobile 390x844: evidence/baseline-*.png;
  /pilates termina em /; HTTP 200, sem overflow e sem falhas locais de recursos.
  Requests externos bloqueados no browser da captura. Não é aceite humano de UX.
- Primeiro lançamento Playwright falhou por chromium_headless_shell ausente.
  Captura foi repetida com Chrome instalado, sem instalar browser/dependências.
- Mídia existente: public/illustrations/pilates-studio-loop.mp4/.webm,
  public/agents/mini/*.png, public/diagnosis/*.png, public/avatars/whatsapp/*.png,
  logo SVG e demos em componentes. Hashes no inventário; nenhuma aprovação editorial
  ou direito de UGC presumido. materials.catalog.json continua vazio.

## Bloqueios com dono e condição de saída

| ID | Dependência / dono da resposta | Bloqueia / saída |
|---|---|---|
| B013-01 | Conta Asaas sandbox, elegibilidade Pix Automático, credencial segura e condições comerciais vigentes — responsável do produto/billing | Implementação/homologação 015; não impede documentação local da 013. Nenhuma cobrança ativada sem estes insumos |
| B013-02 | Deploy autoritativo do Internal e staff — responsável de operação | T013-01/06; confirmar SHA ativo e mecanismo real de identidade/config |
| B013-03 | Homologação, contas sintéticas, permissões e orçamento — responsável da plataforma | Consultas integradas/016/021/024; autorização específica, não usar produção |
| B013-04 | Materiais e direitos/editorial — responsável de conteúdo | Publicar catálogo 015/019; fornecer material aprovado |

B013-01 foi inicialmente tratado como busca de serviço publicado. O usuário corrigiu a premissa em 2026-09-29: não existe billing/Asaas e ele será construído. A busca histórica permanece em `evidence/billing-source-search.json`; o novo escopo está em `DECISAO_BILLING_2026-09-29.md`. Trabalho local da 013 continua; 014/015 só são liberadas pelos gates de dependência, não pela existência deste adendo.

Capturas foram atualizadas após esperar 4 s pela animação inicial. Primeira dobra
desktop/mobile foi inspecionada visualmente. Na recaptura, Chrome encerrou mas Node
ficou pendente na limpeza e foi terminado após salvar imagens; métricas JSON vêm
da primeira captura concluída, com os mesmos hashes de aplicação.
