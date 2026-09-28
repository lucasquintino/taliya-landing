# Taliya — especificação definitiva da landing v1.0

Data: 18/09/2026. Modo ativo: `prelaunch`.

## O que foi entregue

- PDF e DOCX: especificação de leitura, copy, estados, contextos das demos, comportamento e aceite.
- `Taliya_Landing_Especificacao_v1.md`: versão textual editável do documento.
- `landing.content.pt-BR.json`: dataset canônico de conteúdo, IDs e regras. Não é código de produção.
- `schema.description.md`: estrutura e distinção entre campos públicos e instruções internas.
- `qa-checklist.json`: 42 verificações para a implementação. Não são testes já executados do site.
- `sources.json`: base documental e precedência das fontes.
- `PROMPT_IMPLEMENTACAO.md`: instrução para aplicar o pacote no repositório real.
- `validate_content.py`: verificação local de IDs, referências e quantidades.
- `VALIDACAO_CONTEUDO.json`: resultado da validação estrutural local.

## Conteúdo

14 slots de página (prova social oculta), 5 casos no seletor, 7 comparativos, 6 abas em Como funciona, 7 frentes com 39 subtipos, 84 mensagens com 24 iniciais, 5 fluxos com 20 passos, 14 FAQs e 2 formulários.

## O que NÃO foi feito

Não foi alterado ou publicado o site. Não foram produzidas capturas reais do aplicativo. Não foram implementados o backend de captura, a assinatura ou o vínculo do WhatsApp. Os cenários são ilustrações da experiência planejada, não testes do software. Não foi realizada nova auditoria ao vivo nesta entrega.

## Uso

1. Leia o PDF e abra o JSON.
2. Localize os componentes reais do repositório; os nomes dos slots são semânticos.
3. Preserve a identidade visual e os componentes existentes.
4. Aplique o conteúdo e os estados com `activeMode=prelaunch`.
5. Conecte os dois formulários a serviços reais; não simule sucesso.
6. Execute `python validate_content.py` e o QA da implementação.
7. Mantenha o modo `launch` bloqueado até comprovar os gates.

`runtime.onboardingUrl`, `runtime.leadEndpoint` e `runtime.supportWhatsAppUrl` estão sem valor propositalmente: os destinos reais não foram fornecidos nem verificados. Não preenchê-los por adivinhação. `runtime.policyUrl` e `runtime.termsUrl` são rotas contratuais propostas; o conteúdo precisa ser revisado antes da publicação.

Demos usam o relógio fictício de 18/09/2026 (America/Sao_Paulo). Não atualizar somente uma data isolada. Os resultados por subtipo são cenários independentes, não um ledger compartilhado entre todas as tabs.

Não usar nomes de arquivos/IDs do pacote como instrução para criar módulos novos no app. Sete frentes da landing não significam sete módulos do produto.
