# Feature Specification: Fundação da migração Taliya/Copiloto

**Feature Branch**: `013-taliya-foundation`  
**Created**: 2026-09-25  
**Status**: Draft for review  
**Input**: Retomar a landing Copiloto em uma cópia limpa do repositório original, com migração textual, SEO, Mural, integração final e arquitetura/reuso posterior.

## User Scenarios & Testing

### User Story 1 — Continuar em um projeto independente (Priority: P1)

Como responsável pela landing, quero trabalhar sobre uma cópia identificável do código existente, para que a migração não altere o projeto original.

**Why this priority**: A preservação da origem é requisito de toda etapa posterior.

**Independent Test**: Comparar a revisão inicial, o estado da cópia, o remote e o repositório de origem.

**Acceptance Scenarios**:

1. **Given** o commit de origem identificado, **When** a cópia é preparada, **Then** a árvore de aplicação começa daquele commit e registra sua revisão.
2. **Given** a cópia independente, **When** ela é inspecionada, **Then** não há remote configurado e o projeto original permanece sem alterações.

### User Story 2 — Preservar a experiência enquanto a copy muda (Priority: P1)

Como visitante, quero encontrar os textos Copiloto dentro da experiência existente, para compreender o conteúdo sem perder o layout e as interações que já conheço.

**Why this priority**: A solicitação autoriza migração de conteúdo e fixa preservação visual e comportamental.

**Independent Test**: Comparar árvore de componentes, ordem, estilos, controles, destinos e estados antes e depois de uma etapa de copy.

**Acceptance Scenarios**:

1. **Given** uma seção antiga, **When** sua copy é migrada, **Then** somente textos visíveis/acessíveis e dados textuais mudam.
2. **Given** um controle da seção antiga, **When** o usuário o utiliza após a migração, **Then** sua interação, destino, estado e comportamento permanecem os mesmos.
3. **Given** a rota antiga `/pilates`, **When** a nova home for adicionada, **Then** `/pilates` mantém conteúdo e comportamento originais na cópia.

### User Story 3 — Avançar por etapas com rastreabilidade (Priority: P2)

Como revisor, quero ver o escopo permitido, a etapa ativa e os critérios de passagem, para revisar uma etapa concluída antes de seguir a sequência.

**Why this priority**: O usuário pediu uma retomada concreta, etapa por etapa, e a aplicação dos pacotes depende de especificações rastreáveis.

**Independent Test**: Conferir o índice, a Constituição, a matriz de fonte→requisito→arquivo e os estados da verificação.

**Acceptance Scenarios**:

1. **Given** as 14 seções previstas, **When** o índice da migração é consultado, **Then** existe um recorte por seção, além de fundação, SEO, integração e arquitetura final.
2. **Given** os limites diretos do usuário e instruções dos pacotes, **When** existir conflito, **Then** o índice respeita o limite direto e registra a divergência.
3. **Given** um check não executado, **When** seu estado é documentado, **Then** ele fica como pendente/não testado.

### Edge Cases

- Se o dataset pedir uma nova composição fora do Mural, a mudança para até e registra o conflito; não acrescenta markup por conta própria.
- Se um texto Copiloto não tiver campo compatível, ele não é encaixado alterando estado ou comportamento.
- Se a copy de uma seção (por exemplo, uma calculadora) deixar números antigos incorretos, a etapa fica bloqueada para decisão sem alterar a lógica.
- Se a decisão de domínio/legado continuar aberta, não se altera o site publicado e não se presume um redirect.
- Se o Spec Kit de origem tiver contexto ativo diferente, a cópia usa o contexto de migração sem remover templates ou histórico original.

## Requirements

### Functional Requirements

- **FR-001**: O projeto independente MUST derivar do commit `c473a440d562acf6d5314cce0701d48ec284fc07` do repositório indicado.
- **FR-002**: A migração MUST manter o repositório original intocado, não configurar remote no projeto independente e não publicar/deployar.
- **FR-003**: Nas etapas S01–S14, a árvore visual, ordem, CSS, tokens, espaçamentos, controles, handlers, estado e destinos existentes MUST permanecer iguais; somente conteúdo textual pode mudar.
- **FR-004**: A cópia MUST preservar `/pilates` e `/pilates/planos` até decisão documentada de legado, sem inventar redirecionamentos.
- **FR-005**: O conteúdo novo MUST ser rastreado ao JSON canônico e os critérios SEO MUST ser rastreados ao adendo SEO v1.1.
- **FR-006**: O Mural S06 MUST ser a única seção de UI adicional autorizada, com reutilização de mockups/balões existentes e sem conexão a chat, LLM ou backend real.
- **FR-007**: O escopo MUST excluir adicionar a faixa S02, converter a calculadora em fluxos, criar novos controles/subtabs/formulários ou alterar o comportamento das interações existentes.
- **FR-008**: A estrutura documental MUST conter fundação, SEO, uma spec por S01–S14, integração final e arquitetura/reuso após a integração.
- **FR-009**: Cada etapa MUST manter sua própria verificação e registrar distinção entre especificado, implementado, executado, pendente e bloqueado externamente.
- **FR-010**: Melhorias de arquitetura/reuso MUST ocorrer somente após integração, ser justificadas por evidência de duplicação/acoplamento e manter equivalência visual/comportamental.
- **FR-011**: A home Copiloto e mudanças transversais de SEO MUST ser implementadas somente nas rotas/arquivos da cópia independente.

### Key Entities

- **Cópia independente**: árvore de projeto criada a partir de revisão identificada, sem remote.
- **Fonte canônica de conteúdo**: pacote landing v1.0 que governa copy, IDs e cenários.
- **Adendo SEO**: fonte que governa descobribilidade, metadados e arquitetura pública.
- **Etapa SDD**: um dos 18 recortes da sequência, com spec, plano, tarefas e evidência próprios.
- **Baseline**: observação da origem e das telas antes das mudanças.

## Success Criteria

### Measurable Outcomes

- **SC-001**: A cópia registra a URL de origem e a revisão de 40 caracteres, e `git remote -v` não retorna remotes.
- **SC-002**: O estado inicial de `/pilates` e os arquivos da origem são preservados e podem ser comparados após cada etapa.
- **SC-003**: O índice apresenta 18 recortes ordenados: 001, 002, 003–016, 017 e 018.
- **SC-004**: Nenhuma mudança de componente/layout/interação de S01–S14 é aceita sem autorização que amplie o escopo.
- **SC-005**: Cada check de implementação tem status observado; documentos de especificação não são apresentados como prova de runtime.

## Assumptions

- A revisão `c473a440d562acf6d5314cce0701d48ec284fc07` permanece a base escolhida pelo usuário.
- A nova home Copiloto ocupará `/`; a rota `/pilates` da cópia continuará disponível e inalterada enquanto a decisão pública de legado estiver pendente.
- A divisão S01–S14 descreve specs e fontes, não novos componentes.
- O pedido mais recente prevalece sobre propostas estruturais do pacote, exceto pelas três autorizações expressas: SEO, Mural e arquitetura pós-integração.
- A prova social seguirá ausente sem material autorizado.
