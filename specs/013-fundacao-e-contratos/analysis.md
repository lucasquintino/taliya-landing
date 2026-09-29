# Consistência antes da implementação — 013
2026-09-28. Análise manual equivalente às instruções locais speckit-analyze,
com prerequisites Bash; não houve invocação shell fictícia de slash command.

- 5 requisitos, 5 casos, 6 tarefas iniciais e 3 tarefas adicionais de convergência: cobertura definida em todos os artefatos.
- Conflito de constituição/copy-only resolvido em adendo separado, autorizado pelo pedido.
- Diretórios 013–025 livres; branches antigas não são specs colidentes. Pointer desacopla branch.
- Plano original pressupõe consulta de billing: fonte não localizada; T013-02 e aceite integrado continuam bloqueados.
- CLI oferece converge no core_pack, mas a integração de skills não o instalou. Instrução oficial lida; aplicar revisão de lacunas com tarefas append-only.
- Snapshot validator pressupõe zero progresso: separar execução contínua e preservar o snapshot, sem afrouxar aceites.
- Recorte permitido: governança, documentação, baselines e scripts/testes offline. Não alterar runtime antes das dependências.

## Convergência
Resultados finais e divergências remanescentes serão registrados em verification.md.

## Revisão da preparação de 013–025 — 2026-09-28

81 tarefas mapeadas a 65 requisitos/casos; IDs, dependências e critérios originais
preservados. Planos candidatos do ZIP receberam recortes de código atual em
`execution.md`, sem ativar specs futuras. Não houve invocação fictícia de CLI.

- Cobertura/ciclos/dessincronização de cards: verificados pelo novo checker e testes
  negativos. Preparação documentada não libera uma dependência incompleta.
- HIGH B013-01: contrato publicado do billing ausente; obter fonte, sem substituir serviço.
- HIGH B013-02: Internal ativo/staff não comprovados; não escolher painel pela URL 401.
- HIGH B013-03: homologação/orçamento/permissões pendentes; nenhum smoke pago executado.
- HIGH B013-04 para publicação de conteúdo: mídia/direitos não comprovados; catálogo vazio preservado.
- SDK/payload reais, TTL da oferta, retenção e limites propostos exigem confirmação
  na autoridade correspondente antes do recorte afetado. Não são decisões silenciosas.

Hooks de commit opcionais foram dispensados conforme escopo local autorizado.
23 testes de ferramentas de governança passaram; aceites de runtime permanecem abertos.

## Revisão de consistência — 2026-09-29

O usuário corrigiu a premissa: não existe billing/Asaas. T013-02 e T013-07
concluíram o mapeamento e o contrato-alvo local; a implementação e os testes
financeiros foram atribuídos à 015, dependente da 014. O índice corrente contém
87 tarefas, 68 requisitos e 68 casos. As afirmações de 28/09 sobre buscar serviço
publicado e os números 81/65 são históricos, não comandos de execução atuais.
G0 segue bloqueado pela implantação/identidade staff do Internal e pela
homologação da fundação em ambiente autorizado. Os 23 testes de governança
foram atualizados e passaram novamente após a mudança de estado.
