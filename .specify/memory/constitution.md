# Constituição — Landing Taliya/Copiloto

## Princípios

### I. Origem preservada

O trabalho ocorre apenas na cópia independente iniciada do commit documentado. Não alterar o repositório original, remotes, DNS ou site publicado; não fazer push, merge ou deploy.

### II. Copy sem redesign

Nas seções existentes S01–S14, atualizar somente texto visível/acessível e dados de copy. Preservar a estrutura de componentes, a ordem, os estilos, o espaçamento, as proporções, a responsividade, os controles, o estado, os callbacks, os destinos e as interações.

### III. Exceções precisam de escopo próprio

São autorizados: trabalho técnico SEO; o Mural S06 como única nova seção, reutilizando mockups/balões presentes; e refatorações pontuais de arquitetura/reuso depois de concluída a integração S017. Cada exceção requer spec e verificação de equivalência.

### IV. Fontes de conteúdo e verdade

O JSON da landing governa a copy. O adendo SEO v1.1 governa descoberta e metadados. Não inventar preço, integração, disponibilidade, prova social, operação de produto ou resultado de SEO/ChatGPT.

### V. SDD sequencial

Uma spec por seção, além de fundação, SEO, integração e arquitetura/reuso final. Para cada etapa: spec, plano e tarefas apoiados em código real, análise, implementação delimitada, verificação e evidência antes de avançar.

### VI. Refatoração só com motivo

Depois da integração, avaliar estrutura, componentização, reuso, SOLID e clean code com evidência do código. Fazer apenas alterações que resolvam problema concreto e não alterem a experiência observável.

## Restrições

- Não modificar `/pilates` ou `/pilates/planos` enquanto o tratamento de legado não for decidido.
- Não inserir a faixa S02, não substituir a calculadora por fluxos, não criar formulários ou controles novos fora do Mural autorizado.
- Não alterar endpoints/backend nem simular envio bem-sucedido.
- Demos e textos ilustrativos não representam o produto real.
- Conteúdo de pacotes conflitante com o pedido mais recente é documentado, não implementado silenciosamente.

## Fluxo de trabalho

- Manter o estado e os caminhos ativos em `specs/taliya-migration/README.md`.
- Checklists avaliam qualidade documental; `verification.md` registra procedimentos de runtime realmente executados.
- Baselines visuais precedem alterações de aplicação e devem ser comparados depois.
- Se uma copy for impossível sem quebrar um limite, registrar bloqueio pontual e continuar apenas tarefas independentes.

**Versão**: 1.0 | **Ratificada**: 2026-09-25 | **Última revisão**: 2026-09-25
