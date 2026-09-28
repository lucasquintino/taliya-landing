# Taliya — adendo SEO, Google e descoberta no ChatGPT
Versão 1.1 • 19/09/2026 • revisão da estratégia de rotas

## Estado
Especificação e auditoria pública. Nenhum arquivo foi aplicado ao site. A Taliya permanece em pré-lançamento. Os exemplos não habilitam checkout, trial ou aplicativo funcional.

## Decisão revisada
A home `/` é suficiente como núcleo de descoberta para as capacidades já cobertas pela Especificação Definitiva, desde que o conteúdo essencial das sete frentes seja explícito e rastreável. **Não criar `/recursos/agenda`, `/recursos/orcamentos` ou `/recursos/recebimentos` no lançamento apenas por SEO.** Rotas adicionais de feature entram somente quando intenção, conteúdo ou dados justificarem.

## Uso
1. Ler o PDF v1.1 e conferir a Especificação Definitiva v1 da landing.
2. Mapear componentes/rotas REAIS do repositório; este pacote não inventa caminhos de Next.js.
3. Aplicar primeiro SEO-01 a SEO-10, com atenção à cobertura semântica da home.
4. Usar `route_plan.json` como política de arquitetura mínima e critérios para expansão futura, não como sitemap pronto.
5. Gerar metadados/schema a partir dos fatos aprovados e executar `seo_acceptance.md`.
6. Revalidar fontes dinâmicas e registrar dados de Search Console/Bing/analytics após publicação.
7. Só então decidir se algum cluster merece URL própria.

## Arquivos
- Relatório PDF, DOCX e Markdown: auditoria, estratégia revisada, backlog e fontes.
- `seo_config.example.json`: configuração de conteúdo, sem código de integração.
- `robots.public.example.txt` + `robots_policy_notes.md`: exemplo e cuidados.
- `structured_data.prelaunch.json`: entidades básicas sem ratings/oferta.
- `route_plan.json`: arquitetura mínima, legado e critérios objetivos para novas rotas.
- `evidence_summary.json`: observações e limites auditáveis.
- `seo_acceptance.md`: checklist não executado na nova landing.
- `fontes.md`: referências oficiais e públicas.

## Validação local
Os arquivos JSON tiveram sintaxe validada. Isso NÃO é validação do Google, indexação, velocidade, funcionamento das URLs propostas nem teste de produto.
