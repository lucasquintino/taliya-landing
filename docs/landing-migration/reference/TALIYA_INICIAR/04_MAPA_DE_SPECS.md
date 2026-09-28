# Mapa de trabalho — SDD por seção

Este é um **índice de planejamento**, derivado das seções 10–15 do prompt
mestre v2. Não é um conjunto de specs já finalizadas, nem comprova que o
código foi inspecionado. Crie os artefatos reais no projeto novo após ler as
fontes e o repositório. Os nomes abaixo são a organização lógica proposta;
respeite convenções equivalentes existentes sem mover o código para imitá-la.

| Diretório lógico | Responsabilidade |
|---|---|
| `001-fundacao-migracao` | Cópia independente, baseline, inventário e contratos compartilhados |
| `002-seo-arquitetura-publica` | Regras transversais do adendo, rotas, metadados e renderização pública |
| `003-s01-header-hero` | S01: preservar composição e migrar topo, navegação, CTAs e demo |
| `004-s02-confianca-controle` | S02: faixa de confiança e limites verdadeiros |
| `005-s03-na-pratica` | S03: casos, seletor, mockup e vínculos |
| `006-s04-sem-com-taliya` | S04: comparativos, toggle e carrossel |
| `007-s05-como-funciona` | S05: abas, conteúdos e estados |
| `008-s06-mural` | S06: mensagens, seleção por dispositivo e destinos |
| `009-s07-sete-frentes` | S07: frentes, subtipos, demos e deep links |
| `010-s08-fluxos` | S08: remoção da calculadora e fluxos com estados coerentes |
| `011-s09-como-comecar` | S09: etapas e narrativa de entrada |
| `012-s10-entrada-oferta` | S10: formulário de interesse e gates de oferta |
| `013-s11-prova-real` | S11: evidência/autorização e ausência correta do bloco |
| `014-s12-faq` | S12: perguntas, respostas, accordion e foco |
| `015-s13-sua-rotina` | S13: pesquisa de encaixe, com finalidade separada |
| `016-s14-cta-footer-flutuante` | S14: CTA final, footer e controle flutuante |
| `017-integracao-validacao-final` | Página integrada, jornadas, regressões e cobertura dos pacotes |

Todos os recortes estão **pendentes de especificação detalhada no ambiente
de implementação**. Não marque nenhum como implementado/verificado por
constar nesta tabela. O número do diretório não altera o ID Sxx do pacote,
a ordem visual da página, as rotas nem a componentização.

## Documentação de cada recorte

```text
spec.md
plan.md
tasks.md
checklists/requirements.md
verification.md
```

O prompt mestre especifica o conteúdo de cada arquivo. O plano precisa
apontar os componentes/arquivos reais; a verificação precisa registrar
procedimentos realmente executados. A existência dos arquivos não libera,
por si só, a implementação. A forma de invocar Spec Kit deve ser conferida
na integração e versão efetivamente instaladas.

## Regras comuns e dependências

A Constitution é única. A spec 001 mantém os contratos comuns de conteúdo,
modo, navegação, demos, formulários e instrumentação. A 002 mantém o contrato
SEO. As seções consomem esses contratos em vez de defini-los novamente.

Prepare primeiro a fundação e os contratos; ordene as seções pelas dependências
reais, sem mudar sua posição visual. Receptores de deep links e CTAs devem
estar definidos antes de seus emissores. Não paralelize edições conflitantes
em componentes compartilhados ou no contexto ativo da ferramenta.

Mantenha o ciclo de requisitos, clarificações necessárias, plano, checklist,
tarefas, análise, implementação e verificação descrito no prompt. Não
invente execução de ferramentas, aprovação humana ou evidências.

S11 pode estar corretamente implementada com o bloco ausente: não criar um
depoimento fictício para preencher a seção. Integrações externas bloqueadas
não impedem recortes independentes, mas impedem declarar o fluxo afetado
funcional ou a publicação liberada.

O trabalho termina com integração e evidências, não somente com 17 pastas
criadas. A retomada deve ficar registrada no índice real `specs/README.md`.
