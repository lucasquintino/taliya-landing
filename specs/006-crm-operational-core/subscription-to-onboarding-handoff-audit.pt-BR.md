# Handoff Da Assinatura Para O Setup Guiado - Auditoria E Contrato - PT-BR

> Status: auditoria de produto apos aprovacao da imagem 77. Este documento conecta o fluxo pre-CRM de assinatura ao Setup Inicial 51A-51L.

## Conclusao

A transicao da imagem 77 para o Setup Inicial esta coerente, mas precisa ser lida como um handoff entre dois shells:

- imagem 77 fecha a assinatura no shell pre-CRM;
- ao clicar em `Comecar setup guiado`, o usuario entra no shell de onboarding;
- o setup passa a ser conduzido pelo Agente de Configuracao lateral;
- o CRM operacional continua bloqueado ate a configuracao inicial ser publicada.

Nao e necessario redesenhar todas as imagens 51A-51L. A imagem 78 fecha a entrada do setup, e a 51D v2 substitui a 51D antiga no bloco `Studio`.

## Fluxo Aprovado

```text
77 Assinatura confirmada
-> Comecar setup guiado
-> /onboarding
-> 78 Bem-vindo a Taliya / nome do studio
-> diagnostico quando aplicavel
-> setup de 9 blocos
-> revisao/publicacao
-> CRM operacional
```

Se o usuario ja iniciou o setup:

```text
77 Assinatura confirmada
-> Comecar setup guiado
-> /onboarding
-> retomar proxima etapa incompleta
```

Se o setup ja foi publicado:

```text
login futuro
-> CRM operacional
```

## Como A 77 Conversa Com O Setup

| Elemento da 77 | Continuidade no setup |
| --- | --- |
| `Assinatura confirmada` | Permite iniciar `/onboarding`; nao libera `/app` ainda. |
| `Setup guiado pela Taliya` | Corresponde ao Agente de Configuracao das imagens 51A/51B/51C-51L. |
| `Comecar setup guiado` | CTA principal para `/onboarding`. |
| `Agendar ajuda humana` | Deve adicionar acompanhamento humano ao mesmo fluxo; nao cria setup paralelo. |
| `O CRM sera liberado apos a configuracao inicial` | Confirmado pela revisao/publicacao do setup. |

## Imagens Avaliadas

| Imagem | Papel | Resultado da auditoria |
| --- | --- | --- |
| `51A_round-4.1J_onboarding_shell-global-aprovado.png` | Shell do Setup Inicial | Continua valida. Mostra estrutura, progresso, etapa central e agente lateral. |
| `51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png` | Padrao do agente lateral | Continua valida. Sustenta a promessa da 77 de setup guiado. |
| `78_round-4.1Q_onboarding_bem-vindo-taliya-setup-guiado-aprovado.png` | Entrada do setup guiado | Aprovada. E a primeira tela visual apos a 77 quando o usuario ainda precisa informar o nome do studio. |
| `51C_round-4.1J_onboarding_workspace-configuracao-aprovado.png` | Exemplo de workspace/setup em andamento | Continua valida como tela interna, nao como primeira tela obrigatoria depois da 77. |
| `51D_round-4.1J_onboarding_bloco-1-studio-v2-sem-nome-aprovado.png` | Bloco Studio v2 | Aprovada. Substitui a 51D antiga como referencia funcional, sem repetir nome do studio. |
| `51E-51L` | Demais blocos do setup | Continuam validos como referencias dos blocos, com a reinterpretacao de 9 blocos ja documentada. |

## Lacuna Resolvida

A lacuna visual de entrada no setup foi resolvida pela imagem 78.

| Imagem | Papel | Status |
| --- | --- | --- |
| `78_round-4.1Q_onboarding_bem-vindo-taliya-setup-guiado-aprovado.png` | Boas-vindas a Taliya, nome do studio e inicio do setup guiado. | Aprovada |

## Decisoes Fechadas

1. A 77 nao deve levar direto para `/app`.
2. A 77 deve levar para `/onboarding`.
3. O primeiro acesso ao setup comeca pela imagem 78, com o nome do studio antes dos blocos.
4. O agente de configuracao deve aparecer no setup como guia contextual, nao como formulario principal.
5. `Agendar ajuda humana` nao cria outro setup; apenas adiciona acompanhamento humano ao mesmo fluxo.
6. A sequencia oficial do setup continua com 9 blocos:
   - Studio;
   - Equipe;
   - Canais;
   - Planos;
   - Pagamento;
   - Alunos;
   - Turmas;
   - Agenda;
   - Revisao.
7. O CRM so libera depois da revisao/publicacao segura do Setup Inicial.

## Ajustes Necessarios Em Implementacao Futura

- Botao `Comecar setup guiado` da 77 deve abrir `/onboarding`.
- Se nao existir o espaco inicial do studio, `/onboarding` mostra a 78, coleta o nome do studio e cria/identifica esse espaco.
- Se o setup ja estiver em andamento, `/onboarding` retoma a proxima etapa incompleta.
- Se o setup ja tiver sido publicado, o usuario nao deve ver a 77 novamente como etapa obrigatoria; deve ir ao CRM.
- A 51D v2 deve substituir a 51D antiga no bloco Studio, removendo o campo principal de nome do studio.
- As imagens 51D v2, 51H, 51I e 51J devem ser implementadas com a numeracao oficial vigente, conforme `setup-stepper-progress-9-blocks.pt-BR.md`.
- A ajuda humana deve aparecer como estado/acompanhamento dentro do setup, nao como fluxo separado.

## O Que Nao Precisa Ser Reaberto

- O shell de onboarding 51A.
- O painel do Agente de Configuracao 51B.
- Os demais blocos 51E-51L como referencia funcional.
- A decisao de 9 blocos.
- A regra de que o agente guia, mas nao publica sozinho.
- A regra de que humano Taliya ajuda dentro do mesmo fluxo.

## Veredito

O fluxo esta pronto para seguir com as imagens atuais.

A ponte visual esta fechada:

```text
77 Assinatura confirmada
-> 78 Bem-vindo a Taliya / nome do studio
-> 51D v2 Studio / dias e horarios gerais
```
