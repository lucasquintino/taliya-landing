# Contratos compartilhados da migração

## Conteúdo

- `landing.content.pt-BR.json` governa os textos Copiloto disponíveis.
- As etapas de copy não alteram árvore de componentes, estilos, ordem da página, lógica, interações, destinos ou estado.
- Rótulos e descrições acessíveis contam como conteúdo textual e podem acompanhar seus controles existentes.
- Não preencher campos ausentes por invenção. Não apresentar textos de exemplo como operação real.

## Preservação

- `/pilates` e `/pilates/planos` continuam sem alterações durante a migração da nova home.
- O repositório de origem e suas integrações não são alterados.
- A stack e os assets existentes são preservados.
- O Mural é a única nova seção visual autorizada.
- A spec 018 pode reorganizar/refatorar internamente código da migração depois de S017, desde que a saída visual e as interações existentes permaneçam equivalentes.

## SEO e descoberta por IA

- O adendo SEO rege fatos e configuração pública. O JSON recebido tem `activeMode=prelaunch`, mas a atualização mais recente do usuário informa que o app já está pronto; não aplicar a copy de pré-lançamento por padrão. Preço, trial, checkout e URL de onboarding continuam sujeitos aos gates próprios do pacote.
- O conteúdo útil precisa aparecer como conteúdo real da página, sem depender exclusivamente de JSON em script ou texto invisível para robôs.
- Não criar páginas por capacidade/subtipo só para SEO.
- `robots.txt` não substitui autenticação. Preferência de treinamento e acesso de robôs de busca são decisões separadas.
- Descoberta pelo ChatGPT significa permitir e facilitar acesso/citação quando compatível com a política definida; não é promessa de ranking, indexação ou recomendação.
- A origem canônica proposta e destinos de legado não são tratados como produção verificada.

## Evidências e liberação

- Separar review da spec, implementação local, execução de checks e validação externa.
- Baseline visual original pendente até capturas serem feitas.
- Sem push, merge, publicação, deploy, DNS ou envio de mensagens.
- Dependências externas e decisões abertas permanecem registradas, sem serem simuladas.
