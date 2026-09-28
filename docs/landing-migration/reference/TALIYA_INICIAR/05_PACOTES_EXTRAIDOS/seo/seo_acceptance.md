# Checklist de publicação



Cada aceite deve guardar URL, data, resultado e responsável. “Está no código” não equivale a “foi publicado corretamente”.

| Teste | Condição para aprovação |
|---|---|
| QA-01 | Home final responde 200 e não leva à antiga oferta de Pilates |
| QA-02 | HTTP/apex/www não criam loops ou múltiplos destinos concorrentes |
| QA-03 | Cada URL pública relevante tem canonical final consistente |
| QA-04 | Nenhuma página de aquisição recebe noindex acidental |
| QA-05 | robots não bloqueia recursos públicos necessários |
| QA-06 | Sitemap contém apenas páginas canônicas, públicas e existentes |
| QA-07 | Legado tem redirecionamento equivalente ou encerramento deliberado |
| QA-08 | Headline, metadados, formulário e oferta concordam sobre o estágio |
| QA-09 | H1 principal e hierarquia de headings são conferidos em tags reais |
| QA-10 | Sete frentes, subtipos essenciais e perguntas aparecem no HTML renderizado sem novo carregamento após clique |
| QA-11 | JSON em script não é a única representação textual do conteúdo |
| QA-12 | Âncoras internas e páginas institucionais usam href real; não existem rotas de recurso vazias |
| QA-13 | Imagens informativas têm texto alternativo útil; decorativas são tratadas como tais |
| QA-14 | Layout reserva espaço e não cobre texto/CTA no mobile |
| QA-15 | Tabs, mural e modais funcionam por teclado e respeitam redução de movimento |
| QA-16 | Schema corresponde ao conteúdo visível e não inventa oferta/rating |
| QA-17 | Search Console confirma acesso/inspeção; controle de IA é conferido |
| QA-18 | Bing Webmaster recebe sitemap e permite inspeção da propriedade |
| QA-19 | CDN/logs permitem verificar acessos legítimos de robôs |
| QA-20 | Analytics preserva origem de busca/ChatGPT sem enviar dados pessoais |
| QA-21 | Demos não disparam lead, compra ou operação real |
| QA-22 | Formulário registra sucesso apenas depois da gravação efetiva |
| QA-23 | Baseline de busca separa marca, intenção e páginas |
| QA-24 | Teste final de conteúdo não atribui funções fora da V1 |
| QA-25 | A matriz de intenções confirma que a `/` cobre Agenda, Orçamentos e Recebimentos sem depender de URL extra |

**Aceites pendentes nesta auditoria:** inspeção privada, headers brutos, HTML entregue pelo servidor, mobile real, performance e tráfego. Eles foram incluídos como testes, não preenchidos com resultados inventados.



## Resultado por teste
Registrar status (não testado/aprovado/falhou), URL, data, responsável e evidência. Nenhum teste deste arquivo está marcado como executado no site novo.
