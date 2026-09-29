# SDD + Spec Kit no repositório existente
## Diagnóstico específico
O ZIP possui `.specify/init-options.json` com integração Codex/skills, scripts PowerShell e versão declarada `0.8.3.dev0`. O ponteiro `.specify/feature.json` ainda indica `specs/taliya-migration/001-fundacao-migracao`. A constituição proíbe alterações de backend no recorte copy-only. Isso precisa de reconciliação explícita, não de ignorar regras nem recomeçar a aplicação.

## Política de manutenção
Usar novas specs para capacidades transversais e preservar histórico (flow-forward). Dentro de cada nova capacidade, manter spec/plan/tasks coerentes com revisões explícitas. Não apagar as 001–012 nem rerodar todas as seções da migração. [K2]

013–025 são identificadores propostos para a árvore observada. Conferir numeração atual com o Spec Kit antes de criar diretórios. O pacote é uma proposta de artefatos de domínio, não afirma que o CLI rodou. Adotar os arquivos via diff e permitir que Spec Kit gere/ajuste seus próprios artefatos sem destruir conteúdo útil.

## Ciclo por spec
1. Confirmar constituição/contexto ativos e contrato da spec.
2. `speckit.specify`: objetivo e comportamento, com requisitos deste pacote e histórias reais.
3. `speckit.clarify`: resolver ambiguidades materiais; primeiro procurar informação no repo/fontes, sem perguntar decisões já dadas.
4. `speckit.plan`: pontos do código, contratos, migrações, testes e rollout.
5. `speckit.checklist`: qualidade dos requisitos, não resultado de runtime.
6. `speckit.tasks`: tarefas rastreáveis, testes por história e dependências.
7. `speckit.analyze`: conflitos/gaps entre arquivos; corrigir antes de implementar.
8. `speckit.implement`: executar somente recorte permitido, mantendo os testes honestos.
9. `speckit.converge`, quando disponível na versão instalada; caso não exista, executar revisão equivalente documentada de requisitos × código × testes e registrar gaps antes de fechar. Não fingir invocação que a versão não oferece.
10. Revisão humana de UX/política/operação onde indicada; commit e atualização de status/evidências.

Na documentação atual há converge e formas diferentes de invocação por integração. Em Codex skills, normalmente `$speckit-specify`, `$speckit-plan`, etc.; em integrações slash, `/speckit.specify`, etc. Conferir o que a instalação real expõe. Esses comandos são invocados no chat do agente de código, não tratados como comandos shell genéricos. [K1]

## Não executar refresh destrutivo
Não usar `specify init --here --force` como atalho. Primeiro registrar versão, backup/commit, diffs de AGENTS/constituição/templates e scripts. Se necessário atualizar, fixar release e revisar cada arquivo gerenciado. No Mac, decidir conscientemente entre PowerShell disponível e variante shell/Python compatível. A presença de scripts .ps1 não prova que o runtime correto esteja instalado. [K2/K3]

## Convenções de implementação
Reutilizar a estrutura de Next/Python/Postgres. Componentes compartilhados e contratos pequenos; separar domínio, adaptador de provedor e transporte sem criar camadas abstratas sem consumidor real. Tipagem forte, schema de entrada, erros discriminados, logs sanitizados. Não mudar dependências ou layout fora da necessidade comprovada.

Um responsável integra arquivos compartilhados. Paralelizar recortes sem editar os mesmos contratos ao mesmo tempo. Evitar um PR gigante: preferir entrega pequena e testável por spec/slice. Cada PR aponta R-ID, testes, migrações e evidências. Novas tarefas descobertas voltam aos artefatos; não ficam apenas na conversa.

## Campos mínimos do handoff por sessão de implementação
Spec ativa; commit; objetivo concluído; requisito pendente; testes executados; resultado; bloqueio real; próxima tarefa exata; arquivos alterados; decisões de supersessão. Não dizer “pronto” com teste não executado. Não reabrir escolha de modelo/PostHog por preferência pessoal do implementador.

## Gate de autorização
Preparar plano e código não autoriza publicar, criar recursos pagos, alterar DNS, disparar campanhas, cancelar assinaturas ou migrar produção. Essas ações passam pelo gate operacional explícito registrado. Esta auditoria não executou nenhuma delas.
