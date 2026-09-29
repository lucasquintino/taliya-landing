# Testes, metas propostas e evidências
## Níveis
**Estático:** schemas, tipos, lint, build, importações e migrações verificáveis.
**Unidade:** normalização, autorização, patches, dedup, métricas e elegibilidade.
**Contrato:** provedor/Agents API, tools, oferta, identidade, eventos e respostas públicas.
**Integração:** Postgres/fila/outbox, serviço do app/billing, canal e relay PostHog.
**E2E:** journeys no navegador e canal comercial com dados controlados.
**Conversacional real:** Luna/max; perguntas diretas, profissão/atividade, várias mensagens, indecisão, mudança de assunto, limites, fraude e handoff.
**Operação:** backup/restore, rollback, incidentes, orçamento, supressão e exclusão.

## Critérios bloqueantes
Todos os 65 casos da matriz devem ser executados no nível aplicável. Zero falha de autorização, vínculo errado, duplicação financeira, falso sucesso, vazamento, prova social inventada e mensagem tardia após pausa. Casos críticos conversacionais são repetidos pelo menos três vezes com variações; passar uma vez não demonstra invariância. Casos determinísticos têm asserts de banco/recibo, não aprovação subjetiva.

Não classificar um teste como aprovado se o serviço remoto foi substituído por mock e o objetivo era comprovar integração real. Manter grupos offline/sandbox/live separados no relatório.

## Metas de homologação propostas
Não são resultados observados nem promessa de provedor. Ratificar na 013/016 e não afrouxar silenciosamente:
- Aceite durável de mensagem p95 até 1 s no ambiente de teste dimensionado; UI não espera por toda a inferência.
- Resposta final p95 até 20 s para perguntas simples e até 30 s para turnos com ferramentas no conjunto de avaliação. Luna/max permanece. Se não passar, otimizar contexto/IO/fluxo e reavaliar UX; bloquear a liberação ou documentar decisão explícita.
- Pelo menos 95% de respostas úteis e corretas no conjunto não crítico, com rubric e avaliação humana. Sem tolerância percentual para falha crítica.
- Coleta/outbox: nenhuma perda nos testes de recuperação; frescor alvo até 5 min para eventos de produto e até 1 h para snapshots analíticos agendados. Expor last_synced_at e lacunas.
- Fixture financeira: igualdade de contagem de entidades e valores canônicos; tolerância zero para dupla contagem. Valores monetários em centavos, arredondamento somente na exibição.
- Landing: alvo de campo p75 LCP <= 2,5 s, INP <= 200 ms e CLS <= 0,1; laboratório e dispositivo/rede controlados antes do lançamento, sem alegar medição de campo inexistente. [S3]
- Acessibilidade: requisitos aplicáveis de WCAG 2.2 AA, foco/teclado/leitura/legendas testados; auditoria parcial não é certificação completa. [S2]

## Comandos
O snapshot tem `npm run build`, `npm run lint` e scripts de eval antigos em package.json. Confirmar ambiente/runtime suportado e comandos no commit atual. Acrescentar comando explícito de typecheck e suíte v2 no repositório de implementação; este pacote não finge que tais scripts já existem. Python: usar ambiente isolado e versão suportada pelo pyproject; teste atual de produção é ponto de partida, não gate suficiente do agente novo.

## Regressão da assinatura pronta
Executar integração nas quatro combinações mensal/anual × cartão/Pix Automático. Preservar as regras reais já implementadas: não refazer checkout nem inferir lógica a partir de JSON antigo. Verificar associação de conta/negócio, pagamento confirmado, autorização quando aplicável, falha, retomada, duplicação, cancelamento e reembolso. Produção somente com autorização e dados apropriados; sandbox claramente marcado.

## Falhas deliberadas
Banco indisponível; timeout antes/depois da gravação; worker reinicia; stream cai; callback repetido; evento fora de ordem; material retirado; preço muda; humano assume; dois operadores; checkout aberto em duas abas; consentimento revogado; limite PostHog atingido; webhook malformado/falso; billing demora; URL de retorno adulterada. Cada falha precisa de estado visível e caminho de reparo.

## Evidência padrão
Commit/versão, spec/R-ID/caso, ambiente, comando, fixture sanitizada, timestamps, resposta, assert esperado/obtido, artefatos visuais e responsável. Não incluir prompts sensíveis, PII de terceiros, PAN/CVC, chaves ou tokens de sessão. Reportar métricas com tamanho de amostra e limites da conclusão.
