# Mapa de ciclo de vida dos objetos - PT-BR

> Status: Rodada 0 v0.1. Este documento define como os objetos criticos nascem, mudam, pausam, encerram, reabrem ou arquivam.

## Regra central

Toda tela deve respeitar o ciclo de vida do objeto. Se uma acao muda status, deve existir permissao, validacao, impacto e auditoria quando houver risco.

## Contato

```text
novo
  -> identificado
  -> vinculado a aluno/interessado/responsavel
  -> ativo
  -> opt-out parcial ou total
  -> arquivado
  -> reativado
```

Regras:

- Contato duplicado deve ir para Qualidade de dados antes de mesclar.
- Opt-out bloqueia mensagens externas, mas nao apaga o historico operacional.
- Telefone compartilhado exige validacao antes de automacao sensivel.

## Interessado

```text
novo
  -> qualificado
  -> experimental agendado
  -> experimental concluido ou faltou
  -> pre-matricula
  -> convertido em aluno
  -> perdido
  -> reativado como interessado
```

Regras:

- Todo interessado precisa de proxima acao ou motivo de perda.
- Conversao para aluno exige contato valido e dados minimos.
- Origem deve ser preservada para relatorios de venda.

## Aluno

```text
pendente de inicio
  -> ativo
  -> pausado
  -> inativo
  -> cancelado
  -> ex-aluno
  -> reativado
```

Regras:

- Cancelamento nao apaga historico.
- Pausa deve afetar agenda, cobranca e comunicacoes.
- Reativacao deve revisar plano, horario, pendencias e consentimentos.

## Responsavel

```text
criado
  -> validado
  -> permissao limitada
  -> permissao ampliada
  -> revogado
  -> arquivado
```

Regras:

- Permissoes de responsavel sao contextuais: agenda, financeiro, historico limitado e emergencia.
- Historico sensivel exige permissao explicita.

## Turma

```text
rascunho
  -> ativa
  -> cheia
  -> com vaga
  -> pausada
  -> encerrada
  -> arquivada
```

Regras:

- Mudanca de capacidade/professor/horario pode afetar alunos e deve simular impacto quando relevante.
- Turma com vaga pode acionar encaixe programatico, sugestao de agente ou tarefa manual.

## Aula

```text
agendada
  -> aberta para operacao
  -> chamada pendente
  -> chamada concluida
  -> concluida
  -> cancelada
  -> corrigida
```

Regras:

- Chamada pendente deve aparecer em Hoje e no app.
- Correcao de presenca gera auditoria.
- Cancelamento pelo studio pode exigir comunicado aprovado.

## Presenca

```text
esperada
  -> confirmada
  -> presente
  -> falta avisada
  -> no-show
  -> corrigida
```

Regras:

- Falta avisada pode gerar credito de reposicao conforme politica.
- No-show pode alimentar retencao, cobranca ou historico conforme regras.

## Direito de aula

```text
gerado
  -> disponivel
  -> reservado
  -> consumido
  -> devolvido
  -> expirado
  -> ajustado
  -> cancelado
```

Regras:

- Direito de aula pode nascer de mensalidade, pacote, contrato, aula avulsa ou cortesia.
- Consumo segue o modelo configurado do studio/plano, nao uma regra fixa do sistema.
- Ajuste manual deve registrar motivo, politica aplicada e impacto em financeiro/reposicao.

## Credito de reposicao

```text
gerado
  -> disponivel
  -> reservado
  -> usado
  -> expirado
  -> cancelado
```

Regras:

- Validade vem da politica vigente no momento da geracao.
- Uso deve guardar aula original, aula de destino e politica aplicada.
- Credito de reposicao e um tipo de direito de aula; sua origem e regra seguem `billing-lesson-consumption-models.pt-BR.md`.

## Lista de espera

```text
entrada criada
  -> elegivel
  -> convidado
  -> reservado
  -> convertido
  -> expirado
  -> removido
```

Regras:

- Convite externo deve respeitar consentimento, cota e janela de envio.
- Se houver conflito, vira tarefa ou aprovacao.

## Pagamento

```text
previsto
  -> pendente
  -> atrasado
  -> pago
  -> falhou
  -> em disputa
  -> reembolsado
  -> cancelado
```

Regras:

- Confirmacao manual de pagamento exige permissao financeira.
- Disputa, reembolso e desconto exigem aprovacao/tarefa contextual, auditoria e podem escalar para Operacao; nao exigem pagina propria de caso financeiro no MVP.

## Cobranca

```text
rascunho
  -> pronta
  -> pendente de aprovacao
  -> enviada
  -> entregue
  -> falhou
  -> paga
  -> encerrada
```

Regras:

- Envio automatico depende de consentimento, template, cota, politica e janela.
- Falha de envio deve abrir origem e permitir tarefa manual.

## Contrato/documento

```text
rascunho
  -> enviado
  -> visualizado
  -> assinado
  -> expirado
  -> cancelado
  -> arquivado
```

Regras:

- Contrato assinado deve ser somente leitura, salvo fluxo de retificacao.
- Documento sensivel exige visibilidade por papel.

## Caso operacional

```text
aberto
  -> atribuido
  -> em andamento
  -> aguardando aluno
  -> aguardando equipe
  -> pendente de aprovacao
  -> bloqueado
  -> resolvido
  -> reaberto
  -> cancelado
```

Regras:

- Caso sem dono aparece em Hoje/Operacao.
- Caso sensivel precisa de severidade, dono e prazo.

## Tarefa

```text
aberta
  -> assumida
  -> em andamento
  -> aguardando
  -> concluida
  -> cancelada
  -> reaberta
```

Regras:

- Toda tarefa deve ter dono ou fila responsavel.
- Tarefa vencida aparece em Hoje e mobile.

## Aprovacao

```text
pendente
  -> editada
  -> aprovada
  -> rejeitada
  -> expirada
  -> cancelada
```

Regras:

- Aprovacao deve mostrar antes/depois, impacto, custo/cota, risco e motivo.
- Aprovacao sensivel exige auditoria com decisor.

## Conversa

```text
nova
  -> em atendimento por agente
  -> aguardando humano
  -> humano ativo
  -> aguardando contato
  -> resolvida
  -> opt-out
  -> reaberta
```

Regras:

- Handoff humano pausa resposta automatica.
- Opt-out bloqueia automacao externa.
- Conversa deve estar vinculada a contato, aluno ou interessado sempre que possivel.

## Fluxo de agente

```text
rascunho
  -> em teste
  -> ativo
  -> pausado
  -> bloqueado por plano
  -> bloqueado por dado
  -> bloqueado por cota
  -> desativado
  -> nova versao
```

Regras:

- Fluxo ativo sempre tem modo: manual, copiloto ou autonomo.
- Mudanca de modo/limite/template deve gerar auditoria.
- Simulacao deve existir antes de ativar fluxo sensivel.

## Execucao de agente

```text
iniciada
  -> checando dados
  -> aguardando aprovacao
  -> executada
  -> enviada
  -> bloqueada
  -> falhou
  -> corrigida
  -> reprocessada
```

Regras:

- Toda execucao precisa explicar entrada, decisao, ferramenta, custo e resultado.
- Reprocessamento exige idempotencia e seguranca.

## Politica operacional

```text
rascunho
  -> simulada
  -> aguardando aprovacao
  -> publicada
  -> ativa
  -> substituida
  -> revertida
  -> arquivada
```

Regras:

- Agentes devem guardar snapshot da politica usada.
- Mudanca de politica com impacto amplo deve ter simulacao.

## Solicitacao LGPD

```text
recebida
  -> identidade em validacao
  -> aprovada
  -> em execucao
  -> concluida
  -> negada
  -> expirada
```

Regras:

- Nenhuma exclusao/anonimizacao pode ser automatica sem confirmacao humana.
- Tudo gera auditoria.

## Acesso de suporte Taliya

```text
solicitado
  -> aprovado
  -> ativo
  -> expirado
  -> revogado
  -> encerrado
```

Regras:

- Deve ter escopo, motivo, prazo e ator Taliya.
- Toda acao do suporte gera auditoria.
