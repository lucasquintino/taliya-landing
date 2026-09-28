# Rodada 1 - Auditoria completa de produto

> Status: primeira rodada de revisao. Este documento consolida o que precisa ser adicionado, ajustado e removido/evitado depois de revisar documentos, fluxos de agentes, casos de uso, telas, cotas, dados e linguagem PT-BR.

## Veredito da rodada

Estamos no caminho certo, mas ainda nao estamos em 100% de decisao de produto.

O desenho atual ja sustenta a tese principal:

```text
CRM operacional completo para studios de Pilates
+ agentes de IA integrados ao CRM
+ WhatsApp como canal, nao como produto inteiro
+ plano Base funcionando com 0 agentes
+ execucao manual, com sugestao do agente ou automatica com limites
```

O maior problema encontrado nesta rodada nao foi falta de ideias. Foi consistencia entre documentos:

- alguns documentos ainda falavam em 91 fluxos como numero principal, enquanto a revisao posterior trabalha com 96 fluxos fortes e 2 opcionais;
- o mapa mestre usa objetos de negocio que ainda nao estavam no modelo de dados principal;
- varias telas candidatas ainda estavam sem decisao de tipo: tela propria, painel, botao, lista filtrada, configuracao ou acao de bastidor;
- alguns casos de alto risco apareciam com possibilidade automatica sem explicar que a automacao, nesses casos, deve ser apenas detectar, alertar, bloquear ou criar caso;
- a versao PT-BR melhorou, mas precisa continuar sendo a camada de leitura de negocio.

## Numeros apos a revisao

| Item | Numero de trabalho | Decisao da rodada |
| --- | ---: | --- |
| Fluxos originais de agentes | 91 | Continuam como base historica. |
| Novos fluxos fortes de agentes | 5 | Manter como candidatos fortes. |
| Fluxos opcionais de agentes | 2 | Manter como opcionais ate detalhar os cards. |
| Fluxos fortes atuais | 96 | Usar como numero principal de trabalho. |
| Fluxos possiveis se os opcionais virarem agentes standalone | 98 | Nao fechar ainda. |
| Casos de uso gerenciais catalogados | 132 | Base boa, mas incompleta. |
| Lacunas candidatas da auditoria | 25 | Manter no universo de revisao. |
| Casos gerenciais em revisao | 157 | Usar como universo candidato, nao escopo final. |

## Audicao 1 - Proposta do produto

| Fazer | Decisao |
| --- | --- |
| Adicionar | Explicitar que Taliya e CRM primeiro, agentes depois. |
| Ajustar | Parar de tratar agentes como modulo separado do produto; eles aparecem dentro de telas, tarefas, aprovacoes, casos e WhatsApp. |
| Remover ou evitar | Evitar "chatbot com agenda" ou "painel de agentes" como narrativa central. |

Resultado: proposta aprovada para continuar.

## Audicao 2 - Fluxos de agentes

| Fazer | Decisao |
| --- | --- |
| Adicionar | C15 entrada multicanal de lead, D15 alteracao efetiva de plano, E13 reclamacao e confianca, F14 incidente de automacao, F15 mudanca de regra operacional. |
| Ajustar | Usar 96 como numero forte de trabalho, nao 91. |
| Ajustar | Manter E14 primeira semana e G13 anamnese/consentimento como casos aceitos, mas ainda opcionais como fluxos de agente independentes. |
| Remover ou evitar | Nao reabrir B17 substituicao de professor como agente standalone nesta formulacao. |

Resultado: catalogo de agentes deve ser lido como 96 fortes + 2 opcionais.

## Audicao 3 - Casos de uso do gestor

| Fazer | Decisao |
| --- | --- |
| Adicionar | Manter os 25 casos candidatos encontrados na auditoria, porque eles representam rotina real de studio. |
| Ajustar | Separar claramente caso de uso, tela e fluxo de agente. Um caso de uso nao precisa virar tela propria nem agente proprio. |
| Ajustar | Marcar casos de alto risco como humano-obrigatorio quando envolver dinheiro, historico sensivel, privacidade, permissao ou reputacao. |
| Remover ou evitar | Nao chamar os 157 de escopo final. Eles sao universo candidato. |

Resultado: 157 continua correto como universo de revisao, mas nao como promessa de MVP fechado.

## Audicao 4 - Telas e rotas

| Fazer | Decisao |
| --- | --- |
| Adicionar | Detalhes para eventos, segmentos, comunicados, checklists, acordos financeiros, estornos/disputas, exportacoes, pedidos de privacidade, acesso do suporte, recursos e professores. |
| Ajustar | Evitar criar muitas paginas financeiras separadas se uma central de casos financeiros com filtros resolver melhor. |
| Ajustar | Separar configuracao de politicas da area de politicas operacionais versionadas. |
| Ajustar | Tratar mobile como execucao, aprovacao e consulta rapida, nao administracao completa. |
| Remover ou evitar | Nao transformar toda rota candidata em item do menu principal. |

Resultado: precisamos classificar cada item como menu principal, detalhe, aba, filtro, painel, botao, relatorio, configuracao ou bastidor.

## Audicao 5 - Modelo de dados

| Fazer | Decisao |
| --- | --- |
| Adicionar | Politica operacional, pedido de privacidade, acesso temporario do suporte, segmento, acordo financeiro, sala/equipamento, checklist e calendario de fechamento/recesso. |
| Ajustar | Alguns nomes do mapa mestre sao visoes ou relatorios, nao entidades reais. Exemplo: "dinheiro na mesa", "gargalo" e "resumo semanal". |
| Ajustar | Alguns casos podem ser tipos de caso operacional, nao tabelas separadas. Exemplo: disputa financeira, comunicado, incidente e arquivo/reativacao. |
| Remover ou evitar | Nao criar uma entidade nova para cada tela, relatorio ou botao. |

Resultado: modelo de dados precisa de um apendice de objetos candidatos antes de virar schema final.

## Audicao 6 - Manual, sugestao do agente e autonomia

| Fazer | Decisao |
| --- | --- |
| Adicionar | Campo ou regra de "autonomia permitida" por caso. |
| Ajustar | Em caso de alto risco, "automatico" deve significar detectar, alertar, bloquear, criar caso ou preparar revisao, nao executar decisao sensivel sozinho. |
| Ajustar | Toda acao externa, cara, financeira, sensivel ou em massa precisa de trava. |
| Remover ou evitar | Evitar que `manual/sugestao/automatico` pareca permissao ampla demais. |

Resultado: a matriz atual esta boa para mapear caminhos, mas precisa de camada de limite de autonomia.

## Audicao 7 - Cotas e economia

| Fazer | Decisao |
| --- | --- |
| Adicionar | Prioridade de economia por fluxo: essencial, media, baixa. |
| Ajustar | Quando a cota acaba, CRM manual continua funcionando. O que para e a automacao paga. |
| Ajustar | Cotas precisam aparecer no contexto do caso, do envio e da execucao do fluxo, nao so em uma pagina de uso. |
| Remover ou evitar | Nao esconder bloqueio de cota como erro generico. |

Resultado: documento de cotas esta coerente, mas precisa conversar melhor com telas/casos.

## Audicao 8 - Mobile

| Fazer | Decisao |
| --- | --- |
| Adicionar | Classificacao: acao completa, revisar/aprovar, consulta rapida, notificacao, computador apenas. |
| Ajustar | Mobile deve cobrir Hoje, Inbox, Agenda, Chamada, Aluno, Professor, Tarefas, Aprovacoes, Financeiro essencial, Reclamacoes, Agentes em alerta e Cotas. |
| Remover ou evitar | Nao colocar configuracao avancada de agentes, politicas complexas, integracoes profundas, campos, exportacoes e relatorios pesados no app mobile v1. O app deve permitir setup guiado e configuracao essencial de agentes. |

Resultado: app mobile deve ser operacional, nao administrativo.

## Audicao 9 - Versoes PT-BR

| Fazer | Decisao |
| --- | --- |
| Adicionar | Glossario de produto e indices que expliquem como ler os documentos. |
| Ajustar | Continuar substituindo codigo e termo tecnico por linguagem de gestor. |
| Remover ou evitar | Evitar que a versao PT-BR vire espelho tecnico da versao oficial. |

Resultado: PT-BR deve ser camada de entendimento e decisao.

## Mudancas que esta rodada deve aplicar

| Documento | Ajuste |
| --- | --- |
| `spec.md` | Atualizar criterio que ainda falava em 91 fluxos como numero principal. |
| `flow-coverage-matrix.md` | Explicar 91 como base historica e adicionar os 5 fluxos fortes + 2 opcionais. |
| `routes-and-surfaces.md` | Adicionar rotas de detalhe que ficaram faltando e marcar risco de agrupamento por casos. |
| `data-model.md` | Adicionar apendice de objetos candidatos e decidir o que e entidade, tipo de caso, job/log ou visao derivada. |
| `README.md` e `README.pt-BR.md` | Linkar esta rodada de auditoria. |
| `screen-inventory-tree.pt-BR.md` | Manter linguagem de negocio e reforcar que nem tudo vira tela. |

## Decisoes que ainda impedem dizer 100%

| Decisao | Por que importa |
| --- | --- |
| Quais dos 157 ficam aceitos, juntados, depois ou fora | Define escopo real. |
| Quais telas entram no menu principal | Evita CRM inchado. |
| Quais casos financeiros viram uma unica central de casos | Evita fragmentacao no financeiro. |
| Se recursos/salas/equipamentos entram como objeto forte | Afeta agenda, capacidade e modelo de dados. |
| Se primeira semana e anamnese viram agentes standalone | Afeta contagem final de 96, 97 ou 98. |
| Qual a permissao exata por papel | Bloqueia historico sensivel, financeiro e suporte. |
| Qual autonomia e permitida por fluxo | Bloqueia agentes antes de seguranca. |

## Conclusao da rodada 1

Esta rodada nao encontrou um motivo para mudar a tese principal.

Ela encontrou pontos concretos para corrigir:

- alinhar 91 versus 96/98 fluxos;
- documentar objetos candidatos;
- adicionar rotas de detalhe faltantes;
- proteger casos de alto risco;
- manter PT-BR como linguagem de produto;
- impedir que tudo vire tela principal.

Proxima rodada recomendada, agora registrada em `rodada-2-classificacao-157.pt-BR.md`:

```text
classificar os 157 casos em aceitar para desenho detalhado / aceitar com profundidade enxuta / juntar / manter como trava
```

Essa e a rodada que mais aproxima o produto de 100% de decisao.
