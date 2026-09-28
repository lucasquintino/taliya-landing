# Setup Inicial - Stepper E Progresso Com 9 Blocos

Status: decisao aprovada v0.1.
Data: 2026-05-19.

## Decisao

O Setup Inicial passa a ter 9 blocos porque `Pagamento` entra depois de `Planos`.

Sequencia oficial:

1. `Studio`;
2. `Equipe`;
3. `Canais`;
4. `Planos`;
5. `Pagamento`;
6. `Alunos`;
7. `Turmas`;
8. `Agenda`;
9. `Revisao`.

## Regra Para Imagens Ja Aprovadas

As imagens ja aprovadas continuam validas para funcao, layout e hierarquia:

- `78` passa a ser a entrada antes do stepper/blocos;
- `51D v2` substitui a 51D antiga como referencia funcional do bloco `Studio`;
- `51H` continua valida como padrao do bloco `Alunos`;
- `51I` continua valida como padrao do bloco `Turmas`;
- `51J` continua valida como padrao do bloco `Agenda`.

Mas o stepper, o numero do bloco e o progresso visual dessas imagens devem ser reinterpretados com a sequencia de 9 blocos.

Nao e necessario regerar essas imagens apenas para corrigir numeracao/progresso.

## Mapeamento Atualizado

| Imagem aprovada | Bloco antigo na imagem | Bloco oficial atualizado | Status |
|---|---:|---:|---|
| `78_round-4.1Q_onboarding_bem-vindo-taliya-setup-guiado-aprovado.png` | N/A | Entrada antes dos blocos | Aprovada; sem stepper |
| `51D_round-4.1J_onboarding_bloco-1-studio-v2-sem-nome-aprovado.png` | 1 de 8 | 1 de 9 | Aprovada; substitui 51D antiga como referencia funcional |
| `51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png` | 1 de 8 | 1 de 9 | Historica; substituida pela 51D v2 |
| `51E_round-4.1J_onboarding_bloco-2-equipe-aprovado.png` | 2 de 8 | 2 de 9 | Sem ajuste visual necessario |
| `51F_round-4.1J_onboarding_bloco-3-canais-aprovado.png` | 3 de 8 | 3 de 9 | Sem ajuste visual necessario |
| `51G_round-4.1J_onboarding_bloco-4-planos-aprovado.png` | 4 de 8 | 4 de 9 | Sem ajuste visual necessario |
| `51K_round-4.1J_onboarding_bloco-5-pagamento-aprovado.png` | N/A | 5 de 9 | Aprovada |
| `51H_round-4.1J_onboarding_bloco-5-alunos-aprovado.png` | 5 de 8 | 6 de 9 | Nao regerar; ajustar na implementacao |
| `51I_round-4.1J_onboarding_bloco-6-turmas-aprovado.png` | 6 de 8 | 7 de 9 | Nao regerar; ajustar na implementacao |
| `51J_round-4.1J_onboarding_bloco-7-agenda-aprovado.png` | 7 de 8 | 8 de 9 | Nao regerar; ajustar na implementacao |
| `51L_round-4.1J_onboarding_bloco-9-revisao-aprovado.png` | N/A | 9 de 9 | Aprovada |

## Progressos Visuais Recomendados

Os percentuais exatos podem variar na implementacao, mas devem seguir a ideia:

- Studio: cerca de `11%`;
- Equipe: cerca de `22%`;
- Canais: cerca de `33%`;
- Planos: cerca de `44%`;
- Pagamento: cerca de `55%`;
- Alunos: cerca de `66%`;
- Turmas: cerca de `77%`;
- Agenda: cerca de `88%`;
- Revisao: cerca de `96%` a `100%`, dependendo se a publicacao final ja ocorreu.

## Regra De Implementacao

Na implementacao, usar sempre a sequencia oficial de 9 blocos.

As imagens antigas devem ser lidas como referencia visual, nao como fonte final da numeracao.

O bloco `Pagamento` deve aparecer no stepper entre `Planos` e `Alunos`.
