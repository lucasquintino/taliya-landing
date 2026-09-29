# Taliya — plano integral do atendimento e operação SaaS
**Versão 3.0 · 28/09/2026 · plano de execução, não implantação.**

## Direção fechada
Um agente comercial na Agents API com GPT-6 Luna em esforço max; app e assinatura existentes; landing e design system preservados; catálogo compartilhado de vídeos/demos/UGC; criação/atualização integrada de leads/clientes; PostHog para análise; Internal mínimo para ação; SDD + Spec Kit.

## Leitura inicial
Leia `01_AUDITORIA.md`, `02_PLANO_MESTRE_0_A_100.md`, `04_SDD_SPECKIT.md` e `PROMPT_MESTRE_CONTINUIDADE.md`. Em seguida execute somente a spec ativa, começando pela 013. Os contratos, casos e evidências suportam as specs; não são outro plano concorrente.

## Autoridade e supersessão
O pedido atual do usuário prevalece sobre copy-only, pré-lançamento, espera, trial sem cartão e planos de Pilates. Este pacote substitui os roteiros amplos E00–E04 anteriores como plano de execução destas frentes. Preserva arquitetura/visuais aprovados e a política atual da assinatura. Não substitui as specs do app/billing prontos nem autoriza novas funcionalidades operacionais.

Os números 013–025 continuam o intervalo 001–012 observado no ZIP. Se a árvore real já avançou, renumerar com o Spec Kit e atualizar referências de forma atômica antes de implementar. Não sobrescrever specs existentes.

## O que não está incluído como executado
Nenhum deploy, criação de recursos remotos, migração real, teste E2E de produção, inferência paga ou postagem de campanha. Os arquivos `verification.md` estão honestamente como NÃO EXECUTADO. As verificações deste pacote são estruturais e estáticas, descritas em `evidence/VALIDACAO_DESTA_ENTREGA.md`.

## Arquivo original
O código original de 45 MB não está duplicado neste pacote. Utilize o repositório atual e o ZIP original somente como referência. Não copiar este diretório por cima da aplicação inteira. Incorporar docs/specs/contratos por diff revisável.

## Formatos de leitura
`Taliya_Auditoria_e_Plano_Integral_v3.pdf` contém a edição de leitura em 30 páginas. Os arquivos Markdown são a versão editável; `../../specs/`, `contracts/`, `evals/` e `evidence/` contêm os detalhes operacionais. Os hashes em `MANIFESTO_SHA256.json` permitem conferir os arquivos deste pacote.
