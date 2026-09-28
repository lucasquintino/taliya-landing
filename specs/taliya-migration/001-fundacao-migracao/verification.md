# Verificação — Fundação da migração Taliya/Copiloto

## Ambiente

- Data: 2026-09-25
- Diretório: `outputs/taliya-copiloto-landing/`
- Base: `c473a440d562acf6d5314cce0701d48ec284fc07`
- Branch local atual: `013-taliya-foundation`
- Spec Kit: CLI 1.0.7; integração Codex/Spec Kit 0.8.3.dev0

## Resultado

| Verificação | Status | Evidência/limite |
|---|---|---|
| Clone tem o commit de origem esperado | Aprovado | `git rev-parse HEAD` retornou o SHA completo registrado. |
| Cópia sem remote configurado | Aprovado | `git remote -v` vazio após remoção do remote do clone. |
| Estrutura atual de rotas/componentes inventariada | Aprovado (estático) | Leitura de `app/page.tsx`, `app/pilates/page.tsx`, `NicheLandingPage.tsx` e arquivos de seção. |
| Pacotes separados da pasta pública | Aprovado (estático) | Cópia em `docs/landing-migration/reference/TALIYA_INICIAR/`. |
| Integridade dos documentos do ZIP | Aprovado | `LC_ALL=C shasum -a 256 -c 07_INTEGRIDADE/SHA256SUMS.txt`: 35 arquivos `OK`. |
| Projeto original intocado | Aprovado por procedimento | As alterações ficaram na cópia independente. A tentativa anterior foi renomeada para `outputs/taliya-copiloto-landing-previous-attempt/` sem ser apagada. Nenhuma escrita foi feita no clone de origem. |
| `npm ci` para preview | Aprovado com aviso | 379 pacotes instalados do lockfile. Node `22.5.1` está abaixo da faixa pedida por `eslint-visitor-keys@5.0.1` (`^22.13.0`); o servidor iniciou apesar do aviso. O install reportou 8 advisories (1 critical); não rodei auditoria nem alterei versão/lockfile. |
| Baseline `/pilates` desktop | Parcialmente aprovado | `http://127.0.0.1:3001/pilates` abriu e renderizou no Codex In-App Browser; título e conteúdo foram observados e uma captura visual foi exibida na conversa. A interface não oferece gravação desse screenshot como arquivo local. |
| Baseline `/pilates` mobile | Pendente | CUA não permite configurar viewport. BrowserAct 1.4.2 não tem browser configurado; sua criação exigiria autorização separada, então não criei/configurei navegador. |
| HTML inicial / status HTTP | Aprovado localmente | Rota respondeu `200` no servidor dev; snapshot de acessibilidade mostrou a composição original. |
| Lint, testes e build | Não testado | Nenhuma mudança de aplicação foi feita nesta etapa. |
| Publicação/deploy | Fora do escopo | Não executados nem autorizados. |

## Próxima etapa

Revisar a Spec 001 e então preparar/implementar a spec 002 de SEO transversal, sem alterar o layout de `/pilates`. O baseline mobile fica registrado como limite; a spec 002 mantém em aberto o destino público das rotas legadas, conforme `route_plan.json`.
