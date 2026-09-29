# Auditoria consolidada

2026-09-28 · versão 3.0 · código + pacotes + documentação oficial.


## Escopo e limites
Foram inventariados 2.837 arquivos no ZIP original e 27 no pacote Luna Max. A inspeção aprofundou os caminhos ativos de entrada comercial, runtime, leads, eventos, Internal, configuração e regras SDD. Foram analisados sintaticamente 130 arquivos TypeScript/TSX de app/components/lib/data e 205 arquivos Python do serviço. Nenhum erro sintático foi encontrado nessas verificações. Isso não é build, typecheck, auditoria manual de todas as linhas, pen test nem teste de produção.

Não foram instaladas dependências do projeto, executadas inferências pagas, criados agentes/projetos PostHog, consultadas contas privadas, alterados bancos ou publicados serviços. O código do app completo e da assinatura atual não está neste snapshot. O usuário os considera prontos e essa definição é preservada. O trabalho restante é integrar e verificar, não reiniciar o produto.

As prioridades abaixo indicam riscos para a nova entrega se ainda presentes no commit atual. Não são alegações de incidente ou exploração em produção.

## Achados e tratamento
| ID | Prioridade | Achado | Evidência | Tratamento | Spec |
|---|---|---|---|---|---|
| A01 | P0 | Governança ativa ainda é da migração copy-only. | EV01/EV02 | Proíbe backend e destinos que agora precisam mudar. Atualizar autoridade scoped na 013, sem apagar preservação visual. | 013 |
| A02 | P0 | Internal local usa segredo compartilhado e ator por header. | EV05/EV06 | Token em query/frontend e x-operator-id não formam identidade de staff confiável. Substituir por auth/papéis existentes antes da exposição. | 014/020 |
| A03 | P0 | Núcleo ativo ainda carrega papel e estados de Pilates. | EV10/EV11 | Não trocar apenas texto inicial. Isolar agente v2, fonte e contratos; não migrar prompts históricos como conhecimento. | 015/016 |
| A04 | P0 | Rota atual também grava conversão/lead depois da resposta. | EV07/EV08 | Ferramentas novas somadas ao pós-processamento podem duplicar efeitos. Escolher único dono da escrita e dedup de domínio. | 017 |
| A05 | P1 | Configuração contém Internal remoto e tela local. | EV04/EV06 | Confirmar qual implementação atende a produção; não presumir que corrigir esta cópia corrige o app remoto. | 013/020 |
| A06 | P1 | Transporte comercial espera JSON em chamada com timeout de 60 s. | EV09 | Luna/max e chamadas de ferramenta exigem continuidade independente do browser; reusar fila/worker e recuperar itens. | 016/018 |
| A07 | P1 | DDL é executado ao preparar consulta e há opção TLS sem validação. | EV12 | Migrar schema fora do caminho de request e revisar TLS/CA real. O risco depende do perfil de configuração; não foi explorado. | 014 |
| A08 | P1 | Medição existente é própria e o snapshot não contém PostHog nos caminhos ativos examinados. | EV14/EV17 e varredura app/components/lib/services/app | Instrumentar PostHog explicitamente; ausência aqui não prova ausência no app ou em outro repo. | 021 |
| A09 | P1 | Fallback em memória aparece no registro de eventos quando não há Postgres. | EV17 | Não confirmar persistência comercial em produção com armazenamento transitório; falhar explicitamente e alertar. | 014/021 |
| A10 | P1 | Envio humano examinado é WhatsApp e usa lead.updatedAt na checagem da janela. | EV13 | Provar entrega web; conferir último inbound confiável em vez de atualização genérica da ficha. Validar política do provedor antes de homologar. | 020 |
| A11 | P1 | Contrato anterior permite três asset_ids apesar do objetivo de brevidade. | L2 agent/config.base.json e contracts/reply.schema.json | Novo contrato limita a um material por resposta. IDs e links são resolvidos pelo backend. | 015/019 |
| A12 | P1 | Versão de SDK e scripts Spec Kit são do snapshot, não prova de compatibilidade atual. | EV03/EV15 | Codex skills + scripts PowerShell; validar ambiente Mac/Linux e suporte beta.agents sem atualização indiscriminada. | 013/016 |
| A13 | P1 | Preços de duas gerações e CTA comercial antigo convivem. | EV11/EV18 e fonte de produto | Uma oferta real; assinatura direta não pode virar diagnóstico/lista de espera. Não fixar preço a partir deste snapshot. | 015/018 |
| A14 | P1 | Pacote anterior contém contratos e validação offline, não integração pronta. | L2 evidence/validation-report.json | Os 39 checks históricos não comprovam identidade, billing, handlers, UX, custo ou execução de modelo. Transformar casos em testes reais. | 024 |
| A15 | P1 | Métricas financeiras e estados comerciais exigem fonte oficial distinta de browser/LLM. | L3 e plano anterior | Projetar billing e conferir queries contra registros canônicos. mark_won, retorno de checkout e eventos públicos não são pagamentos. | 017/021/022 |
| A16 | P1 | Franquia PostHog não cobre automaticamente todos os usos/addons e ambientes. | P1/P3/P4/P5 | 1 projeto free; Group Analytics e outros módulos devem ser dimensionados. Teto pode descartar eventos; alertar e conciliar. | 021/022 |
| A17 | P2 | Fontes e mídia precisam de manutenção e retirada após publicação. | L3/L2 | Definir responsável, classificação UGC, captions/transcrição, expiração e pipeline simples de catálogo. | 015/019 |
| A18 | P1 | App e assinatura prontos são premissa do usuário; código completo não veio neste ZIP. | L3/EV16 | Preservar prontidão; mapear contratos reais na 013 sem exigir reconstrução ou afirmar homologação já feita. | 013/024 |

## O que reaproveitar
Widget e design system; adaptadores Next/Python; histórico e storage de leads; filas/outboxes compatíveis; entrada WhatsApp; auth e billing do app prontos; componentes da fila/ficha; estruturas de testes; convenções de Spec Kit. Validar cada reuso no commit atual.

## O que substituir
Papel comercial Pilates; diagnóstico/lista de espera como padrão; oferta duplicada; compilação antiga de conversões no caminho v2; autenticação administrativa por token compartilhado; uso do analytics como autoridade; estados de cliente baseados em texto do modelo.

## Conclusão da auditoria
Há uma base aproveitável, mas a fronteira que precisa mudar é maior que o prompt. A solução deve integrar produto pronto, atendimento, dados e análise sob contratos únicos. O esforço principal está em consistência, autorização, continuidade e prova de operação — não em criar outro CRM ou mais agentes.

As evidências de código com linhas estão em `evidence/CODIGO_VERIFICADO.md`. Achados sem comprovação de runtime continuam condicionais até a 013/024. Este documento substitui a leitura de que o pacote anterior, por existir, representava implementação concluída.
