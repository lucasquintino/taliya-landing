# Setup E Configuracoes - Criterios De Aceite

Status: contrato v0.1.
Data: 2026-05-13.

## Objetivo

Definir quando a arquitetura de setup/configuracoes esta pronta para virar telas, prompts, contratos tecnicos e implementacao.

## Criterio global

O setup esta pronto quando um gestor de studio consegue configurar o CRM sem entender termos tecnicos, e o sistema consegue transformar essa configuracao em regras publicadas, auditaveis e consumidas por CRM/agentes sem conflito.

## Criterios por artefato

| Artefato | Aceite minimo |
|---|---|
| Principios de setup | Deve deixar claro que agente/humano guiam, gestor decide, sistema configura e auditoria registra. |
| Inventario de configuracoes | Cada configuracao precisa ter dono, impacto, decisao MVP e fonte da verdade. |
| Contrato tecnico | Toda regra precisa caber no contrato padrao sem excecao solta. |
| Corte de complexidade | Deve separar obrigatorio, recomendado, default, avancado, pos-MVP e removido. |
| Fonte da verdade | Nenhuma regra pode morar em duas paginas como dona. |
| Precedencia | Todo conflito relevante precisa ter regra vencedora. |
| Consumo pelo CRM/agentes | CRM/agentes leem configuracao publicada ou snapshot, nunca rascunho solto. |
| Perguntas do setup | Toda pergunta precisa mapear para configuracao real ou ser removida. |
| Arvore adaptativa | Precisa cobrir 0/1/3/7 agentes, canal ausente, financeiro incompleto e regras sensiveis. |
| Matriz de impacto | Toda configuracao critica aponta paginas, agentes, fluxos, cotas, permissoes e auditoria afetados. |
| Publicacao parcial | Deve ativar CRM seguro mesmo quando agentes/autonomia ficam pendentes. |
| Reconfiguracao | Toda mudanca pos-go-live precisa de diff, simulacao, publicacao e rollback quando aplicavel. |
| Testes de conflito | Devem cobrir privacidade, permissao, plano, cota, politica, dado, integracao e acao sensivel. |
| Cenarios reais | Devem simular 0, 1, 3, 7 agentes e modelos de cobranca/consumo diferentes. |
| Blueprint de telas | Deve mostrar como o usuario configura sem expor complexidade tecnica. |
| Plano de imagens | Deve gerar apenas imagens necessarias, sem duplicar rotas herdadas. |

## Criterios de simplicidade para o gestor

O setup nao esta pronto se:

- usa termos como "entitlement", "policy engine" ou "snapshot" na interface final;
- pede uma pergunta que o sistema poderia inferir com default seguro;
- mostra o inventario completo de configuracoes para o cliente;
- deixa o cliente navegar livremente por todas as areas configuraveis antes do go-live;
- transforma o onboarding em um hub de Configuracoes do CRM;
- obriga configurar agentes para usar CRM;
- exige entender todos os fluxos antes de publicar algo;
- chama rotinas operacionais de "fluxos" na interface do setup;
- mostra "politicas" como termo principal quando o gestor deveria ver regras de seguranca, aprovacoes ou excecoes;
- chama previa de impacto de simulacao no onboarding;
- mistura financeiro do studio com billing Taliya;
- mistura modelo de cobranca com consumo de aula sem explicar impacto;
- mostra modo autonomo antes de explicar risco e fallback.

O Setup Inicial esta no escopo certo quando:

- pergunta apenas o necessario para operar no primeiro dia;
- usa defaults para o que pode ser decidido com seguranca pelo sistema;
- transforma ajustes nao essenciais em pendencias rastreaveis;
- manda configuracoes profundas para pos-go-live;
- permite que o CRM opere manualmente mesmo sem agente;
- prepara agentes sem abrir configuracao profunda de fluxo.

## Criterios de seguranca

O setup inicial nao deve configurar profundamente nem publicar autonomia de fluxo. Ele pode apenas preparar agentes e rascunhos/pendencias de fluxos recomendados.

A configuracao pos-go-live em Agentes/Fluxos so pode publicar autonomia quando:

1. plano permite;
2. cota permite;
3. permissao existe;
4. regra de seguranca/politica foi publicada;
5. canal esta conectado;
6. modelo de mensagem esta aprovado quando aplicavel;
7. fallback humano esta definido;
8. auditoria esta ativa;
9. simulacao/preflight passou;
10. gestor aprovou.

## Criterios para 0 agentes

O plano Base com 0 agentes precisa sair do setup com:

- CRM manual ativo;
- agenda funcionando;
- alunos funcionando;
- financeiro funcionando;
- tarefas/checklists/aprovacoes funcionando;
- configuracoes basicas publicadas;
- agentes claramente indisponiveis por plano;
- nenhum fluxo essencial bloqueado por falta de IA.

## Criterios para imagens/telas

As telas de onboarding devem deixar claro `pronto agora` versus `configurar depois` quando isso ajuda a decisao do usuario, especialmente em agentes, painel de impacto e revisao/publicacao. Nao deve existir banner repetitivo explicando que o setup e inicial em toda tela.

Toda pendencia de pos-go-live exibida na revisao deve ser rastreavel, com responsavel, motivo, destino e status.

Uma imagem nova so e necessaria quando:

- a rota tem layout proprio;
- o estado muda muito a decisao do usuario;
- existe abaixo da dobra realmente relevante;
- o drawer/painel muda o tipo de acao;
- a rota nao consegue herdar padrao aprovado.

Se a rota herda lista + filtros + drawer, ou kanban + drawer, deve ser documentada sem imagem nova sempre que possivel.

## Criterios de fechamento

Esta rodada fica fechada quando:

- nao houver duplicidade consciente de fonte da verdade;
- cada risco tiver bloqueio, fallback ou aprovacao;
- setup guiado por agente e chamada humana opcional estiverem coerentes;
- os documentos novos estiverem linkados no indice;
- as decisoes abertas forem apenas defaults/presets finos, nao arquitetura central.
