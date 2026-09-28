# Taliya CRM - Mapa Dos Perfis De Configuracao De Agentes/Fluxos

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Objetivo

Mostrar que os 96 fluxos nao exigem 96 configuracoes diferentes.

O produto deve usar poucos perfis reutilizaveis. O dono/admin escolhe preset e pacote; depois ajusta somente campos simples quando precisar.

## Regra De Produto

Cada perfil define:

- o que ja vem fixo;
- o que vem como default;
- o que o studio pode ajustar;
- quais modos aparecem;
- onde a operacao continua quando para.

O perfil nao expoe prompt, ferramenta tecnica, retry interno, modelo de IA, payload, idempotencia ou regra de seguranca.

## Mapa Geral

| Perfil | Nome | Fluxos | Quantidade |
|---|---|---|---:|
| P01 | Conversa segura | A1, A2, A3, A4, A5, A10 | 6 |
| P02 | Identidade e privacidade | A6, A7, A8, A9 | 4 |
| P03 | Presenca e faltas | B1, B2, B3, B14 | 4 |
| P04 | Reposicoes e vagas | B4, B5, B6, B13 | 4 |
| P05 | Agenda estrutural | B8, B9, B10, B11, B16 | 5 |
| P06 | Experimental e primeira aula | B7, B12, B15, C2, C3, C4, C5, C11, C12 | 9 |
| P07 | Captura e qualificacao | C8, C9, C10, C15 | 4 |
| P08 | Conversao e matricula | C1, C6, C7, C13, C14 | 5 |
| P09 | Financeiro simples | D1, D2, D3, D7, D8, D10 | 6 |
| P10 | Financeiro sensivel | D4, D5, D6, D9, D11, D12, D13, D14, D15 | 9 |
| P11 | Retencao preventiva | E1, E2, E3, E6, E7, E10 | 6 |
| P12 | Retencao sensivel | E4, E5, E8, E9, E11, E12, E13 | 7 |
| P13 | Comando e governanca | F1, F2, F3, F4, F5, F6, F7, F8, F9, F10 | 10 |
| P14 | Integracao, teste e incidente | F11, F12, F13, F14, F15 | 5 |
| P15 | Historico e professor | G1, G2, G3, G4, G5, G6, G7, G8, G9, G10, G11, G12 | 12 |

Total: 96 fluxos.

## P01 Conversa Segura

Fluxos: A1, A2, A3, A4, A5, A10.

Serve para conversas de inbox, respostas permitidas, chamada humana e SLA.

Fixo:

- identidade minima do contato;
- opt-out respeitado;
- baixa confianca chama humano;
- auditoria de envio ou chamada humana;
- limite de respostas automaticas.

Default:

- Autonomo com excecoes para triagem;
- Autonomo para FAQ permitido, fora de escopo, chamada humana e SLA;
- fallback para tarefa/fila humana.

Ajustes do studio:

- fila responsavel;
- limite de respostas antes de chamar humano;
- tom/template aprovado;
- tempo de SLA;
- se o botao de ajuda aparece em modo manual.

## P02 Identidade E Privacidade

Fluxos: A6, A7, A8, A9.

Serve para consentimento, opt-out, identidade, midias, LGPD e privacidade.

Fixo:

- opt-out sempre bloqueia envio;
- pedido de dados sensiveis exige aprovacao/caso;
- identidade incerta nao libera acao sensivel;
- auditoria obrigatoria.

Default:

- opt-out em Autonomo;
- midias/identidade em Autonomo com excecoes;
- privacidade e telefone compartilhado em Autonomo com aprovacao.

Ajustes do studio:

- responsavel de revisao;
- aprovador de privacidade;
- tipos de midia aceitos;
- regra de validacao de identidade.

## P03 Presenca E Faltas

Fluxos: B1, B2, B3, B14.

Serve para confirmar presenca, tratar falta, no-show e correcao de chamada.

Fixo:

- aula e aluno precisam existir;
- janela de envio;
- chamada auditavel;
- correcao de presenca exige motivo.

Default:

- confirmacao de presenca em Autonomo;
- falta/no-show em Autonomo com excecoes;
- correcao de presenca em Autonomo com aprovacao.

Ajustes do studio:

- horario do lembrete;
- regra de falta;
- responsavel;
- quando criar tarefa de retencao;
- aprovador de correcao.

## P04 Reposicoes E Vagas

Fluxos: B4, B5, B6, B13.

Serve para vaga aberta, lista de espera, reposicao/remarcacao e credito de reposicao.

Fixo:

- capacidade da aula;
- credito e validade;
- lista de espera;
- regra de reposicao;
- auditoria em mudanca de saldo.

Default:

- recuperar vaga/lista em Autonomo com excecoes;
- reposicao e credito em Autonomo com aprovacao.

Ajustes do studio:

- prioridade da lista;
- limite de convites;
- validade de credito;
- aprovador;
- destino de excecoes.

## P05 Agenda Estrutural

Fluxos: B8, B9, B10, B11, B16.

Serve para mudanca de horario fixo, cancelamento pelo studio, conflito de capacidade, ajuste de grade e evento/workshop.

Fixo:

- simulacao de impacto;
- alunos afetados;
- comunicacao aprovada;
- auditoria;
- aprovacao antes de impacto.

Default:

- Autonomo com aprovacao.

Ajustes do studio:

- aprovador;
- prazo de aprovacao;
- template de comunicado;
- responsavel por excecoes;
- data de vigencia.

## P06 Experimental E Primeira Aula

Fluxos: B7, B12, B15, C2, C3, C4, C5, C11, C12.

Serve para disponibilidade, experimental, no-show experimental, primeira aula, follow-up e demanda sem vaga.

Fixo:

- consentimento;
- limite de contato;
- interessado/aluno vinculado;
- aula ou agenda quando aplicavel.

Default:

- lembrete experimental em Autonomo;
- demais fluxos em Autonomo com excecoes.

Ajustes do studio:

- cadencia;
- responsavel comercial;
- horarios oferecidos;
- limite de tentativas;
- quando chamar humano.

## P07 Captura E Qualificacao

Fluxos: C8, C9, C10, C15.

Serve para origem, qualificacao, perda comercial, indicacao e entrada multicanal de lead.

Fixo:

- origem registrada;
- duplicidade verificada;
- dono do lead;
- motivo de perda ou indicacao quando houver.

Default:

- origem/entrada multicanal em Autonomo com excecoes;
- perda e indicacao em Autonomo com aprovacao.

Ajustes do studio:

- fontes aceitas;
- campos obrigatorios;
- responsavel;
- regra de duplicidade;
- aprovador de beneficio.

## P08 Conversao E Matricula

Fluxos: C1, C6, C7, C13, C14.

Serve para valores, planos, objecoes, pre-matricula, conversao e upgrade.

Fixo:

- base de planos aprovada;
- promessa comercial limitada;
- matricula exige aprovacao;
- upgrade exige aprovacao;
- contrato/plano auditavel.

Default:

- valores/planos em Autonomo com excecoes;
- matricula, objecoes e upgrade em Autonomo com aprovacao.

Ajustes do studio:

- aprovador;
- base de respostas;
- template de proposta;
- checklist de matricula;
- responsavel comercial.

## P09 Financeiro Simples

Fluxos: D1, D2, D3, D7, D8, D10.

Serve para lembrete de vencimento, atraso, Pix/link, falha, recibo e conciliacao.

Fixo:

- valor/cobranca precisa existir;
- opt-out respeitado;
- idempotencia;
- auditoria financeira;
- limite de tentativas.

Default:

- lembrete de vencimento em Autonomo;
- atraso/falha/recibo em Autonomo com excecoes;
- Pix/link e conciliacao em Autonomo com aprovacao.

Ajustes do studio:

- horario;
- template;
- tentativas;
- fila financeira;
- limite de valor;
- aprovador.

## P10 Financeiro Sensivel

Fluxos: D4, D5, D6, D9, D11, D12, D13, D14, D15.

Serve para confirmacao de pagamento, renovacao, desconto, pausa, contrato, bloqueio, credito, fechamento e alteracao de plano.

Fixo:

- aprovacao em acoes financeiras sensiveis;
- motivo obrigatorio;
- auditoria;
- antes/depois seguro;
- sem decisao financeira livre.

Default:

- quase todos em Autonomo com aprovacao;
- fechamento mensal em Autonomo com excecoes.

Ajustes do studio:

- aprovador;
- responsavel financeiro;
- prazo;
- limite de valor;
- checklist;
- tipos de excecao permitidos.

## P11 Retencao Preventiva

Fluxos: E1, E2, E3, E6, E7, E10.

Serve para queda de frequencia, inatividade, retorno, satisfacao, retorno apos pausa e marco de engajamento.

Fixo:

- consentimento;
- limite de contato;
- risco alto chama humano;
- historico sensivel protegido.

Default:

- Autonomo com excecoes.

Ajustes do studio:

- cadencia;
- responsavel;
- regra de queda/inatividade;
- quando abrir reclamacao;
- limite de contato.

## P12 Retencao Sensivel

Fluxos: E4, E5, E8, E9, E11, E12, E13.

Serve para risco de cancelamento, reativacao, risco por perfil, pos-cancelamento, saude/evento pessoal, segmentacao e reclamacao.

Fixo:

- aprovacao antes de contato sensivel;
- dono do caso;
- pausa de automacoes quando necessario;
- sem promessa de compensacao livre;
- auditoria.

Default:

- Autonomo com aprovacao.

Ajustes do studio:

- dono do caso;
- aprovador;
- quando pausar automacoes;
- segmento permitido;
- cadencia de reativacao.

## P13 Comando E Governanca

Fluxos: F1-F10.

Serve para prioridades, dinheiro na mesa, fila humana, gargalos, resumo, qualidade de dados, cotas, performance, auditoria e capacidade.

Fixo:

- fontes internas;
- consumo/cota visivel;
- permissao;
- sem alterar regra sensivel sem aprovacao.

Default:

- prioridades, fila, resumo e limites em Autonomo;
- analises e qualidade em Autonomo com excecoes;
- permissoes/auditoria em Autonomo com aprovacao.

Ajustes do studio:

- horario/frequencia;
- responsavel;
- fontes exibidas;
- tipo de alerta;
- metricas visiveis.

## P14 Integracao, Teste E Incidente

Fluxos: F11-F15.

Serve para falhas, logs, importacao, teste de fluxo, incidente e mudanca de politica.

Fixo:

- logs tecnicos ficam em Integracoes;
- incidente fica em Operacao;
- publicacao exige simulacao;
- reprocessamento so se for seguro/idempotente;
- mudanca de politica exige aprovacao.

Default:

- teste de fluxo em Autonomo;
- falhas/incidente em Autonomo com excecoes;
- importacao/mudanca de politica em Autonomo com aprovacao.

Ajustes do studio:

- responsavel;
- severidade;
- aprovador;
- auto-pausa;
- data de vigencia;
- exemplos de simulacao.

## P15 Historico E Professor

Fluxos: G1-G12.

Serve para contexto de aula, observacao, restricao, evolucao, documentos, correcao, repasse, lembrete e compartilhamento.

Fixo:

- permissao de historico;
- dado sensivel protegido;
- compartilhamento com aprovacao;
- correcao auditavel;
- visibilidade por papel.

Default:

- lembrete professor em Autonomo;
- contexto/observacao/linha do tempo em Autonomo com excecoes;
- restricao/documento/compartilhamento/permissao em Autonomo com aprovacao.

Ajustes do studio:

- visibilidade;
- professor/responsavel;
- aprovador;
- documentos exigidos;
- horario do lembrete;
- campos do resumo.

## Como Visualizar No Produto

Na tela do fluxo, o usuario nao escolhe perfil. O perfil so decide quais campos aparecem.

Exemplo:

- D2 Pagamento Atrasado usa P09 Financeiro simples.
- Como o modo e Autonomo com excecoes, a tela mostra tentativas, fila financeira e sinais que chamam humano.
- Nao mostra configuracao de prompt, retry tecnico ou auditoria.

## Criterios De Aceite

Este mapa esta correto quando:

- reduz os 96 fluxos a 15 perfis;
- cada perfil tem poucos ajustes visiveis;
- nenhum perfil exige conhecimento tecnico;
- defaults resolvem a maior parte dos studios;
- as configuracoes sensiveis continuam protegidas por aprovacao, permissao e auditoria.
