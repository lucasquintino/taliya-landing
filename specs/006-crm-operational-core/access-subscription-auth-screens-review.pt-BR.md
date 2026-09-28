# Acesso E Assinatura - Auth Screens 72/73 - PT-BR

> Status: imagens 72 e 73 salvas para referencia visual, com ajustes finos documentados antes de aprovacao final.

## Imagens Salvas

| Imagem | Tela | Status |
| --- | --- | --- |
| `72_round-4.1Q_acesso-assinatura_signup-criar-conta-salvo-ajustes.png` | Criar conta | Salva; fluxo aprovado; ajustes visuais finos pendentes. |
| `73_round-4.1Q_acesso-assinatura_signin-entrar-salvo-ajustes.png` | Entrar | Salva; direcao aprovada; ajustes visuais finos pendentes. |

Arquivos:

- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\72_round-4.1Q_acesso-assinatura_signup-criar-conta-salvo-ajustes.png`
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\73_round-4.1Q_acesso-assinatura_signin-entrar-salvo-ajustes.png`

## Decisao De Fluxo

### Criar Conta

Criar conta nao pede senha na primeira tela.

Caminhos permitidos:

- continuar com Google;
- continuar com Microsoft;
- continuar com e-mail.

Fluxo por e-mail:

```text
usuario informa e-mail profissional
→ Taliya envia link seguro
→ usuario continua pelo link
→ usuario define senha depois
```

Nao usar Facebook como provedor de conta.

### Entrar

Entrar pode usar:

- Google;
- Microsoft;
- e-mail e senha;
- recuperar senha.

## O Que Esta Correto Na 72

- Nao pede senha no signup.
- Usa Google, Microsoft e e-mail.
- Mantem shell 71, sem sidebar, sem CRM, sem checkout e sem onboarding.
- Explica que o usuario recebera link seguro para continuar e definir senha.
- Mantem termos, privacidade e link para entrar.

## O Que Falta Ajustar Na 72

| Ajuste | Motivo |
| --- | --- |
| Reduzir quebras duras em microcopy e termos | Melhorar leitura e acabamento SaaS. |
| Refinar largura/line-height do card | Evitar sensacao comprimida no miolo. |
| Garantir que o fundo nao fique lavado demais | Manter profundidade do shell 71/imagem 16. |
| Polir raio, borda e sombra dos inputs/botoes | Aproximar do acabamento premium do design system. |

## O Que Esta Correto Na 73

- Estrutura de login SaaS esta correta.
- Usa Google, Microsoft e e-mail/senha.
- Tem `Manter conectado`, `Esqueci minha senha` e link para criar conta.
- Nao mistura login com checkout, onboarding ou CRM.
- Mantem o shell visual pre-CRM.

## O Que Falta Ajustar Na 73

| Ajuste | Motivo |
| --- | --- |
| Aumentar raio dos botoes sociais e inputs | Aproximar do DNA arredondado da imagem 16/71. |
| Tornar o botao principal mais pill | O botao atual ainda esta um pouco retangular/pesado. |
| Suavizar borda/sombra do card | Evitar cara de form generico. |
| Ajustar profundidade do fundo | Manter a tela menos lavada e mais Taliya premium. |
| Conferir alinhamento da linha `Manter conectado` / `Esqueci minha senha` | Deixar o espacamento mais polido. |

## Regra Para As Proximas Versoes

As proximas imagens finais devem manter:

- shell 71;
- auth card centralizado;
- sem coluna lateral;
- sem sidebar;
- sem CRM;
- sem onboarding;
- sem checkout;
- sem plano/preco;
- Google e Microsoft como provedores;
- signup por e-mail sem senha inicial.

## Proximas Imagens Da Familia

Com 72 e 73 salvas, a numeracao seguinte deve ser:

| Imagem | Tela |
| --- | --- |
| 74 | Revisar assinatura |
| 75 | Aguardando confirmacao |
| 76 | Resolver assinatura / bloqueado |
| 77 | Assinatura confirmada / ir para onboarding |

