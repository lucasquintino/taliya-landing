# Glossario de produto - PT-BR

> Status: rascunho de leitura. Use este glossario para evitar que os documentos de produto virem documentacao tecnica antes da hora.

## Termos que devem aparecer para produto

| Em vez de | Usar | Significado pratico |
| --- | --- | --- |
| Rota | Tela, area ou caminho | Lugar por onde o usuario passa no sistema. |
| Drawer | Painel lateral | Um painel que abre dentro da tela atual. |
| Modal | Janela de confirmacao | Uma janela pequena para confirmar, revisar ou completar algo. |
| Background action | Acao de bastidor | Algo que o sistema faz sem abrir uma tela propria. |
| Gate | Trava | Regra que impede uma acao sensivel sem validacao. |
| SLA | Prazo combinado | Tempo maximo esperado para responder ou resolver. |
| Runtime | Execucao do agente | Momento em que o agente roda uma tarefa. |
| Data model | Objetos principais do produto | Coisas que o sistema precisa conhecer: aluno, pagamento, turma, aula, conversa. |
| Backend/API | Base tecnica do sistema | Parte que guarda dados e conecta telas, agentes e integracoes. |
| RBAC | Permissao por papel | O que gestor, professor, recepcao e suporte podem ver ou fazer. |
| Merge | Juntar itens parecidos | Quando dois casos parecem diferentes, mas podem virar uma unica experiencia. |
| P0/P1/P2 | Essencial, importante, depois | Ordem de prioridade para decidir escopo. |
| Candidate | Candidato | Ainda esta em avaliacao; nao e escopo fechado. |
| Web-only | Melhor no computador | Funcao que provavelmente nao precisa ir para o celular agora. |
| Mobile review | Revisar pelo celular | Celular serve para aprovar, negar ou acompanhar. |
| Copiloto | Agente sugerindo | A IA recomenda, mas uma pessoa decide. |
| Autonomo | Automatico com limites | O sistema executa sozinho somente quando regras, cotas e permissoes permitem. |

## Regra de escrita

Nos documentos PT-BR, a preferencia e escrever como um gestor de studio pensaria:

- "resolver pagamento atrasado", nao "executar fluxo financeiro";
- "aprovar acao sugerida pelo agente", nao "aprovar run";
- "trava financeira", nao "gate financeiro";
- "permissao por papel", nao "RBAC";
- "tela, botao ou painel", nao "route type".

Codigos internos podem existir nas planilhas para rastreio, mas nao devem ser a forma principal de leitura.
