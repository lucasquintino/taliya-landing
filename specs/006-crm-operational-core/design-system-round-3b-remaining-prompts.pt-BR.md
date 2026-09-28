# Design System Web - Prompts Das Rodadas 3B Restantes

> Status: guia operacional v0.1. Use estes prompts no ChatGPT Pro depois da aprovacao da Rodada 3B.1.

## Regra Geral

As proximas rodadas 3B devem ser feitas em conversas separadas ou em conversas novas quando o ChatGPT Pro comecar a desobedecer.

Todas as rodadas restantes devem usar como anexos:

1. Rodada 3A aprovada: componentes web presentes na referencia.
2. Tela Taliya 2A.2 aprovada: identidade aplicada em tela real.
3. Referencia original: atmosfera, cinza frio, suavidade, densidade e baixo contraste.
4. Rodada 3B.1 aprovada: inputs, formularios e filtros.

Nao anexar tentativas antigas reprovadas, como 2A ou 2A.1, para nao contaminar o resultado.

Regra de interpretacao das imagens:

```text
3A = componentes existentes.
2A.2 = Taliya aplicado em tela real.
Base ref = atmosfera.
3B.1 = anatomia de inputs, formularios e filtros.
```

## Rodada 3B.2 - Overlays E Feedback

### Anexos

1. Imagem da 3A aprovada.
2. Imagem da 2A.2 aprovada.
3. `crm_1.webp` como base ref.
4. Imagem da 3B.1 aprovada.

### Prompt

```text
Esta e uma nova conversa.
Ignore qualquer tentativa anterior.
Use apenas as imagens anexas como fonte visual.

Vou anexar 4 imagens.

Imagem 1:
Rodada 3A aprovada. Ela mostra os componentes web ja existentes do Taliya CRM.

Imagem 2:
Tela Taliya 2A.2 aprovada. Ela mostra a identidade Taliya aplicada em uma tela real.

Imagem 3:
Referencia original. Ela define a atmosfera visual: cinza frio, suavidade, densidade, baixo contraste e aparencia SaaS premium.

Imagem 4:
Rodada 3B.1 aprovada. Ela mostra inputs, formularios e filtros.

Quero iniciar a Rodada 3B.2.

Nome:
Taliya CRM - Rodada 3B.2: Overlays E Feedback Web

Objetivo:
Criar uma prancha de design system web apenas com componentes de overlay, feedback e estados de resposta do sistema.

Esta rodada complementa a 3A e a 3B.1.
Nao criar visualizacoes operacionais, chat, agentes, cotas, billing ou telas finais.

Componentes obrigatorios:

1. Modal
Mostrar:
- modal pequeno de confirmacao;
- modal medio com formulario curto;
- estado de acao destrutiva;
- rodape com botao secundario e botao principal.

2. Drawer lateral
Mostrar:
- drawer direito;
- header;
- conteudo com campos compactos;
- acoes no rodape;
- estado com item selecionado.

3. Popover
Mostrar:
- popover de opcoes;
- popover com mini formulario;
- popover de detalhes rapidos.

4. Tooltip
Mostrar:
- tooltip simples;
- tooltip com texto curto;
- tooltip em icone circular.

5. Toast
Mostrar:
- sucesso;
- alerta;
- erro;
- informacao;
- acao curta dentro do toast.

6. Alerta inline
Mostrar:
- informativo;
- alerta;
- erro;
- sucesso;
- alerta com icone e CTA curto.

7. Confirmacao
Mostrar:
- confirmacao simples;
- confirmacao de acao sensivel;
- confirmacao com resumo da acao.

8. Empty state
Mostrar:
- sem resultados;
- sem permissao;
- sem integracao conectada;
- estado com botao circular/CTA curto.

9. Loading / skeleton
Mostrar:
- skeleton de card;
- skeleton de tabela;
- skeleton de painel;
- spinner discreto.

10. Error state
Mostrar:
- erro de carregamento;
- falha de integracao;
- tentar novamente;
- contato/suporte discreto.

Direcao visual obrigatoria:
- seguir a Rodada 3A;
- seguir a tela Taliya 2A.2;
- usar a 3B.1 para inputs e formularios dentro de overlays;
- preservar atmosfera da referencia original;
- fundo cinza frio #E4E4E4;
- superficies brancas suaves/translucidas;
- preto #10141A para foco;
- azul #83A2DB para informacao/progresso;
- vermelho #CE6969 para erro/alerta;
- radius alto;
- sombras muito sutis;
- baixo contraste premium;
- tipografia inspirada em Lufga.

Regras:
- Nao criar chat.
- Nao criar agente/copiloto.
- Nao criar calendario completo.
- Nao criar kanban.
- Nao criar tabela completa.
- Nao criar cotas.
- Nao criar billing.
- Nao criar permissoes complexas.
- Nao criar tela final de produto.
- Nao criar landing page.
- Nao mudar a direcao visual.
- Nao deixar branco demais.
- Nao parecer UI kit generico.

Formato:
Criar uma imagem landscape 16:9.
Pode ser uma prancha organizada em blocos.

Criterio de sucesso:
A prancha deve completar apenas overlays, feedback e estados de sistema do Taliya CRM web, parecendo extensao natural das imagens anexas.
```

## Rodada 3B.3 - Visualizacoes Operacionais

### Anexos

1. Imagem da 3A aprovada.
2. Imagem da 2A.2 aprovada.
3. `crm_1.webp` como base ref.
4. Imagem da 3B.1 aprovada.

### Prompt

```text
Esta e uma nova conversa.
Ignore qualquer tentativa anterior.
Use apenas as imagens anexas como fonte visual.

Vou anexar 4 imagens.

Imagem 1:
Rodada 3A aprovada. Ela mostra os componentes web ja existentes do Taliya CRM.

Imagem 2:
Tela Taliya 2A.2 aprovada. Ela mostra a identidade Taliya aplicada em uma tela real.

Imagem 3:
Referencia original. Ela define a atmosfera visual: cinza frio, suavidade, densidade, baixo contraste e aparencia SaaS premium.

Imagem 4:
Rodada 3B.1 aprovada. Ela mostra inputs, formularios e filtros.

Quero iniciar a Rodada 3B.3.

Nome:
Taliya CRM - Rodada 3B.3: Visualizacoes Operacionais Web

Objetivo:
Criar uma prancha de design system web apenas com visualizacoes operacionais do CRM.

Esta rodada deve mostrar como listas, tabelas, kanban, calendario e historico aparecem no Taliya.
Nao criar chat, agentes, cotas, billing, permissoes ou telas finais.

Componentes obrigatorios:

1. Tabela completa
Mostrar:
- header;
- filtros compactos;
- busca;
- linhas;
- status pill;
- avatar/responsavel;
- checkbox de selecao;
- paginacao;
- acao por linha.

2. Lista densa
Mostrar:
- item principal;
- metadados;
- avatar;
- status;
- acao rapida;
- item selecionado.

3. Kanban compacto
Mostrar:
- 3 colunas;
- card de oportunidade/tarefa;
- status;
- responsavel;
- contador por coluna;
- card selecionado.

4. Calendario compacto
Mostrar:
- mini semana;
- bloco de aula;
- horario;
- responsavel/professor;
- estado ocupado;
- estado disponivel;
- conflito.

5. Timeline / historico
Mostrar:
- eventos em sequencia;
- icone por tipo;
- horario;
- responsavel;
- nota curta;
- evento destacado.

6. Painel de atividade
Mostrar:
- feed recente;
- tarefas;
- alertas;
- filtros;
- estado vazio pequeno.

7. Cards de resumo operacional
Mostrar:
- indicador curto;
- variacao positiva/neutra/alerta;
- acao circular;
- mini grafico simples.

Direcao visual obrigatoria:
- seguir a Rodada 3A;
- seguir a tela Taliya 2A.2;
- usar a 3B.1 para filtros e busca;
- preservar atmosfera da referencia original;
- fundo cinza frio #E4E4E4;
- superficies brancas suaves/translucidas;
- preto #10141A para foco;
- azul #83A2DB para progresso/selecionado;
- vermelho #CE6969 para alerta/conflito;
- radius alto;
- sombras muito sutis;
- baixo contraste premium;
- densidade de CRM operacional.

Regras:
- Nao criar chat.
- Nao criar agente/copiloto.
- Nao criar cotas.
- Nao criar billing.
- Nao criar permissoes complexas.
- Nao criar modal/drawer como foco.
- Nao criar tela final de produto.
- Nao criar landing page.
- Nao mudar a direcao visual.
- Nao deixar branco demais.
- Nao parecer dashboard generico.

Formato:
Criar uma imagem landscape 16:9.
Pode ser uma prancha organizada em blocos.

Criterio de sucesso:
A prancha deve completar visualizacoes operacionais do Taliya CRM web com densidade de produto real e atmosfera da referencia.
```

## Rodada 3B.4 - Comunicacao E Agentes

### Anexos

1. Imagem da 3A aprovada.
2. Imagem da 2A.2 aprovada.
3. `crm_1.webp` como base ref.
4. Imagem da 3B.1 aprovada.

### Prompt

```text
Esta e uma nova conversa.
Ignore qualquer tentativa anterior.
Use apenas as imagens anexas como fonte visual.

Vou anexar 4 imagens.

Imagem 1:
Rodada 3A aprovada. Ela mostra os componentes web ja existentes do Taliya CRM.

Imagem 2:
Tela Taliya 2A.2 aprovada. Ela mostra a identidade Taliya aplicada em uma tela real.

Imagem 3:
Referencia original. Ela define a atmosfera visual: cinza frio, suavidade, densidade, baixo contraste e aparencia SaaS premium.

Imagem 4:
Rodada 3B.1 aprovada. Ela mostra inputs, formularios e filtros.

Quero iniciar a Rodada 3B.4.

Nome:
Taliya CRM - Rodada 3B.4: Comunicacao E Agentes Web

Objetivo:
Criar uma prancha de design system web apenas com componentes de comunicacao, WhatsApp, copiloto e agentes integrados ao CRM.

Esta rodada deve mostrar agentes como parte do CRM, nao como produto separado.
Nao criar billing, cotas, permissoes complexas ou telas finais.

Componentes obrigatorios:

1. Inbox / conversa
Mostrar:
- lista de conversas;
- conversa selecionada;
- contador de nao lidas;
- status de canal WhatsApp;
- responsavel humano.

2. Bolhas de mensagem
Mostrar:
- mensagem recebida;
- mensagem enviada;
- mensagem interna;
- mensagem sugerida;
- status de envio/erro.

3. Composer
Mostrar:
- campo de mensagem;
- anexar;
- template;
- enviar;
- acao circular;
- estado desabilitado.

4. Painel de copiloto
Mostrar:
- sugestao do agente;
- resumo da conversa;
- proxima melhor acao;
- aceitar;
- editar;
- rejeitar.

5. Aprovacao de acao
Mostrar:
- proposta do agente;
- impacto esperado;
- risco;
- botao aprovar;
- botao ajustar;
- botao cancelar.

6. Execucao autonoma
Mostrar:
- status em execucao;
- etapa atual;
- log curto;
- pausar;
- assumir manualmente.

7. Falha de agente
Mostrar:
- erro;
- motivo;
- fallback manual;
- tentar novamente;
- registrar incidente.

8. Handoff humano
Mostrar:
- transferir para responsavel;
- selecionar pessoa;
- nota interna;
- confirmar.

9. Card de confianca
Mostrar:
- nivel de confianca;
- recomendacao;
- politica aplicada;
- auditoria curta.

Direcao visual obrigatoria:
- seguir a Rodada 3A;
- seguir a tela Taliya 2A.2;
- usar a 3B.1 para composer, inputs e seletores;
- preservar atmosfera da referencia original;
- fundo cinza frio #E4E4E4;
- superficies brancas suaves/translucidas;
- preto #10141A para foco;
- azul #83A2DB para progresso/sugestao;
- vermelho #CE6969 para alerta/falha;
- radius alto;
- sombras muito sutis;
- baixo contraste premium;
- agentes discretos e integrados ao CRM.

Regras:
- Nao transformar em aplicativo de chat generico.
- Nao transformar agente em mascote.
- Nao criar landing page de IA.
- Nao criar billing.
- Nao criar cotas.
- Nao criar permissoes complexas.
- Nao criar tela final de produto.
- Nao mudar a direcao visual.
- Nao usar roxo/gradiente de IA.
- Nao deixar branco demais.

Formato:
Criar uma imagem landscape 16:9.
Pode ser uma prancha organizada em blocos.

Criterio de sucesso:
A prancha deve mostrar comunicacao e agentes como componentes nativos do Taliya CRM, com aparencia premium, discreta e operacional.
```

## Rodada 3B.5 - Sistema, Plano E Governanca

### Anexos

1. Imagem da 3A aprovada.
2. Imagem da 2A.2 aprovada.
3. `crm_1.webp` como base ref.
4. Imagem da 3B.1 aprovada.

### Prompt

```text
Esta e uma nova conversa.
Ignore qualquer tentativa anterior.
Use apenas as imagens anexas como fonte visual.

Vou anexar 4 imagens.

Imagem 1:
Rodada 3A aprovada. Ela mostra os componentes web ja existentes do Taliya CRM.

Imagem 2:
Tela Taliya 2A.2 aprovada. Ela mostra a identidade Taliya aplicada em uma tela real.

Imagem 3:
Referencia original. Ela define a atmosfera visual: cinza frio, suavidade, densidade, baixo contraste e aparencia SaaS premium.

Imagem 4:
Rodada 3B.1 aprovada. Ela mostra inputs, formularios e filtros.

Quero iniciar a Rodada 3B.5.

Nome:
Taliya CRM - Rodada 3B.5: Sistema, Plano E Governanca Web

Objetivo:
Criar uma prancha de design system web apenas com componentes de sistema, plano, cotas, permissoes, integracoes, auditoria, billing e configuracoes.

Esta rodada deve completar os componentes administrativos do CRM.
Nao criar paginas finais completas.

Componentes obrigatorios:

1. Card de plano
Mostrar:
- plano atual;
- quantidade de agentes;
- status do plano;
- CTA de upgrade;
- plano base com 0 agentes.

2. Card de cota / limite
Mostrar:
- uso atual;
- limite;
- barra de progresso;
- alerta proximo do limite;
- fallback manual.

3. Permissao / bloqueio
Mostrar:
- acao bloqueada;
- motivo;
- papel necessario;
- solicitar acesso;
- continuar manualmente quando permitido.

4. Billing / pagamento
Mostrar:
- metodo de pagamento;
- proxima cobranca;
- fatura;
- status pago/pendente;
- acao circular.

5. Integracao
Mostrar:
- WhatsApp conectado;
- calendario conectado;
- integracao com erro;
- reconectar;
- configurar.

6. Auditoria
Mostrar:
- evento;
- usuario/agente;
- horario;
- objeto afetado;
- antes/depois resumido.

7. Politica / guardrail
Mostrar:
- politica ativa;
- nivel de autonomia;
- requer aprovacao;
- risco;
- versao da politica.

8. Configuracao
Mostrar:
- grupo de settings;
- toggle;
- select;
- input;
- salvar alteracoes.

9. Estado 0 agentes
Mostrar:
- CRM ativo sem agentes;
- acoes manuais disponiveis;
- sugestao de ativar agente;
- sem bloquear o uso principal.

Direcao visual obrigatoria:
- seguir a Rodada 3A;
- seguir a tela Taliya 2A.2;
- usar a 3B.1 para formularios, selects e toggles;
- preservar atmosfera da referencia original;
- fundo cinza frio #E4E4E4;
- superficies brancas suaves/translucidas;
- preto #10141A para foco;
- azul #83A2DB para progresso/ok;
- vermelho #CE6969 para alerta/bloqueio;
- radius alto;
- sombras muito sutis;
- baixo contraste premium;
- administrativo, claro e operacional.

Regras:
- Nao criar pagina final completa.
- Nao criar landing page de pricing.
- Nao criar marketing.
- Nao transformar billing em checkout completo.
- Nao transformar governanca em tela tecnica complexa.
- Nao criar chat/agente como foco.
- Nao mudar a direcao visual.
- Nao usar cores novas dominantes.
- Nao deixar branco demais.

Formato:
Criar uma imagem landscape 16:9.
Pode ser uma prancha organizada em blocos.

Criterio de sucesso:
A prancha deve completar componentes administrativos do Taliya CRM, incluindo 0 agentes, cotas, plano, permissoes, integracoes, auditoria e configuracoes, sem parecer sistema separado.
```

