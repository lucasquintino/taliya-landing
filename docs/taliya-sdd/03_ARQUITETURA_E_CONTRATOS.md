# Arquitetura e contratos da integração
## 1. Fronteira estável
Manter widget → API Next → runtime Python quando esse continuar sendo o caminho real. A API gerenciada não exige trocar a linguagem. Introduzir uma implementação v2 atrás de um contrato comercial interno, sem subir um segundo serviço por conveniência. O SDK/REST concreto é fixado após smoke test e tipos verificados. [O2/O4]

Entrada pública proposta: texto do usuário, ID de mensagem do cliente para dedup, contexto visual não autoritativo e sessão opaca emitida pelo servidor. O backend reconstrói a identidade, a conversa original e o contexto de negócio autorizado. Não aceitar histórico arbitrário do browser como mensagens do sistema ou recibos de ferramentas.

Fluxo: autenticar/limitar → persistir entrada → enfileirar → executar Luna/max → validar ferramenta → gravar efeito/recibo/outbox → devolver resultado → validar resposta pública → persistir entrega → canal. Operações atravessando bancos usam eventos e reconciliação; não prometer atomicidade distribuída.

## 2. Configuração e saída
Um agente por versão/ambiente; uma sessão remota por conversa autorizada. Sem shell, web search de produção, MCP amplo, plugins genéricos ou subagentes. A configuração declarativa está em `agent/config.intent.json`; ela não é apresentada como request homologado. [O1/O2]

Formato público: até duas mensagens curtas, até um `asset_id`, até duas referências de ação. O backend resolve o ID da mídia/ação e cria o link seguro. Nenhum campo URL livre, status pago, papel de usuário ou pontuação financeira é aceito da IA. O schema anterior com até três mídias foi restringido.

## 3. Cinco ferramentas
| Função | Entrada do modelo | Contexto somente do servidor | Resultado |
|---|---|---|---|
| consultar_taliya | tópico/pergunta | fonte atual/versionamento | fatos públicos + versão + frescor |
| buscar_material | assunto/formato/contexto declarado | catálogo aprovado | IDs autorizados + resumo/classificação |
| atualizar_contato | campos allowlist + message_id original | contato/autorizações/versão | recibo da alteração aplicada ou erro |
| preparar_proximo_passo | destino e periodicidade | identidade/negócio/acesso | referência de navegação válida |
| solicitar_atendimento_humano | motivo + evidência | conversa/operador/estado | recibo único + pausa confirmada |

Os schemas reaproveitados estão em `contracts/tools.json`; a 016 deve validar sua aceitação no contrato atual da API. Código de função não é criado ao cadastrar uma ferramenta no painel. Pending calls vêm de `required_actions`; salvar resultado antes de devolvê-lo e recuperar após falha. [O4]

## 4. Dados e donos das escritas
Entidades lógicas, não ordem para criar tabelas novas: sessão de conversa, mensagem, contato comercial, vínculo pessoa-contato, negócio, assinatura, projeção de cliente, recibo de ferramenta, solicitação humana, preferência/consentimento, catálogo, evento/outbox. Primeiro mapear equivalentes existentes.

O cadastro de clientes de cada prestador dentro do app não é o CRM da Taliya. Não expor esses dados ao agente comercial. Um contato declarado pode existir sem conta; uma pessoa pode pertencer a vários negócios; uma assinatura pertence ao escopo definido no billing. Usuários membros não multiplicam clientes pagantes.

Estado separado:
- Aquisição: prospect/lead identificado/cadastro/checkout iniciado/cliente convertido, com marcos históricos; adotar nomes reais do domínio.
- Billing: estado oficial da assinatura/pagamentos/reembolso.
- Acesso: estado oficial e período válido.
- Atendimento: IA ativa/aguardando humano/humano ativo/encerrado.

Cancelar renovação não apaga período pago. Estorno solicitado não é estorno concluído. Não implementar o antigo `mark_won` como acesso pago; no novo painel removê-lo ou renomeá-lo estritamente como anotação comercial sem impacto financeiro.

## 5. Idempotência e ordenação
Distinguir ID de mensagem do canal, ID do request, ID de turn/call e chave do efeito de domínio. Uma repetição pode ter call_id novo e ainda representar o mesmo efeito; basear dedup em conversa + mensagem original + operação + alvo/versão. Atualizações concorrentes usam versão/revisão. Limitar ordenação por conversa, não serializar o SaaS inteiro.

Pausa humana incrementa versão de atendimento. Antes de cada escrita de ferramenta e entrega, verificar se a versão ainda permite a operação. Transação grava solicitação/pausa/recibo/outbox juntas quando pertencem ao mesmo banco. Confirmação determinística do handoff é única e permitida por seu recibo, não uma brecha para liberar texto tardio.

## 6. Contratos do produto pronto a mapear na 013
Para cada um: método/rota real, auth, IDs, request/response, códigos de erro, idempotência, versão e dono. Precisamos de identidade/membership; oferta pública; iniciar/retomar contratação; status de assinatura/acesso; gestão autenticada; eventos de primeira confirmação/renovação/falha/cancelamento/reembolso; primeira operação útil do app. Não inventar REST paths apenas para preencher o documento.

## 7. Operação e caches
Oferta: consultar fonte vigente ao responder preço/garantia/contratar. Catalogo: cache versionado e invalidável; retirar conteúdo durante sessão deve surtir efeito. Contexto privado mínimo é buscado server-side após login, não exposto na ferramenta pública.

Mudança de prompt/ferramenta cria versão; sessões existentes não herdam tudo automaticamente. Política: concluir/pausar turno seguro, criar sessão nova com resumo mínimo autorizado e registrar vínculo; não transportar instruções históricas ou promessas antigas. [O3]

## 8. Segurança
Sessão HttpOnly/Secure/SameSite apropriada ou mecanismo equivalente do app; CSRF/origin nas mutações; JWT validado e RBAC; IDs opacos não são autorização. Rate limits distribuídos e antiabuso antes de chamadas caras; limites de tamanho/tempo/custo. URLs allowlist contra SSRF/redirecionamento aberto. Renderização saneada contra XSS. Segredos somente no servidor.

Revisar particularmente EV05/EV06 (token compartilhado), EV12 (DDL/TLS), histórico do cliente em EV09 e cadeia de permissões em rewrites. Nenhuma credencial em URL, log, transcrição ou evento. Reusar mecanismos prontos antes de adicionar serviços.

## 9. Integração com canais
Web e WhatsApp comercial compartilham política do agente, não identidade automaticamente. Vincular canais apenas com verificação. No WhatsApp, auditar autenticação de webhooks, idempotência, ordenação, timestamp real da última mensagem do usuário e permissões/templates do provedor atual. Não usar uma atualização administrativa da ficha como prova de janela de conversa aberta. Mídia de saída pode ser link/card permitido; não acrescentar voz/computer use como dependência desta entrega.

## 10. Falhas e entrega
Evitar manter browser esperando execução longa como única garantia. Retorno rápido de aceite persistido + polling/SSE de status, conforme canal. Streams da OpenAI não reexecutam eventos perdidos; conciliar itens salvos por IDs. [O5]

Se o provedor demora, mostrar estado de processamento e oferecer ações estáticas. Mensagem de fallback não inventa sucesso. Falha de PostHog não impede a compra; falha do billing não é substituída por estimativa da IA. Kill switches específicos: geração, escrita assistida, envio proativo, ingestão analítica; checkout não depende deles.
