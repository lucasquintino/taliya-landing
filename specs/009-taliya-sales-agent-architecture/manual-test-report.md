# Agent V2 Manual Runtime Test Report

Run date: 2026-05-21  
Mode: local production server, `AI_ATTENDANT_V2_MODE` unset/default v2 auto, WhatsApp token `mock`
Target: `http://localhost:3999`

## Commands

- `npm run lint`
- `npm run build`
- `npm run eval:agent-v2:layers`
- `npm run eval:agent-v2:matrix`
- `npm run eval:agent-v2:runtime`

## Results

- Layer evals: pass
- Conversation matrix: 62/62 pass
- Runtime simulations: 29/29 pass
- Sales Inbox endpoint probe: pass, sanitized report saved in `eval-reports/sales-inbox-runtime.json`
- WhatsApp webhook probe: pass with mock Cloud API send and separated message previews

## Runtime Transcripts

### Widget - price before diagnostic

Lead: oi  
Agent: Oi! Tudo bem?  
Agent: Em que posso te ajudar?

Lead: Quero ver planos  
Agent: Hoje os planos sao: Base: R$ 197/mes; Essencial: R$ 497/mes; Avance: R$ 897/mes; Completo: R$ 1.497/mes.  
Agent: Se preferir ver direto, o comparativo fica aqui: https://www.taliya.com.br/pilates/planos

Lead: diagnostico  
Agent: Vou usar o que voce ja contou.  
Agent: Hoje seu studio tem mais ou menos quantos alunos ativos?

### Widget - diagnostic to waitlist to post-waitlist question

Lead: oi  
Agent: Oi! Tudo bem?  
Agent: Em que posso te ajudar?

Lead: Quero fazer diagnostico gratuito  
Agent: Vou usar o que voce ja contou.  
Agent: Hoje seu studio tem mais ou menos quantos alunos ativos?

Lead: 96  
Agent: Boa, isso ja me da uma nocao do tamanho da operacao.  
Agent: Qual parte mais pesa hoje: WhatsApp, agenda/reposicoes, vendas, financeiro ou acompanhamento dos alunos?

Lead: Vendas e interessados  
Agent: Entendi. Quando interessados ficam soltos, muita oportunidade esfria antes de virar aluno.  
Agent: Hoje isso fica em algum sistema ou mais em WhatsApp, planilha e caderno?

Lead: Hoje uso WhatsApp e planilha  
Agent: Entendi onde isso esta registrado hoje.  
Agent: Quando alguem chama querendo conhecer o studio, voces conseguem acompanhar ate virar aluno?

Lead: Perco interessados por demora no retorno  
Agent: Vou usar o que voce ja contou.  
Agent: Pensando na rotina do studio, qual tarefa voce mais gostaria de deixar mais leve primeiro?

Lead: Quero aliviar WhatsApp e agenda primeiro  
Agent: Ok, ja tenho as informacoes necessarias para montar seu diagnostico. Ja te retorno.  
Agent: O gargalo principal parece estar em vendas e interessados. Primeiro passo: organizar cadastro, historico de conversas, agenda/presenca e prioridades do dia em uma base unica.  
Agent: Agentes indicados: Atendimento, Agenda, Vendas. Plano para comparar: Avance ou Completo. Isso faz sentido para o momento do seu studio?

Lead: faz sentido  
Agent: Estamos trabalhando com um numero pequeno de studios agora.  
Agent: Se fizer sentido, posso colocar seu studio na lista de espera e chamar assim que abrir uma proxima janela.

Lead: pode ser  
Agent: Perfeito. Para registrar certinho, so falta um detalhe.  
Agent: Qual e o nome do studio e de qual cidade ele e?

Lead: Studio do Lucas, Vitoria  
Agent: Perfeito. Para registrar certinho, so falta um detalhe.  
Agent: Qual WhatsApp ou email voce prefere deixar para chamarmos?

Lead: 27996991427  
Agent: Perfeito. Agora ficou completo.  
Agent: Coloquei seu studio na lista de espera e chamamos assim que possivel.

Lead: quanto custa depois?  
Agent: Hoje os planos sao: Base: R$ 197/mes; Essencial: R$ 497/mes; Avance: R$ 897/mes; Completo: R$ 1.497/mes.  
Agent: Se preferir ver direto, o comparativo fica aqui: https://www.taliya.com.br/pilates/planos  
Agent: Seu studio continua registrado na lista de espera.

### WhatsApp - first direct question with reliable profile name

Lead: Quanto custa a Taliya?  
Agent: Oi, Lucas. Tudo bem?  
Agent: Hoje os planos sao: Base: R$ 197/mes; Essencial: R$ 497/mes; Avance: R$ 897/mes; Completo: R$ 1.497/mes.  
Agent: Se preferir ver direto, o comparativo fica aqui: https://www.taliya.com.br/pilates/planos

### Widget - human handoff

Lead: quero falar com uma pessoa  
Agent: Claro. Vou deixar uma pessoa assumir daqui.  
Agent: Tambem deixo o contexto salvo para voce nao precisar repetir tudo.

## Notes

- Real WhatsApp delivery with real Meta token was not executed locally; the webhook path was tested with mock send.
- Production should keep the v2 behind the feature flag until the post-deploy WhatsApp test plan passes.
