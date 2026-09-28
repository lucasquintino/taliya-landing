# Auditoria Multi-Visao Do Produto - Taliya CRM Web/App

> Status: auditoria exploratoria. Versao PT-BR do resumo consolidado em `multi-view-product-audit.md`.

## Veredito Executivo

Estamos no caminho certo.

A direcao atual e coerente:

```text
CRM operacional para studios de Pilates
+ agentes de IA integrados ao sistema
+ WhatsApp como um canal de execucao
+ caminhos manual, copiloto e autonomo
+ nucleo programatico antes de IA
```

Mas o mapa ainda nao e final.

O problema principal agora nao e falta de ideias. O problema e **organizar as decisoes**:

- casos candidatos precisam de status de decisao;
- cada caso precisa dizer se vira tela, botao, painel lateral, alerta, configuracao ou acao automatica;
- fluxos sensiveis precisam de travas claras;
- mobile precisa de limites mais claros;
- alguns assuntos importantes ainda nao aparecem como objetos claros do produto;
- algumas telas talvez sejam melhor como filtros, abas ou paineis dentro de outra tela;
- itens aceitos, opcionais e itens que talvez devam ser juntados ainda estao misturados.

## O Que Manter

- Produto como CRM operacional com agentes integrados.
- WhatsApp como canal, nao como produto inteiro.
- Base com 0 agentes exigindo caminho manual real.
- 96 fluxos candidatos de agentes como base de trabalho.
- 157 casos candidatos como universo atual de mapeamento.
- Regra: primeiro sistema/regras/dados; IA entra para linguagem, ambiguidade, explicacao, resumo e recomendacao.
- UX por botoes contextuais, assistente lateral, aprovacoes e gatilhos automaticos.

## O Que Adicionar

- Colunas novas na tabela mestre: prioridade, decisao, tipo de rota, risco, profundidade mobile, objeto primario, objetos relacionados e fluxos de agente.
- Linhas de jornada para onboarding/setup, qualidade de dados, privacidade/LGPD, incidentes de automacao e politicas.
- Mais visoes separando acoes em massa, LGPD, correcao de duplicidades, aprovacao pelo celular e nova tentativa quando uma integracao falhar.
- Revisao dos principais objetos de negocio: politicas operacionais, pedidos de privacidade, acesso temporario do suporte, segmentos, acordos de pagamento e salas/equipamentos.

## O Que Ajustar

- Tratar 157 como universo candidato, nao escopo final.
- Tratar E14/G13 como casos candidatos aceitos, mas ainda opcionais como fluxos autonomos de agente.
- Financeiro sensivel, historico sensivel e autonomia precisam ser tratados como riscos maximos de seguranca.
- Evitar criar muitas rotas financeiras separadas se um workspace de casos financeiros resolver.
- Separar a area de mudanca de politicas operacionais da area de configuracoes gerais.
- Separar:
  - timeline do aluno;
  - workspace de historico/evolucao.

## O Que Nao Fazer Agora

- Nao trazer B17 como fluxo independente de agente.
- Nao criar botao generico principal de "chamar agente".
- Nao transformar payroll, fornecedores, estoque, impostos e conselho clinico em escopo agora.
- Nao transformar toda rota candidata em item de navegacao principal.

## Maiores Riscos

| Risco | Por que importa |
| --- | --- |
| Travas financeiras | Reembolso, bloqueio, disputa, acordo e cortesia nao podem ser frouxos. |
| Historico sensivel | Professor, financeiro e recepcao nao podem ver dados errados. |
| Autonomia | Agentes nao podem passar por cima de consentimento, cota, risco ou permissao. |
| Politicas | Mudanca de regra afeta automacoes futuras. |
| Mobile amplo demais | App deve focar acao diaria, nao administracao completa. |
| Dados ruins | Setup ruim faz agente parecer quebrado. |

## Proximas Decisoes

1. Recursos/salas/equipamentos viram objetos de primeira classe?
2. Checklists diarios entram como tela, widget do Hoje ou depois?
3. Comunicados/campanhas sao modulo proprio ou acao filtrada em Vendas/Retencao?
4. Excecoes financeiras viram paginas separadas ou um workspace de casos financeiros?
5. Mobile pode executar financeiro ou so revisar/aprovar?
6. Os fluxos opcionais de primeira semana e entrada de dados sensiveis viram agentes proprios ou ficam como casos com trava humana?
7. Quais dos 157 ficam aceitos, juntos, adiados ou fora?

## Proximo Artefato

O mapa mestre v2 ja foi criado. O proximo artefato certo agora e uma rodada de decisao sobre os 157 casos:

```text
aceitar para desenho detalhado / aceitar com profundidade enxuta / juntar / manter como trava
```

Essa rodada deve fechar profundidade de tela, limite de autonomia, papel do celular e prioridade de produto antes de qualquer plano de implementacao.
