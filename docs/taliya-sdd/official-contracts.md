# Referências oficiais consultadas — 2026-09-28

- [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna): página
  declara suporte a max. Isso não confirma habilitação da conta na Agents API.
- [Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview) e
  [quickstart](https://developers.openai.com/api/docs/guides/agents-api/quickstart):
  contrato atual foi consultado; sessão/modelo/tools/saída ainda sem smoke remoto.
  Intent JSON continua declarativo. Não adaptar runtime com SDK 2.44.0 por suposição.
- [Spec Kit](https://github.com/github/spec-kit): a instalação local 1.0.7 e seu
  core_pack são a origem rastreada dos scripts Bash. Artifact list revela converge
  no CLI, porém skill converge não estava instalada em .agents/skills.
- [Supabase SSR](https://supabase.com/docs/guides/auth/server-side/creating-a-client):
  validar token no servidor; sessão armazenada por si só não prova identidade.
- [Changelog Supabase](https://supabase.com/changelog.md): consultado por HTTP após
  parser web rejeitar markdown. Não houve upgrade/migração Supabase nesta entrega.

Documentação externa confirma contratos do fornecedor, não integrações do produto.
Contrato Asaas do serviço publicado ainda deve ser fornecido antes de codificar adapter.
