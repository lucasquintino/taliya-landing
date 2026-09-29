# Dependências, estimativa e decisões
## Fontes de entrada operacionais
| Item | Como resolver | Bloqueia |
|---|---|---|
| Commit/repo atual landing/Internal | Ler árvore e contratos, comparar ao ZIP; verificar implantação que atende as rotas | Final da 013/020 |
| Interfaces reais de app/billing | Ler código/docs e exemplos de homologação já existentes | Ferramentas de navegação/contexto e regressão financeira |
| Conta OpenAI habilitada | Smoke test autorizado sem publicar; nunca pedir chave em texto aberto | Encerramento 016 |
| Projeto PostHog/permissões/orçamento | Usar conta existente; conferir plano/addons/região; homologação isolada | Encerramento 021/022 |
| Mídia aprovada | Inventário + links/arquivos reais + direitos | Publicação do respectivo material |
| Oferta/políticas vigentes | Fonte do billing e revisão responsável | Preço/garantia e envio público |
| Operador e canal | Login de staff, treinamento e destino de contato | Atendimento humano e release |

Tratar bloqueios de forma localizada. Nenhuma ausência justifica reconstruir app/assinatura já prontos ou fabricar URL. Se fontes acessíveis resolvem a ambiguidade, ler antes de perguntar.

## Estimativa de planejamento
Somatório dos recortes: 27–46 dias de engenharia focada. Referência: um desenvolvedor experiente com ferramentas de IA e revisão de produto/QA; não inclui produção de mídia, espera de credenciais, filas de aprovação ou retrabalho substancial no produto existente. Calendário orientativo: cerca de 6–10 semanas em execução majoritariamente sequencial, a reestimar após 013. Paralelismo bem controlado pode reduzir duração, não elimina trabalho ou gates.

Não há evidência para prometer que um agente de programação fará tudo em uma sessão ou que o custo será exatamente o somatório mínimo. O caminho crítico passa por contratos → identidade/fontes → runtime → ciclo comercial → experiência → medição → homologação → release.

## Decisões já fechadas pelo usuário
Agents API; Luna/max; simplicidade; app e assinatura prontos; integração de leads/clientes; PostHog + Internal mínimo; SDD/Spec Kit; materiais explicativos/demos/UGC; preservação de arquitetura/visual.

## Defaults propostos neste pacote
Um agente, cinco tools, um material por resposta; sem Group Analytics/replay amplo inicialmente; sem CMS/CRM/BI novos; duas áreas Internal; três automações controladas; confirmação financeira no billing; gates e metas conforme 06/07. Esses defaults evitam perguntas sobre detalhes reversíveis. Mudanças que afetem produto, gasto ou segurança exigem registro, não decisão silenciosa do implementador.

## Propostas que exigem ratificação operacional antes de ativar
Teto PostHog; verba de testes reais de IA; retenção e base legal de cada finalidade; textos/cadência de campanhas; janelas de medição; SLA de atendimento humano; aprovação de publicação. Não são impedimentos para preparar código/testes em homologação.

## Supersessão
E00–E04 anteriores deixam de ser o roteiro principal destas frentes; a matriz 013–025 distribui o trabalho. Copy-only segue válido para preservação visual, não para proibir as integrações explicitamente solicitadas agora. App pronto prevalece sobre pré-lançamento. Garantia com cobrança prevalece sobre trial sem cartão. Pagamento oficial prevalece sobre mark_won/mensagem do usuário. O PostHog não substitui fonte transacional.
