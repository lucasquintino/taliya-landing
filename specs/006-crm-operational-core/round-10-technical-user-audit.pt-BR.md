# Rodada 10 - Revisao tecnica e visao de usuario

> Status: auditoria v0.1 posterior as Rodadas 0-9. Este documento revisa os resultados com dois filtros: arquitetura tecnica de produto e experiencia real de um gestor de studio de Pilates.

## Veredito

Estamos no caminho certo.

O conjunto atual ja descreve um CRM operacional completo com agentes de IA integrados, plano Base com 0 agentes, web profundo, app para o dia a dia, cotas, auditoria, permissoes, suporte interno e caminhos manual/copiloto/autonomo.

Ainda nao estamos em 100% final porque a auditoria encontrou pontos que nao sao "mais telas por ansiedade", mas sim decisoes que mudam como as telas devem nascer:

- presets iniciais do studio para o gestor nao precisar configurar tudo do zero;
- navegacao final web/app para muitas superficies nao virarem menu infinito;
- exportacao final linha a linha das telas/casos/fluxos antes de prompt visual definitivo;
- fechamento de decisoes sensiveis de identidade, LGPD, autonomia, contrato, reposicao e suporte.

## Revisao tecnica

| Severidade | Achado | Impacto | Correcao/decisao |
| --- | --- | --- | --- |
| Alta | As Rodadas 1-7 cobrem as areas, mas alguns arquivos indice ainda pareciam esqueleto futuro. | Risco de alguem achar que a arquitetura nao foi preenchida ou usar o arquivo errado como fonte unica. | Atualizado `functional-architecture.pt-BR.md` e `screen-specs-detailed.pt-BR.md` para declarar que sao indices canonicos v0.1. |
| Alta | A cobertura atual e por familia/area; ainda falta exportacao final linha a linha para cada caso, fluxo, tela e rota antes de gerar telas definitivas. | O ChatGPT pode inventar ou simplificar se receber so resumo. | Manter Rodada 11 como pacote final de prompts/telas, usando fichas das Rodadas 1-7 e CSVs como controle. |
| Alta | Muitos fluxos dependem de formulas nao fechadas: prioridade do Hoje, encaixe, retencao e autonomia. | Cards, filas, badges e ordenacao podem mudar bastante. | Mantido como decisoes D013, D021, D029 e D032. |
| Alta | Um gestor real nao deve passar por setup pesado para comecar. | Risco de produto correto no papel, mas dificil de implantar. | Criada D036 sobre presets iniciais de agenda, reposicao, cobranca, vendas, retencao, mensagens e agentes. |
| Alta | Web e app tem muitas superficies mapeadas. Sem agrupamento final, o app pode ficar completo demais e lento de entender. | Risco de "tudo existe", mas o gestor nao acha o que precisa. | Criada D037 sobre navegacao final web/app. |
| Media | Rotas de configuracao tinham abreviacoes ambiguis depois da primeira rota. | Risco de implementar subrotas soltas em vez de rotas sob Configuracoes. | Normalizadas as rotas em `round-1-activation-setup-spec.pt-BR.md`. |
| Media | D011 e D035 tratam suporte interno Taliya com sobreposicao. | Risco de duplicar decisao e telas internas. | Registrar unificacao ou separacao clara na Rodada 10 antes de congelar. |
| Media | LGPD, dados sensiveis e historico do professor ainda precisam regra final. | Risco legal, reputacional e de permissao. | Mantido como D006, D017 e D031; precisa decisao antes de desenho final dessas telas. |
| Baixa | Os documentos estao em linguagem melhor que antes, mas ainda ha arquivos tecnicos em ingles usados como fonte. | Pode confundir decisao de produto se forem lidos isoladamente. | README PT-BR agora deve ser a porta de entrada para leitura de negocio. |

## Revisao como gestor de studio

### O que funciona bem

- Eu consigo entrar no sistema sem agentes e ainda operar: agenda, alunos, turmas, financeiro, vendas, comunicados, tarefas e historico.
- Eu consigo usar agentes como camada integrada, nao como produto separado.
- Eu tenho controle: aprovar, pausar, revisar execucao, voltar para manual e ver cota.
- Eu consigo resolver uma turma vaga sem depender obrigatoriamente de IA: o encaixe e calculado pelo sistema, e a IA so ajuda no texto, explicacao ou excecao.
- O app mobile cobre o dia a dia: Hoje, Agenda, Chamada, Inbox, Alunos, Professor, aprovacoes, financeiro essencial, vendas rapidas, retencao e configuracoes essenciais.
- O web cobre o que precisa de profundidade: configuracoes, politicas, agentes, relatorios, cotas, auditoria, billing e suporte.

### Onde eu ainda travaria como gestor

| Momento | Travamento provavel | Ajuste necessario |
| --- | --- | --- |
| Primeira configuracao | "Nao sei qual politica de reposicao/cobranca/mensagem escolher." | Presets iniciais por tipo de studio e explicacao de impacto. |
| Primeiro dia usando | "Tem muita coisa. Onde olho primeiro?" | Hoje precisa ser a entrada operacional principal, com tarefas e riscos ja priorizados. |
| App mobile | "Consigo fazer tudo, mas posso me perder em Mais." | Navegacao final precisa separar rotina diaria, acoes rapidas e configuracoes raras. |
| Agentes | "Nao sei se posso confiar no autonomo." | Mostrar qualidade, exemplos, simulacao, limite, custo e botao de pausa. |
| Financeiro/retencao | "Nao quero que uma mensagem ruim piore a relacao com aluno." | Copiloto por padrao em casos sensiveis; autonomia bloqueada ate regra clara. |
| Professor | "Quero dar contexto, mas nao expor dado sensivel." | Regra final de historico permitido por papel. |
| Suporte Taliya | "Se alguem da Taliya entrar, quero ver exatamente o que fez." | Grant com prazo, escopo, trilha e visibilidade para o gestor. |

## Simulacao resumida de uso

1. O gestor cria a conta, escolhe um preset de studio e importa alunos.
2. O sistema mostra qualidade de dados e o que esta bloqueando automacoes.
3. O gestor configura agenda, turmas, politicas basicas, canais e equipe.
4. O gestor entra no Hoje e ve aulas do dia, riscos, tarefas, aprovacoes e alertas de cota.
5. No app, professor faz chamada, ve contexto permitido e registra observacao.
6. Uma vaga aparece em turma; o sistema calcula encaixes programaticamente.
7. O gestor pode convidar manualmente, pedir sugestao de mensagem ou deixar o agente agir se o fluxo estiver liberado.
8. Um interessado chega; vendas registra origem, experimental, follow-up e matricula.
9. Uma cobranca vence; financeiro mostra caso, historico, permissao e sugestao de abordagem.
10. Um aluno reclama; automacao sensivel pausa, abre caso e exige revisao humana.
11. O gestor revisa agentes, execucoes, incidentes, cotas e economia.
12. Se precisar de suporte, concede acesso temporario e depois audita o que foi feito.

Resultado: o fluxo fecha como produto real, desde que presets, navegacao e decisoes sensiveis sejam resolvidos antes da geracao final de telas.

## O que adicionar

- D036: presets iniciais por tipo de studio.
- D037: navegacao final web/app.
- Exportacao final linha a linha de caso -> rota -> tela -> bloco -> acao -> estado -> permissao -> cota -> auditoria.
- Prompt final por tela somente depois das decisoes altas.

## O que ajustar

- Unificar ou separar claramente D011 e D035.
- Tratar `screen-specs-detailed.pt-BR.md` como checklist e indice, nao como documento unico de todas as telas.
- Garantir que toda rota de configuracao fique sob `/app/configuracoes/*`.
- No app, separar telas de rotina diaria de configuracoes/consultas para nao sobrecarregar o menu.

## O que remover ou evitar

- Evitar criar uma tela nova para cada automacao pequena; algumas devem ser botoes, gavetas, estados, tarefas ou jobs de bastidor.
- Evitar IA onde regra programatica resolve melhor, como ranking de encaixe.
- Evitar autonomia em cobranca delicada, cancelamento, reclamacao, LGPD, mudanca de permissao, billing e suporte interno.
- Evitar prompts visuais finais enquanto decisoes altas ainda estao abertas.

## Status apos esta revisao

| Area | Status |
| --- | --- |
| Proposta do produto | Correta: CRM completo com agentes integrados. |
| Cobertura funcional | Boa v0.1; nao ha grande area principal sem dona. |
| Rotas/telas | Cobertas por area, mas precisam exportacao final linha a linha. |
| App mobile | Mais forte que antes; precisa navegacao final. |
| Agentes | Cobertos como WhatsApp + CRM web/app; autonomia ainda depende de thresholds. |
| Cotas | Bem espalhadas; precos e pacotes seguem abertos. |
| Usuario gestor | Caminho viavel; presets e clareza diaria sao obrigatorios. |
| Pronto para gerar telas finais | Ainda nao. Pronto para prototipo exploratorio v0.1. |
