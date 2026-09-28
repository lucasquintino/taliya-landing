# Taliya CRM - Contrato Final Da Pagina De Fluxo

Status: contrato funcional v0.2.
Data: 2026-05-22.

## Objetivo

Definir como a pagina `Ver e ajustar fluxo` deve funcionar para todos os 96 fluxos de Agentes/Fluxos.

Fonte principal:

- `agents-flows-final-flow-contract-matrix.pt-BR.csv`
- `agents-flows-detailed-mode-rules-matrix.pt-BR.csv`
- `agents-flows-detailed-mode-rules-review.pt-BR.md`
- `agents-flows-lifecycle-mode-matrix.pt-BR.csv`
- `agents-flows-lifecycle-mode-review.pt-BR.md`
- `agents-flows-96-complete-detail-matrix.pt-BR.csv`
- `agents-flows-96-complete-detail-review.pt-BR.md`
- `agents-flows-chain-contract.pt-BR.md`
- `agents-flows-lifecycle-narrative-contract.pt-BR.md`
- `agents-flows-operational-variation-contract.pt-BR.md`
- `agents-flows-post-publication-light-ops-contract.pt-BR.md`
- `agents-flows-falta-com-aviso-image-prompt.pt-BR.md` para a proxima imagem de referencia.

Fontes usadas para gerar a matriz:

- `agents-flows-configuration-matrix.pt-BR.csv`
- `agents-flows-routine-profile-map.pt-BR.md`
- `agents-flows-routine-page-visual-contract.pt-BR.md`

Observacao:

```text
`agents-flows-configuration-matrix.pt-BR.csv` e insumo historico.
Ele ainda pode conter nomes antigos de modo.
Para produto, UI, prompts e imagens, usar sempre a matriz final deste contrato.
```

## Regra Principal

Cada fluxo tem seu proprio modo.

A rotina aplica um perfil (`Mais manual`, `Equilibrado` ou `Mais autonomo`), mas o usuario pode abrir qualquer fluxo e ajustar somente aquele fluxo.

A pagina do fluxo responde:

```text
Como este fluxo vai operar?
```

Ela nao deve comecar por ajuste tecnico.

## Modos Finais Da UI

| Modo | Significado simples |
|---|---|
| Manual | Humano conduz; Taliya organiza tarefa, contexto ou checklist. |
| Copiloto | Taliya sugere, resume ou prepara rascunho; humano decide e executa. |
| Autonomo com aprovacao | Taliya prepara a acao, mas para antes de concluir e pede aprovacao. |
| Autonomo com excecoes | Taliya resolve o caso comum e chama equipe quando sai da regra. |
| Autonomo | Taliya conclui o caso comum sozinha dentro dos limites publicados. |

Nao usar na UI:

- Automatico direto;
- Automatico com excecoes;
- Automatico com aprovacao.

## Teto Do Fluxo

O teto define o maior modo que aquele fluxo pode usar.

| Teto | Modos que aparecem habilitados |
|---|---|
| Autonomo com aprovacao | Manual; Copiloto; Autonomo com aprovacao |
| Autonomo com excecoes | Manual; Copiloto; Autonomo com aprovacao; Autonomo com excecoes |
| Autonomo | Manual; Copiloto; Autonomo com aprovacao; Autonomo com excecoes; Autonomo |

Modos acima do teto podem aparecer bloqueados quando isso ajudar o usuario a entender o limite.

## Estrutura Da Pagina

Rota base:

```text
/app/agentes/[agentId]/rotinas/[routineId]/fluxos/[flowId]
```

A pagina tem:

1. breadcrumb;
2. titulo do fluxo;
3. subtitulo curto;
4. chips de header lado a lado: `modo atual`, `status` e preflight compacto;
5. bloco `Como este fluxo deve trabalhar?`;
6. seletor de modo limitado pelo teto, sem texto longo dentro dos cards;
7. bloco `Como funciona neste modo`, dinamico e explicado em `Inicio`, `Meio` e `Fim`;
8. bloco `Ajustes deste fluxo`, ocupando a largura principal inteira;
9. botoes `Testar este fluxo`, `Salvar ajuste`, `Voltar para rotina`;
10. painel direito com Agente de Configuracao.

Nao criar um card grande separado de requisitos.

Preflight deve ser compacto no header, por exemplo:

```text
[Autonomo com excecoes] [Pronto] [7 requisitos OK]
```

Se houver problema:

```text
[Autonomo com excecoes] [Precisa ajuste] [2 pendencias]
```

Ao clicar no chip de preflight, a UI pode abrir uma lista curta de dependencias. Essa lista e read-only: canal, permissao, cota, dados obrigatorios, integracao e auditoria nao sao ajustes livres do fluxo.

## Texto Base Do Bloco De Modo

```text
Este fluxo herdou o comportamento da rotina, mas voce pode mudar so este caso.
```

Se o fluxo foi alterado individualmente:

```text
Este fluxo esta personalizado. Ele nao segue mais automaticamente o perfil da rotina.
```

## O Que Muda Ao Trocar O Modo

A pagina usa duas camadas:

1. `agents-flows-final-flow-contract-matrix.pt-BR.csv` define teto, modo, status, ajustes e requisitos.
2. `agents-flows-detailed-mode-rules-matrix.pt-BR.csv` define as regras detalhadas do bloco `Como funciona neste modo`.

A matriz final tem cinco colunas de resumo dinamico:

- `manual_na_pagina`;
- `copiloto_na_pagina`;
- `autonomo_aprovacao_na_pagina`;
- `autonomo_excecoes_na_pagina`;
- `autonomo_na_pagina`.

Essas colunas servem como resumo.

Para a area principal `Como funciona neste modo`, usar `agents-flows-lifecycle-mode-matrix.pt-BR.csv`.

A matriz detalhada de regras continua sendo a fonte das condicoes, excecoes e limites; a matriz de lifecycle transforma isso em narrativa de `Inicio`, `Meio` e `Fim`.

Se a coluna disser `bloqueado`, o modo aparece desabilitado e explica o motivo.

### Fonte Do Bloco Como Funciona

| Modo selecionado | Colunas usadas |
|---|---|
| Manual | `manual_como_funciona` |
| Copiloto | `copiloto_como_funciona` |
| Autonomo com aprovacao | `autonomo_aprovacao_como_funciona` + `se_parar` |
| Autonomo com excecoes | `autonomo_excecoes_segue_sozinho_quando` + `autonomo_excecoes_chama_equipe_quando` + `se_parar` |
| Autonomo | `autonomo_conclui_sozinho_quando` + `autonomo_para_quando` + `se_parar` |

Nao usar frases vagas como:

```text
Se estiver dentro da regra.
```

A tela deve mostrar quais regras exatas permitem seguir e quais casos chamam equipe, aprovacao ou fallback.

Mas essas regras devem ser explicadas como uma historia operacional:

- `Inicio`: o que dispara o fluxo e quais dados entram;
- `Meio`: o que a Taliya verifica, decide, executa, aprova ou entrega para humano;
- `Fim`: o que fica registrado, enviado, aprovado, pausado ou encadeado para outro fluxo.

O seletor de modo nao deve repetir essas explicacoes. Os cards de modo mostram so:

- nome do modo;
- icone;
- estado selecionado ou bloqueado.

A explicacao detalhada fica no bloco `Como funciona neste modo`.

## Inicio Meio Fim

Todo fluxo deve ser explicado como uma operacao completa.

O usuario precisa entender:

```text
Quando comeca?
O que acontece no meio?
Como termina?
```

Inicio, Meio e Fim mudam quando o modo muda.

O fluxo base continua o mesmo, mas a narrativa deve deixar claro:

- quem faz cada parte;
- onde a Taliya para;
- onde pede aprovacao;
- onde apenas sugere;
- onde chama equipe;
- onde conclui sozinha.

Cada etapa deve ter 2 a 4 linhas curtas e explicativas.

Nao usar frases genericas como:

```text
Taliya processa o caso.
Taliya segue a regra.
Fluxo finalizado.
```

### Inicio

Mostra:

- gatilho;
- entidade principal: aluno, aula, lead, conversa, pagamento, professor ou caso;
- dados minimos usados;
- canal ou tela de entrada, quando houver.

### Meio

Mostra:

- validacoes;
- acoes da Taliya;
- pontos de aprovacao;
- pontos que chamam equipe;
- limites do modo selecionado.

### Fim

Mostra:

- resultado;
- mensagem ou acao feita;
- tarefa, aprovacao ou caso criado;
- encadeamento para outro fluxo, quando houver;
- auditoria.

Encadeamento pertence ao `Fim`, nao ao `Meio`.

Nao colocar consequencias em listas de condicao.

## Encadeamento No Fim

Fluxos podem emendar em outros fluxos.

Mas um fluxo nao configura o outro.

Quando houver continuidade, ela deve aparecer dentro do `Fim` do fluxo.

Exemplo dentro de `Fim`:

```text
Se a falta for registrada, a Taliya cria uma tarefa de reposicao.
A rotina Vagas, reposicoes e lista de espera decide vaga, credito, prioridade e remarcacao conforme as proprias regras.
```

Essa explicacao deve mostrar:

- para qual rotina, fluxo ou area a operacao vai;
- por qual motivo;
- se continua como tarefa, aprovacao, caso ou outro fluxo;
- que o destino usa as proprias regras.

Nao colocar consequencias em `Segue sozinho quando`.

`Segue sozinho quando` deve conter apenas condicoes para o fluxo atual executar.

Se o usuario quiser mudar a logica do destino, ele deve abrir a rotina/fluxo de destino.

### Manual

Mostrar:

- tarefa ou checklist criado;
- responsavel humano;
- prazo ou prioridade, quando fizer sentido;
- onde a operacao continua.

Ocultar:

- configuracoes de envio automatico;
- aprovacoes desnecessarias;
- detalhes de autonomia.

### Copiloto

Mostrar:

- o que a Taliya sugere;
- rascunho ou resumo preparado;
- quem decide;
- botoes de aceitar, editar ou descartar.

Ocultar:

- publicacao autonoma;
- execucao sem decisao humana.

### Autonomo Com Aprovacao

Mostrar:

- acao preparada pela Taliya;
- aprovador;
- prazo de aprovacao;
- o que acontece se ninguem aprovar;
- preview da acao antes de confirmar.

### Autonomo Com Excecoes

Mostrar:

- caso comum que a Taliya resolve;
- situacoes que chamam equipe;
- responsaveis por excecao;
- fallback;
- limite de tentativas, quando houver mensagem.

### Autonomo

Mostrar:

- caso comum que a Taliya conclui sozinha;
- limites publicados;
- condicoes que param o fluxo;
- fallback;
- auditoria e cota.

## Ajuste Real Vs Requisito Fixo

Ajuste real e algo que o studio pode mudar porque altera a operacao de forma util.

Exemplos:

- responsavel por excecao;
- aprovador;
- prazo;
- tentativas;
- tom/template da mensagem;
- limite de contato;
- checklist;
- destino da tarefa.

Requisito fixo nao e configuracao livre.

Exemplos:

- canal conectado;
- integracao funcionando;
- cota disponivel;
- permissao correta;
- dados do aluno/aula/pagamento existentes;
- politica publicada;
- auditoria ativa;
- opt-out respeitado.

## Layout Do Bloco De Ajustes

`Ajustes deste fluxo` e o bloco mais importante depois do modo.

Ele deve ocupar a faixa horizontal principal inteira, com cara de formulario operacional, nao de card secundario.

Cada ajuste deve mostrar:

- nome claro;
- valor atual;
- controle simples para alterar;
- efeito pratico da mudanca quando isso nao for obvio.

Exemplo para `Falta com aviso`:

| Ajuste | Exemplo de valor | O que muda |
|---|---|---|
| Prazo para aviso | Ate 2 horas antes da aula | Define quando a Taliya pode tratar como falta avisada comum. |
| Proximo passo apos falta | Criar tarefa de reposicao | Encaminha a operacao sem configurar a logica de reposicao neste fluxo. |
| Responsaveis por excecao | Recepcao; Coordenadora; Dono/admin | Define quem recebe o caso quando sair da regra. |
| Tom/template da mensagem | Acolhedor | Define a mensagem enviada ao aluno. |

## Simulacao Do Fluxo

A simulacao deve ensaiar o fluxo real, nao prever resultado comercial.

Deve mostrar:

- gatilho;
- dados usados;
- regra aplicada;
- acao ou mensagem;
- se pede aprovacao;
- se chama equipe;
- fallback;
- encadeamento para outro fluxo ou area, quando houver;
- consumo estimado de cota;
- evento de auditoria.

Quando o modo muda, a simulacao anterior fica invalida.

## Publicacao

Um fluxo so pode publicar quando:

- modo escolhido esta dentro do teto;
- requisitos fixos estao ok;
- ajustes obrigatorios foram preenchidos;
- simulacao valida existe;
- fallback existe;
- usuario tem permissao para publicar.

## Pausa, Rollback E Fallback

Pausa pode acontecer por:

- usuario autorizado;
- cota;
- falha de integracao;
- incidente;
- aprovacao vencida;
- dependencia removida.

Rollback nao apaga auditoria. Ele volta para a ultima versao publicada da rotina ou do fluxo.

Fallback sempre cria uma continuacao operacional: tarefa, aprovacao, caso, incidente ou item na fila humana.

## Como Ler A Matriz

Cada linha da matriz final representa um fluxo.

Colunas principais:

| Coluna | Uso na UI |
|---|---|
| `id` | codigo interno; nao mostrar no card para o dono. |
| `agente` | agrupamento principal. |
| `rotina` | pagina de rotina onde o fluxo aparece. |
| `fluxo` | titulo humano do fluxo. |
| `teto` | maior modo permitido. |
| `modos_permitidos` | cards habilitados no seletor de modo. |
| `modos_bloqueados` | modos que podem aparecer bloqueados com explicacao. |
| `mais_manual`, `equilibrado`, `mais_autonomo` | modo aplicado quando a rotina usa cada perfil. |
| `modo_padrao_pagina` | modo inicial exibido ao abrir a pagina do fluxo. |
| `status_padrao_card` | chip do card da rotina. |
| `explicacao_card` | explicacao curta do card. |
| `*_na_pagina` | texto dinamico exibido ao selecionar cada modo. |
| `ajustes_do_studio` | campos que podem aparecer como configuracao. |
| `requisitos_fixos` | dependencias read-only. |
| `quando_chama_equipe` | texto de handoff. |
| `quando_pede_aprovacao` | texto de aprovacao. |
| `fallback` | continuacao operacional se nao puder seguir. |
| `onde_continua` | area, rota ou destino operacional; pode representar tela, tarefa, aprovacao ou proximo fluxo. |
| `simulacao_obrigatoria` | o que a simulacao precisa mostrar. |
| `nota_para_pagina_do_fluxo` | instrucao especifica de renderizacao. |

## Exemplo: Falta Com Aviso

Rota:

```text
/app/agentes/agenda/rotinas/presenca-e-faltas/fluxos/falta-com-aviso
```

Leitura da matriz:

- teto: Autonomo com excecoes;
- modos habilitados: Manual, Copiloto, Autonomo com aprovacao, Autonomo com excecoes;
- modo padrao no perfil Mais autonomo: Autonomo com excecoes;
- Autonomo fica bloqueado;
- ajustes reais: prazo para aviso, proximo passo apos falta, responsaveis por excecao, tom/template da mensagem;
- depois deste fluxo: se a falta for registrada, cria tarefa de reposicao e a rotina `Vagas, reposicoes e lista de espera` assume vaga, credito, prioridade e remarcacao;
- requisitos fixos: agenda publicada, aluno/aula identificados, regras publicadas, canal quando houver mensagem, permissao, cota e auditoria;
- simulacao mostra um caso comum e um caso que chama a equipe.

## Resultado Esperado Na UX

O dono nao configura 96 fluxos manualmente.

Ele:

1. escolhe um perfil na rotina;
2. entende como cada fluxo ficou;
3. abre so os fluxos que quer mudar;
4. testa o fluxo ou a rotina;
5. publica uma versao clara e auditavel.
