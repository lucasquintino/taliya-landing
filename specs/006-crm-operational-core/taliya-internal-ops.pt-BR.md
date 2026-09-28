# Operacao interna da Taliya - PT-BR

> Status: historico/base. Para o contrato completo do backoffice interno, usar `taliya-internal-backoffice-contract.pt-BR.md`.

## Regra central

Suporte Taliya nao e usuario normal do studio. Todo acesso a conta de cliente precisa ser autorizado, escopado, temporario e auditado.

## Superficies internas

| Superficie | Papel |
| --- | --- |
| `/internal` | Visao operacional interna da Taliya. |
| `/internal/leads` | Leads comerciais da propria Taliya. Nao e inbox dos studios pagantes. |
| `/internal/sales-inbox` | Alias/legado para leads comerciais da Taliya. |
| `/internal/commercial-metrics` | Metrica/aba comercial da operacao interna. |
| `/internal/tenants` | Clientes/studios, planos, usuarios, status, grants, incidentes, billing e entitlements. |
| `/internal/support` | Tickets internos vindos de `/app/suporte`. |
| `/internal/support/grants` | Grants temporarios autorizados pelos studios. |
| `/internal/incidents` | Incidentes tecnicos e operacionais da plataforma Taliya. |
| `/internal/billing` | Assinaturas, faturas, planos, add-ons e entitlements. |
| CRM do studio `/app/*` | Produto vendido ao studio; suporte entra apenas com grant. |

## Objetos internos

| Objeto | Uso |
| --- | --- |
| Tenant | Conta do studio. |
| Entitlement | Plano, agentes incluidos, cota, add-ons. |
| Incidente tecnico | Falha de sistema, integracao ou runtime. |
| SupportAccessGrant | Acesso temporario autorizado pelo studio. |
| SupportAction | Acao feita por suporte dentro do escopo. |
| BillingEvent | Status de assinatura/fatura/add-on. |

## Acesso de suporte

```text
studio solicita/autoriza
  -> define escopo
  -> define prazo
  -> suporte acessa
  -> cada acao audita
  -> acesso expira ou e revogado
```

Escopos possiveis:

- diagnostico de integracao;
- revisao de importacao;
- investigacao de incidente de agente;
- suporte de billing;
- suporte de configuracao;
- acesso somente leitura.

## Limites

Suporte Taliya nao pode:

- alterar financeiro do aluno sem aprovacao explicita;
- enviar mensagem externa como studio sem autorizacao;
- baixar/exportar dados sensiveis sem motivo e auditoria;
- ver historico sensivel fora do escopo;
- manter acesso permanente;
- usar conta de cliente para teste nao autorizado.

## O que o studio deve ver

- acesso ativo;
- quem/qual time Taliya esta acessando;
- motivo;
- escopo;
- prazo;
- acoes feitas;
- botao revogar;
- auditoria.

## Aceite

Qualquer plano de telas deve incluir:

- tela de aprovar acesso de suporte;
- estado "suporte ativo";
- auditoria de suporte;
- caminho para revogar;
- separacao clara entre Sales Inbox interno e Inbox do studio.

## Contrato Atual

Este arquivo fica como registro historico da separacao inicial. O escopo completo, as rotas oficiais e a cobertura visual recomendada estao em:

- `taliya-internal-backoffice-contract.pt-BR.md`.
