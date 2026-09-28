CONTEÚDO + INTERAÇÃO + IMPLEMENTAÇÃO

TALIYA

Especificação definitiva
da nova landing

Do pivot à copy de cada aba.

Versão 1.0  |  18 de setembro de 2026

**Modo ativo: pré-lançamento**

> A rotina pode começar por uma mensagem. A página precisa deixar claro o que a Taliya organiza, como continuar depois e quando usar o app — sem prometer um produto já disponível.

Inclui: 14 blocos de página; 5 demos de entrada; 6 abas de funcionamento; 7 frentes com 39 subtipos; 84 mensagens; 5 fluxos completos; 14 FAQs; formulários, estados, rotas e critérios de aceite.

A copy de lançamento está preparada em paralelo, mas só pode ser ativada após os gates de produto, oferta e onboarding. Não houve publicação ou alteração do site nesta entrega.

# Guia de leitura



| Parte | Onde encontrar |
| --- | --- |
| 01–03 | Fonte de verdade, mapa de reaproveitamento, modo de publicação e CTAs. |
| S01–S06 | Primeira impressão, demos, Sem/Com, funcionamento e mural. |
| S07 | Copy de cada frente e de todos os 39 subtipos. |
| S08–S14 | Continuidade, entrada, oferta, FAQ, formulários e encerramento. |
| Anexo A | 84 mensagens com destino de frente/subtipo. |
| Anexos B–D | Contratos de implementação, assets, rotas, eventos, QA e fontes. |

Como usar: textos em caixas “Copy” são conteúdo publicável; instruções e notas não vão para a landing. Nos campos com duas versões, escolher o modo inteiro. Nunca misturar pré-lançamento com oferta ativa.

Os IDs não são nomes de arquivos do repositório. Identifique os componentes reais antes de aplicar o conteúdo. Esta especificação não autoriza um redesign nem cria novos módulos no app.

**Leitura do JSON**

> landing.content.pt-BR.json contém a mesma base estruturada, com IDs estáveis, mensagens, estados e guardrails. O app não deve executar os comandos das demonstrações: são cenários locais e fictícios.

# 01. Fonte de verdade e decisões consolidadas

- Vender o que a pessoa resolve, não uma equipe de agentes nem a arquitetura interna.

- Preservar identidade, containers, espaçamentos, tabs, carrosséis, mockups, cards, accordions e navegação já existentes. Os nomes dos componentes abaixo são contratos conceituais, não caminhos de código observados.

- As sete frentes são categorias comerciais: Clientes, Serviços, Agenda, Orçamentos, Recebimentos, Lembretes e Arquivos e documentos. Histórico e contexto são transversais; orçamento continua no mesmo Serviço.

- O profissional fala com o número da Taliya. Não conectar o WhatsApp comercial dele nem sugerir acesso às outras conversas.

- Após criar e vincular a conta, a rotina coberta pode acontecer pela conversa. Não prometer ausência de cadastro/app para identidade, permissões, privacidade ou assinatura.

- A página deve explicar registrar, consultar, corrigir e continuar, não apenas capturar dados.

- Não exigir orçamento, início, conclusão e pagamento em todo uso. Começar por uma necessidade é uma forma válida de adoção.

- Todas as demos desta especificação são fictícias e roteirizadas. Não chamar vídeo simulado de prova de execução.

- Remover a calculadora de ROI e os sliders numéricos; reutilizar seu espaço e cards para fluxos. Não manter uma calculadora escondida nem trocar somente seus rótulos.

- Não acrescentar emissão fiscal, banco, Pix automático, links de pagamento, autoagendamento público, equipe ou tarefas para imitar o concorrente.

Base: [S1] pp.2,6–14 e17–19; [S2] §§1–9 e12; [S3] pp.25,45–46 e55–57. Esta é uma especificação decorrente da auditoria, não uma nova rodada de navegação.

# 02. Mapa final de página e reaproveitamento



| ID / âncora | Bloco | Intervenção |
| --- | --- | --- |
| S01<br>#top | Header e hero | Manter shell; substituir conteúdo |
| S02<br>#controle | Confiança e controle | Adicionar faixa compacta |
| S03<br>#na-pratica | Na prática | Reutilizar seletor de 5 opções e conversa |
| S04<br>#sem-com | Sem / Com Taliya | Reutilizar toggle e 7 posições |
| S05<br>#como-funciona | Como funciona | Reutilizar 6 tabs e estruturas internas |
| S06<br>#fale-do-seu-jeito | Mural de mensagens | Adicionar usando balões existentes |
| S07<br>#o-que-resolve | Sete frentes | Reutilizar Time Taliya e subtabs |
| S08<br>#fluxos | Fluxos reais | Substituir lógica da calculadora; reusar área e cards |
| S09<br>#como-comecar | Como começar | Reutilizar 4 etapas |
| S10<br>#comecar | Começar / oferta | Formulário no pré-lançamento; oferta no lançamento |
| S11<br>#quem-usa | Prova real | Reservar sem renderizar |
| S12<br>#duvidas | FAQ | Reusar accordion; ampliar para 14 perguntas |
| S13<br>#sua-rotina | Seu trabalho funciona de outro jeito? | Reutilizar textarea e captura |
| S14<br>#final | CTA final e footer | Reutilizar; limpar links e textos |

S11 é apenas um slot reservado e não aparece sem prova real. Preservar a identidade da página, não a semântica antiga. O espaço da calculadora muda de função e vai depois das sete frentes; essa é a alteração de ordem deliberada.

# 03. Modo de publicação e contrato dos CTAs



| Campo | Pré-lançamento — ativo | Lançamento — bloqueado |
| --- | --- | --- |
| Selo | Em desenvolvimento | Para quem trabalha por conta |
| CTA principal | Quero testar primeiro | Começar 14 dias grátis |
| CTA secundário | Ver como vai funcionar | Ver na prática |
| Destino principal | #comecar: formulário real de interesse | onboardingUrl validada |
| Aviso de demo | Demonstração ilustrativa da experiência planejada. | Exemplo ilustrativo com dados fictícios. |
| Preço / prova | Sem preço; sem depoimentos de exemplo | Preço confirmado; prova só se houver caso real |

**Aviso publicável de pré-lançamento**

> A Taliya ainda não está disponível para uso. Cadastre-se para receber um aviso sobre os primeiros testes.

Manter esse aviso perto dos CTAs e das demonstrações. O presente do indicativo nas falas dos roteiros representa uma encenação, não disponibilidade real. A label da demo deve ser visível; não escondida apenas no rodapé.



| CTA | Destino e regra |
| --- | --- |
| PRIMARY — modes[activeMode].primaryCta | #comecar em prelaunch; runtime.onboardingUrl em launch |
| DEMO — modes[activeMode].secondaryCta | #na-pratica |
| FRONTS — Veja tudo que você pode resolver | #o-que-resolve |
| FLOWS — Ver um fluxo completo | #fluxos |
| SUPPORT — Falar com a equipe | supportEmail ou supportWhatsAppUrl autorizado |

Gate específico: a fonte de produto usa o app para concluir identidade/configuração. Não divulgar “nunca precisa de app”, “sem cadastro” ou “100% no WhatsApp”. [S3] p.45. Preferências simples por mensagem não equivalem a permissões do aparelho.

# S01. Header e hero

**Reaproveitar:** header, âncoras, hierarquia visual do hero, área de demonstração e dois CTAs.



| Navegação | Destino |
| --- | --- |
| Como funciona | #como-funciona |
| O que resolve | #o-que-resolve |
| Exemplos | #fluxos |
| Como começar | #como-comecar |
| Dúvidas | #duvidas |

Adicionar “Preço” → #comecar somente no modo lançamento. Menu mobile: “Abrir menu” / “Fechar menu”. Logo: “Taliya — início”.

**Eyebrow**

> Para quem trabalha por conta e presta serviços

**Headline / H1**

> Seu negócio organizado. É só falar.

**Subheadline — pré-lançamento**

> Estamos criando a Taliya para você organizar horários, orçamentos e recebimentos conversando pelo WhatsApp. O app reúne os mesmos registros para ver e editar quando precisar.

**Subheadline — lançamento**

> Organize horários, orçamentos e recebimentos conversando com a Taliya pelo WhatsApp. O app reúne os mesmos registros para ver e editar quando precisar.

**Apoio**

> Comece pela rotina que mais pesa hoje. Não precisa usar tudo.

**Microcopy de canal**

> Você conversa com o número da Taliya usando seu WhatsApp comum.

**CTAs:** usar o par do modo ativo; secundário sempre leva a #na-pratica.

## S01. Demonstração do hero

Exemplo fictício: orçamento de instalação de R$900 já registrado para Marina.



| Quem fala | Mensagem da demonstração |
| --- | --- |
| Você | A Marina aprovou o orçamento de R$900 e pagou R$300 de entrada. |
| Taliya | Registrei a aprovação e os R$300 recebidos. Restam R$600 nesse serviço. |

**Card de resultado**

> Cliente: Marina
> Serviço: Instalação
> Situação: Confirmado
> Combinado: R$900
> Recebido: R$300
> Restante: R$600

**Comportamento:** Não duplicar o hero com uma segunda demo grande. Reutilizar mockup e card de resultado, preservar a ordem dos CTAs. Primeiro frame precisa explicar mensagem e resposta sem autoplay.

Estado ilustrativo, não uma operação real. Não mostrar data agendada sem horário/duração.

# S02. Faixa de confiança e controle

**Reaproveitar:** estilo de cards compactos; acrescentar o bloco, sem selos de certificação nem prova social inventada.



| Título | Texto publicável |
| --- | --- |
| Seu WhatsApp continua seu | A conversa é com a Taliya. Isso não dá acesso aos seus outros chats. |
| Você pode corrigir | Confira o resultado e ajuste o que precisar pela conversa ou pelo app. |
| Use só o que precisar | Comece por agenda, recebimentos, lembretes ou pela rotina que fizer sentido. |
| O app acompanha | O que você organiza na conversa também pode ser visto e editado no app. |

No pré-lançamento, o título da faixa é “Como estamos construindo a Taliya” e a página mantém o aviso de experiência planejada. Não usar cadeados ou selos que afirmem certificação.

Não transformar a faixa em uma seção de segurança técnica. Seu papel é esclarecer acesso aos chats, correção, uso parcial e relação com o app. Não usar “homologado”, “certificado”, “100% seguro” ou “ilimitado” sem evidência e condições aplicáveis.

# S03. Na prática — seletor de cinco situações

**Título**

> Aconteceu no trabalho? Fala pra Taliya.

**Subtítulo**

> Escolha uma situação e veja o que fica organizado.

**Microcopy:** Toque em um exemplo para ver a conversa.

**Estado inicial:** NP01 — Fechei um serviço. Todos os cinco casos são independentes, com dados fictícios.



| ID | Opção | Benefício |
| --- | --- | --- |
| NP01 | Fechei um serviço | Cliente, combinado e horário sem repetir cadastro. |
| NP02 | Mudou o horário | O mesmo atendimento, com a data atualizada. |
| NP03 | Recebi uma parte | O que entrou e o que falta ficam claros. |
| NP04 | Quero um orçamento | Uma proposta ligada ao trabalho, não um PDF perdido. |
| NP05 | Vendi um pacote | A contratação fica pronta antes de marcar todas as sessões. |

Reutilizar o seletor com ícone, chat e resultado. Os exemplos não são uma interface de chat aberta; clicar troca dados locais. CTA “Explorar esse caso” seleciona o subtipo correspondente em S07.

## NP01 — Fechei um serviço

**Resumo**

> Cliente, combinado e horário sem repetir cadastro.

Contexto da demo — não publicar como dado real: Cenário fictício: hoje é 18/09/2026. Luana ainda não está cadastrada.



| Quem fala | Mensagem da demonstração |
| --- | --- |
| Você | Fechei uma limpeza de sofá para a Luana amanhã às 16h, por duas horas, por R$250. |
| Taliya | Registrei a Luana e a limpeza por R$250. Ficou marcada para 19/09, das 16h às 18h. |

**Resultado ilustrativo**

> Cliente: Luana
> Serviço: Limpeza de sofá
> Quando: 19/09 · 16h–18h
> Combinado: R$250
> Situação: Confirmado

**CTA:** Explorar esse caso → S07 / AG01

Regra de fidelidade: Agenda sem conflito no cenário. Nome e instrução inequívocos; não inventar telefone/endereço nem perguntar cadastro opcional.

Repetir a legenda do modo ativo junto à demo. Não adicionar horário fictício “online agora” nem selo de pagamento bancário.

## NP02 — Mudou o horário

**Resumo**

> O mesmo atendimento, com a data atualizada.

Contexto da demo — não publicar como dado real: Visita do Carlos já agendada em 24/09, 14h–15h; duração de 1h conhecida.



| Quem fala | Mensagem da demonstração |
| --- | --- |
| Você | Passa a visita do Carlos de quinta para sexta às 10h. |
| Taliya | Remarquei a mesma visita para 25/09, das 10h às 11h. |

**Resultado ilustrativo**

> Cliente: Carlos
> Antes: 24/09 · 14h–15h
> Agora: 25/09 · 10h–11h
> Situação: Agendado

**CTA:** Explorar esse caso → S07 / AG04

Regra de fidelidade: Novo horário livre no cenário; manter serviço/ocorrência e duração. Não afirmar envio de aviso ao cliente.

## NP03 — Recebi uma parte

**Resumo**

> O que entrou e o que falta ficam claros.

Contexto da demo — não publicar como dado real: Limpeza da Ana: R$450 combinados e nenhum pagamento anterior.



| Quem fala | Mensagem da demonstração |
| --- | --- |
| Você | A Ana pagou R$300 pela limpeza. Ficaram faltando R$150. |
| Taliya | Registrei R$300 recebidos. Restam R$150 da limpeza da Ana. |
| Você | Quanto falta receber desse serviço? |
| Taliya | Faltam R$150, dos R$450 combinados. |

**Resultado ilustrativo**

> Cliente: Ana
> Combinado: R$450
> Recebido: R$300
> Restante: R$150
> Situação: Parcial

**CTA:** Explorar esse caso → S07 / RC02

Regra de fidelidade: Registro informado pelo dono. Sem integração bancária, processamento de Pix ou cobrança enviada.

## NP04 — Quero um orçamento

**Resumo**

> Uma proposta ligada ao trabalho, não um PDF perdido.

Contexto da demo — não publicar como dado real: Marina pediu uma instalação. Itens e preço são informados na mensagem.



| Quem fala | Mensagem da demonstração |
| --- | --- |
| Você | Faz um orçamento para a Marina: R$650 de instalação e R$200 de material. |
| Taliya | Preparei o orçamento de R$850 para você revisar. Ele ficou ligado ao serviço da Marina. |

**Resultado ilustrativo**

> Cliente: Marina
> Instalação: R$650
> Material cobrado: R$200
> Total proposto: R$850
> Documento: Orçamento · versão 1
> Situação: Para revisão

**CTA:** Explorar esse caso → S07 / OR01

Regra de fidelidade: Material é item cobrado ao cliente, não custo/estoque. Não marcar enviado, aprovado ou recebido por gerar proposta.

## NP05 — Vendi um pacote

**Resumo**

> A contratação fica pronta antes de marcar todas as sessões.

Contexto da demo — não publicar como dado real: Primeira contratação de João; duração das aulas ainda desconhecida.



| Quem fala | Mensagem da demonstração |
| --- | --- |
| Você | O João fechou oito aulas por R$600. Marca as duas primeiras em 22 e 24 de setembro às 7h. |
| Taliya | Registrei o pacote de oito aulas por R$600. Quanto tempo dura cada aula? |
| Você | Uma hora. |
| Taliya | Marquei 22/09 e 24/09, das 7h às 8h. São duas aulas agendadas e seis ainda disponíveis para agendar. |

**Resultado ilustrativo**

> Cliente: João
> Pacote: 8 aulas · R$600
> Realizadas: 0
> Agendadas: 2
> Disponíveis para agendar: 6

**CTA:** Explorar esse caso → S07 / SV03

Regra de fidelidade: Não criar infinitas aulas pela regra semanal nem consumir aula agendada. Pergunta necessária faz parte da demo.

# S04. Sem Taliya / Com Taliya

**Título**

> Seu trabalho já é corrido. Organizar não pode virar outro trabalho.

**Subtítulo**

> Veja o que muda quando o contexto deixa de ficar espalhado.

Preservar sete posições, toggle, setas, contador e ilustrações. Iniciar em Clientes / Com Taliya. Texto, exemplo e resultado mudam juntos. Não posicionar “sem Taliya” como incapacidade universal de qualquer planilha ou agenda.

## Clientes — Seu cliente não precisa começar do zero a cada conversa.



| Estado | Título / texto publicável |
| --- | --- |
| Sem Taliya | O contexto fica espalhado<br>Telefone num contato, combinado numa conversa e histórico na memória. |
| Com Taliya | Encontre o que já sabe<br>Consulte os serviços e os dados registrados para aquele cliente. |

**Mensagem de apoio:** Me mostra os serviços da Marina.

CTA “Ver esse exemplo” → CL02 em S07.

## Serviços — O combinado acompanha o trabalho.



| Estado | Título / texto publicável |
| --- | --- |
| Sem Taliya | Cada parte num lugar<br>Escopo, valor e mudanças acabam em anotações separadas. |
| Com Taliya | Um trabalho, um contexto<br>A contratação mantém o combinado e as mudanças que você registra. |

**Mensagem de apoio:** O Carlos fechou a instalação por R$750.

CTA “Ver esse exemplo” → SV02 em S07.

## Agenda — Mudou o horário? Atualize sem recomeçar.



| Estado | Título / texto publicável |
| --- | --- |
| Sem Taliya | Mudança para lembrar depois<br>É preciso lembrar qual horário mudou e a que trabalho ele se refere. |
| Com Taliya | O mesmo atendimento atualizado<br>Agende, remarque ou cancele o horário no contexto do serviço. |

**Mensagem de apoio:** Passa o Carlos para sexta às 10h.

CTA “Ver esse exemplo” → AG04 em S07.

## Orçamentos — Saiba qual proposta vale.



| Estado | Título / texto publicável |
| --- | --- |
| Sem Taliya | Versões soltas<br>Uma proposta corrigida pode se misturar com PDFs e valores anteriores. |
| Com Taliya | Proposta com histórico<br>Revise versões e registre qual delas foi aprovada pelo cliente. |

**Mensagem de apoio:** Me mostra a versão aprovada do orçamento.

CTA “Ver esse exemplo” → OR05 em S07.

## Recebimentos — Recebeu uma parte? Consulte o restante.



| Estado | Título / texto publicável |
| --- | --- |
| Sem Taliya | Saldo na cabeça<br>Você lembra que entrou dinheiro, mas precisa conferir de qual serviço. |
| Com Taliya | Recebido e restante juntos<br>Os pagamentos informados ficam ligados ao que foi combinado. |

**Mensagem de apoio:** Quanto falta a Ana pagar pela limpeza?

CTA “Ver esse exemplo” → RC04 em S07.

## Lembretes — Lembre do assunto, não só do alarme.



| Estado | Título / texto publicável |
| --- | --- |
| Sem Taliya | Lembrança sem contexto<br>Um aviso solto não explica o cliente, o serviço ou o valor envolvido. |
| Com Taliya | Aviso com contexto<br>Peça um lembrete sobre o que realmente precisa retomar. |

**Mensagem de apoio:** Me lembra segunda de cobrar os R$150 da Ana.

CTA “Ver esse exemplo” → LE01 em S07.

## Arquivos e documentos — Ache o material daquele trabalho.



| Estado | Título / texto publicável |
| --- | --- |
| Sem Taliya | Arquivo perdido no histórico<br>Fotos, PDFs e contratos ficam entre mensagens e pastas diferentes. |
| Com Taliya | Material ligado ao serviço<br>Guarde e recupere os arquivos pelo contexto do trabalho. |

**Mensagem de apoio:** Cadê o contrato da Empresa Norte?

CTA “Ver esse exemplo” → AR02 em S07.

# S05. Como funciona — seis abas

**Título**

> Você fala. A Taliya mantém o contexto.

**Subtítulo**

> Sem decorar comandos, sem começar pelo cadastro inteiro e sem registrar a mesma coisa em dois lugares.

Os seis tópicos existentes são rebatizados, não duplicados em seis seções longas. Cada aba troca somente seu painel. Abrir CF01. Contexto e regras internas abaixo não são texto promocional.

## CF01 — Fale normalmente

**Título do painel**

> Conte do jeito que for mais fácil.

**Kicker:** Texto, áudio e materiais do trabalho

**Descrição**

> Pode ser uma mensagem curta, um áudio ou um arquivo acompanhado do que você precisa fazer. A Taliya usa o pedido e o contexto para continuar.

**Componente interno:** Seletor de formatos + mockup compartilhado; sem criar caixa de chat livre na landing.



| Seleção / etapa | Exemplo ou fala | Resultado |
| --- | --- | --- |
| Texto | A Ana pagou R$300 pela limpeza. | Pagamento informado ligado ao serviço da Ana. |
| Áudio | Passa a visita do Carlos para sexta às 10h. | Mesma visita remarcada; duração já conhecida. |
| Foto | Guarda essas fotos no serviço da Júlia. | Fotos anexadas ao trabalho indicado. |
| PDF | Guarda este contrato na instalação da Empresa Norte. | Documento associado ao serviço. |
| Contato | Cadastra a Marina com esse contato. | Cliente criado ou localizado com os campos compartilhados. |

**CTA:** Ver exemplos de mensagens → #fale-do-seu-jeito

Guardrail: Uma foto ou um contato sozinho não autoriza pagamento, contratação ou envio a terceiros.

## CF02 — Entende o contexto

**Título do painel**

> Não precisa contar a mesma história de novo.

**Kicker:** O que já foi registrado continua valendo

**Descrição**

> A Taliya procura o cliente e o serviço a que você se refere. Assim, um recebimento, uma mudança de horário ou um documento continua no mesmo trabalho.

**Componente interno:** Reutilizar processo de 4 passos; trocar o texto, não simular agentes internos.



| Seleção / etapa | Exemplo ou fala | Resultado |
| --- | --- | --- |
| 1. Entende o pedido | “A Ana pagou mais R$100.” | Identifica que você está informando outro pagamento. |
| 2. Consulta o contexto | Limpeza da Ana: R$450 combinados e R$300 recebidos. | Localiza o serviço e o saldo registrado de R$150. |
| 3. Atualiza o registro | Você informou mais R$100. | Total recebido passa a R$400. |
| 4. Mostra o resultado | “Registrei mais R$100. Agora restam R$50.” | O saldo atualizado fica disponível para a próxima consulta. |

**CTA:** Ver um fluxo completo → #fluxos

Guardrail: O cenário tem uma única Ana e um serviço inequívoco. Havendo mais de um candidato, a conversa esclarece antes da alteração.

## CF03 — Pergunta só o necessário

**Título do painel**

> Só falta uma informação? Responda só ela.

**Kicker:** Começar não precisa virar um cadastro

**Descrição**

> Quando um dado realmente faz falta para a próxima ação, a Taliya pergunta sem pedir que você repita todo o pedido.

**Componente interno:** Dois exemplos selecionáveis reaproveitando tabs e chat; default Duração.



| Seleção / etapa | Exemplo ou fala | Resultado |
| --- | --- | --- |
| Falta a duração | Você: “Marca a limpeza da Luana amanhã às 16h.”<br>Taliya: “Quanto tempo dura essa limpeza?”<br>Você: “Duas horas.” | Taliya: “Marquei para 19/09, das 16h às 18h. O valor ficou sem definir.” |
| Existem duas Anas | Você: “A Ana pagou R$200.”<br>Taliya: “Ana Lima, telefone final 8421, ou Ana Souza, final 1190?”<br>Você: “A Lima.” | Taliya continua no único serviço em aberto da Ana Lima e registra os R$200. |

**CTA:** Conhecer o cadastro progressivo → #como-comecar

Guardrail: O preço pode continuar ausente no agendamento. Telefone e endereço não são exigidos sem necessidade. Perguntar cliente não dispensa resolver o serviço quando também houver ambiguidade.

## CF04 — Tudo fica conectado

**Título do painel**

> O combinado acompanha o serviço.

**Kicker:** Um trabalho, não várias anotações soltas

**Descrição**

> Orçamento, datas, pagamentos e arquivos ficam relacionados. Você pode voltar depois e encontrar a informação no contexto certo.

**Componente interno:** Reutilizar a comparação em três cards; não desqualificar planilha ou chat genericamente.



| Seleção / etapa | Exemplo ou fala | Resultado |
| --- | --- | --- |
| O que você combinou | Marina aprovou a instalação de R$900. | A aprovação identifica a versão do orçamento que vale. |
| O que você registrou | Marina pagou R$300 de entrada. | O pagamento fica ligado à instalação, não a um lançamento solto. |
| O que pode consultar | “Quanto falta receber da instalação?” | “Restam R$600 dos R$900 combinados.” |

**CTA:** Ver as sete frentes → #o-que-resolve

Guardrail: Os dados dependem do que foi informado ou obtido por integrações autorizadas. A Taliya não acompanha automaticamente conversas externas.

## CF05 — WhatsApp + app

**Título do painel**

> Sua rotina na conversa. A visão completa no app.

**Kicker:** Uma conta, os mesmos registros

**Descrição**

> Depois de criar a conta e vincular seu número, você pode registrar, consultar e ajustar a rotina pelo WhatsApp. Use o app quando preferir visualizar ou editar diretamente.

**Componente interno:** Split conversa/app com duas seleções; nunca duas bases independentes.



| Seleção / etapa | Exemplo ou fala | Resultado |
| --- | --- | --- |
| Pelo WhatsApp | “A Ana pagou R$300 pela limpeza.” | Conversa: R$300 recebidos e R$150 restantes. App: os mesmos valores no serviço da Ana. |
| Pelo app | Você corrige o pagamento de R$300 para R$350 na ficha do serviço. | Na consulta seguinte pelo WhatsApp, a Taliya informa R$100 restantes, mantendo o total de R$450. |

**CTA:** Entender os dois canais → faq-whatsapp

Guardrail: Conta, permissões, privacidade e assinatura podem exigir app ou página segura. Preferências simples podem ser alteradas por ordem clara; permissão do aparelho não nasce de uma mensagem.

## CF06 — Do seu jeito

**Título do painel**

> Um jeito de organizar. Vários jeitos de trabalhar.

**Kicker:** A contratação não precisa ditar sua agenda

**Descrição**

> Serviço avulso, pacote de sessões ou mensalidade. Uma data, várias visitas, alguns dias ou uma rotina recorrente. Comece por uma parte, sem adotar um processo obrigatório.

**Componente interno:** Dois grupos independentes: 3 tabs comerciais e 4 chips temporais. Não gerar combinações aleatórias; mostrar exemplos definidos abaixo.



| Seleção / etapa | Exemplo ou fala | Resultado |
| --- | --- | --- |
| Avulso | “Fechei a instalação do Carlos por R$750.” | Um serviço contratado, com datas e pagamentos quando forem informados. |
| Pacote | “João fechou oito aulas por R$600. Vou marcar depois.” | Oito aulas contratadas; nenhuma sessão marcada por obrigação. |
| Plano | “Jardinagem do Carlos: R$350 por mês a partir de 1º de outubro.” | Valor por ciclo mensal, sem multiplicar a cobrança pelo número de visitas. |



| Execução | Exemplo |
| --- | --- |
| Uma vez | Uma instalação em uma data combinada. |
| Várias datas | O mesmo serviço com duas visitas, nos dias 22 e 24/09. |
| Vários dias | Pintura de 21 a 23/09; período informativo se não houver horários. |
| Recorrente | Visitas às sextas, 8h–9h, com frequência e alcance confirmados. |

**CTA:** Ver situações completas → #fluxos

Guardrail: Sem tarefas, turmas, equipe ou controle de estoque. No pacote, agendar reserva; registrar realização consome.

# S06. Mural — Fale do seu jeito

**Título**

> Fale como você já fala no dia a dia.

**Subtítulo**

> Conte o que aconteceu ou o que precisa fazer. Quando uma informação importante estiver faltando, a Taliya pergunta só o necessário.

**Fechamento**

> Você fala. A Taliya organiza o contexto para continuar depois.

**Apoio ao app**

> Prefere usar o app? Você também pode registrar, consultar e corrigir diretamente por lá.

**CTA:** Veja tudo que você pode resolver → #o-que-resolve

Posição: após Como funciona e imediatamente antes das sete frentes. A biblioteca possui 84 mensagens; a seleção inicial possui 24, em três faixas de oito. No mobile, mostrar 12 e revelar outras 12 com “Ver mais mensagens”. O conjunto completo está no Anexo A e no JSON.

**Mensagem em destaque**

> A Marina aprovou o orçamento de R$900, pagou R$300 de entrada e quer fazer dia 24.

A data sem horário pode ficar informativa. Para agendar, a Taliya precisa do início e da duração.

**Interação:** Seleciona a frente/subtipo correspondente em S07 e rola até o painel. Não envia mensagem nem abre um chat real.

**Movimento:** Animação opcional; desligada por padrão. Com movimento, pausar em foco/hover, oferecer pausa explícita e respeitar preferência de movimento reduzido.



| Faixa | Mensagens iniciais |
| --- | --- |
| 1 | O que eu tenho hoje?<br>Marca a Júlia amanhã às 14h por uma hora.<br>Passa a Júlia de quinta para sexta às 10h.<br>Cancela só o atendimento da Ana de amanhã.<br>Fechei uma limpeza de sofá para a Luana por R$250.<br>Faz um orçamento de instalação de R$850 para a Marina.<br>A Marina aprovou a versão 2 do orçamento.<br>A Marina pagou R$300 e ainda faltam R$150. |
| 2 | Quem ainda tem valor em aberto?<br>Me lembra segunda às 9h de cobrar os R$150 da Ana.<br>João fechou oito aulas por R$600.<br>Cadê a versão aprovada da Empresa Norte?<br>Corrige aquele pagamento: foram R$350, não R$300.<br>Guarda esse PDF no serviço da Marina.<br>Quais horários já tenho ocupados na sexta?<br>Essa pintura vai de segunda a quarta. |
| 3 | Quando foi o último serviço concluído da Júlia?<br>Toda segunda às 9h me lembra de revisar as propostas.<br>Recebi R$200 de sinal da instalação do Carlos.<br>Esse PDF é uma nova versão da proposta.<br>Carlos entrou no plano mensal de R$350 a partir de outubro.<br>Aquela instalação é da Camila, não da Carla.<br>Terminei o serviço inteiro da Marina.<br>Me mostra os documentos dessa instalação. |

# S07. Sete frentes — contrato do componente

**Título**

> O que você pode resolver com a Taliya

**Subtítulo**

> Não precisa usar tudo. Comece pela parte que já toma tempo ou fica na sua cabeça.



| ID | Frente | Subtipos |
| --- | --- | --- |
| CL | Clientes | Criar ou identificar; Consultar; Atualizar; Histórico; Corrigir relação |
| SV | Serviços | Pedido novo; Fechou direto; Pacote; Plano; Vários dias; Concluir ou cancelar |
| AG | Agenda | Agendar; Consultar; Disponibilidade; Remarcar; Cancelar horário; Recorrência |
| OR | Orçamentos | Criar; Itens; Revisar; Aprovação; Encontrar |
| RC | Recebimentos | Recebeu tudo; Parcial; Sinal; Saldo; Corrigir; Ciclos |
| LE | Lembretes | Cobrar; Cliente; Serviço; Documento e rotina; Antes do atendimento; Se ainda estiver aberto |
| AR | Arquivos e documentos | Guardar; Encontrar; Versões; Orçamento, contrato ou recibo; Corrigir relação |

**initial:** Agenda / Agendar é a abertura editorial; hash de campanha pode escolher outro par válido.

**changeCategory:** Trocar apenas a frente ativa. Selecionar seu primeiro subtipo; não deixar o subtipo da frente anterior ativo.

**changeSubtype:** Atualizar caso, mensagem, resposta, card de resultado e próximo passo juntos. Nenhuma mudança de dado real.

**reset:** Cada subtipo tem seu próprio cenário fictício. Trocar de exemplo reinicia a demonstração, sem carregar saldo de outro cenário.

**depth:** No máximo dois níveis: frente e subtipo. Não adicionar menus aninhados de terceiro nível.

**deepLink:** #o-que-resolve?frente=AG&caso=AG04; validar IDs localmente. Fragmento é tratado no cliente e não autoriza consulta de dados.

**mobile:** Mostrar a lista horizontal de frentes e as subtabs em região rolável própria, sem overflow da página. Conteúdo visível fica abaixo; resultado não se esconde atrás de “ver detalhes”.

**accessibility:** Tabs com nome, foco visível, estado selecionado e painel associado. Foco não salta para o topo quando muda o caso; navegação por teclado alcança todas as opções.

**Não criar uma arquitetura paralela**

> Clientes, Serviços, Agenda, Orçamentos, Recebimentos, Lembretes e Arquivos e documentos são rótulos comerciais. Orçamento continua dentro do Serviço. Histórico e contexto aparecem em todas as frentes.

Os próximos painéis têm a copy completa de todos os subtipos. Exibir os seis campos publicáveis com o resultado já visível, sem “ver detalhes” obrigatório. Contexto/guardrail são apenas instruções para quem implementa.

# S07.CL — Clientes

**Título da frente**

> Lembre do cliente e do que já combinou.

**Descrição**

> Os dados e os trabalhos ficam relacionados, sem exigir uma ficha completa para começar.

Fontes de escopo: S2 §§3–4; S3 OP-CL-01. Asset lógico: VIS-FR-CL.

## CL01 · Criar ou identificar

**Quando você usa:** Chegou um cliente novo ou você compartilhou um contato.

**Você:** Cadastra a Marina com esse contato.

**Taliya:** Marina cadastrada com o nome e o telefone do contato.

**O que a Taliya organiza:** Localiza um cadastro compatível ou cria o cliente com os dados compartilhados.

**O que fica registrado:** Cliente: Marina · Nome e telefone informados.

**O que você pode fazer depois:** Registrar um serviço ou complementar um dado quando precisar.

Contexto da encenação: Cartão de contato fictício de Marina; nenhum homônimo. | Não publicar: Contato não cria contratação, agenda ou recebimento sozinho.

## CL02 · Consultar

**Quando você usa:** Você quer recuperar rapidamente os trabalhos de uma pessoa ou empresa.

**Você:** Me mostra os serviços ativos da Marina.

**Taliya:** Marina tem uma instalação confirmada de R$900, com R$600 restantes.

**O que a Taliya organiza:** Reúne os serviços registrados para aquele cliente, sem misturar outros nomes.

**O que fica registrado:** Cliente e serviço consultados. Nenhum dado alterado.

**O que você pode fazer depois:** Abrir o serviço, consultar uma data ou conferir um documento.

Contexto da encenação: Instalação MAR-S01 confirmada, entrada de R$300. | Não publicar: Consulta não grava nova operação; resumir com base na mesma projeção do app.

## CL03 · Atualizar

**Quando você usa:** O cliente informou um dado novo.

**Você:** O endereço da Marina para essa instalação é Rua das Flores, 120.

**Taliya:** Registrei Rua das Flores, 120, para a instalação da Marina.

**O que a Taliya organiza:** Associa o endereço informado ao trabalho certo.

**O que fica registrado:** Endereço de atendimento registrado na instalação da Marina.

**O que você pode fazer depois:** Consultar o local antes de sair ou corrigir o número depois.

Contexto da encenação: Rua fictícia; instalação selecionada. | Não publicar: Não sobrescrever todos os endereços da cliente por um endereço de serviço.

## CL04 · Histórico

**Quando você usa:** Um cliente voltou e você quer lembrar do último trabalho.

**Você:** Qual foi o último serviço que fiz para a Ana?

**Taliya:** O último serviço registrado como concluído foi a limpeza de sofá de 10/09, por R$450.

**O que a Taliya organiza:** Busca o histórico disponível e distingue serviço concluído de apenas agendado.

**O que fica registrado:** Histórico consultado. Registro original preservado.

**O que você pode fazer depois:** Abrir o registro e consultar o que foi combinado.

Contexto da encenação: Fixture Ana inclui serviço concluído em 10/09. | Não publicar: Não chamar horário passado de realizado sem registro explícito.

## CL05 · Corrigir relação

**Quando você usa:** Você associou um trabalho à pessoa errada.

**Você:** A instalação de sexta é da Camila, não da Carla.

**Taliya:** Encontrei a instalação de sexta ligada à Carla. Quer trocar para Camila Souza, final 2255?

**O que a Taliya organiza:** Localiza o serviço e apresenta o cliente correto antes de corrigir um vínculo sensível.

**O que fica registrado:** Após confirmação: mesmo serviço, cliente corrigido e histórico preservado.

**O que você pode fazer depois:** Confirmar o vínculo e continuar no mesmo serviço.

Contexto da encenação: Uma instalação na sexta; Camila existente; confirmação prevista. | Não publicar: Não mesclar clientes nem mover outros serviços por semelhança de nome.

# S07.SV — Serviços

**Título da frente**

> Mantenha o combinado junto do trabalho.

**Descrição**

> Do pedido inicial à contratação direta, cada serviço conserva seu contexto.

Fontes de escopo: S2 §§4–5 e7. Asset lógico: VIS-FR-SV.

## SV01 · Pedido novo

**Quando você usa:** Um cliente pediu informações e ainda não fechou.

**Você:** Ana pediu um orçamento para limpar o sofá.

**Taliya:** Registrei o pedido de orçamento da Ana para limpeza de sofá.

**O que a Taliya organiza:** Registra a demanda sem fingir que já houve contratação.

**O que fica registrado:** Cliente: Ana · Serviço: pedido de limpeza · Situação: Novo · Sem cobrança.

**O que você pode fazer depois:** Preparar a proposta, informar o valor ou encerrar a negociação.

Contexto da encenação: Pedido explícito; nenhum orçamento gerado ainda. | Não publicar: Sem lead separado, cobrança ou agenda automática.

## SV02 · Fechou direto

**Quando você usa:** O cliente já aceitou e você só quer registrar o combinado.

**Você:** Fechei a instalação do Carlos por R$750.

**Taliya:** Instalação do Carlos registrada por R$750, como confirmada.

**O que a Taliya organiza:** Registra a contratação sem exigir orçamento ou etapas que não aconteceram.

**O que fica registrado:** Instalação do Carlos · Situação: Confirmado · Combinado: R$750.

**O que você pode fazer depois:** Marcar o horário ou informar uma entrada.

Contexto da encenação: Contratação direta inequívoca; pagamento não informado. | Não publicar: Não fabricar proposta aprovada ou marcar recebido.

## SV03 · Pacote

**Quando você usa:** Você vendeu uma quantidade fechada de aulas ou sessões.

**Você:** João fechou oito aulas por R$600. Vou marcar os horários depois.

**Taliya:** Pacote do João registrado: oito aulas por R$600, ainda sem horários marcados.

**O que a Taliya organiza:** Guarda a quantidade e o valor contratado sem obrigar a preencher a agenda.

**O que fica registrado:** Pacote: 8 aulas · Valor: R$600 · Realizadas: 0 · Agendadas: 0 · Disponíveis: 8.

**O que você pode fazer depois:** Agendar aos poucos e consultar realizadas, reservadas e disponíveis.

Contexto da encenação: Nenhuma sessão anterior no pacote. | Não publicar: Aula agendada reserva; não consome até confirmar realização.

## SV04 · Plano

**Quando você usa:** O serviço é contratado por um valor a cada período.

**Você:** Jardinagem do Carlos por R$350 ao mês, a partir de 1º de outubro.

**Taliya:** Plano mensal do Carlos registrado por R$350, com início em 01/10.

**O que a Taliya organiza:** Registra o valor por ciclo e o início da contratação.

**O que fica registrado:** Jardinagem do Carlos · Plano mensal: R$350 por ciclo · Início: 01/10.

**O que você pode fazer depois:** Informar quando as visitas acontecem ou consultar o ciclo correspondente.

Contexto da encenação: Não há limite de visitas informado; quantidade fica desconhecida, não ilimitada. | Não publicar: Cinco visitas não geram cinco mensalidades. Não materializar dezenas de cobranças.

## SV05 · Vários dias

**Quando você usa:** Um trabalho continua por mais de um dia.

**Você:** A pintura da Carla ficou R$2.400 e vai de segunda a quarta.

**Taliya:** Pintura da Carla registrada de 21 a 23/09, por R$2.400. O período está sem horários definidos.

**O que a Taliya organiza:** Registra o período de execução no mesmo serviço.

**O que fica registrado:** Pintura da Carla · Serviço avulso · Período: 21 a 23/09 · Valor: R$2.400.

**O que você pode fazer depois:** Adicionar intervalos de trabalho ou ajustar a data de término.

Contexto da encenação: Relógio do exemplo 18/09/2026; sem horas. | Não publicar: Período sem hora é informativo; não bloquear três dias inteiros nem criar tarefas.

## SV06 · Concluir ou cancelar

**Quando você usa:** Você decide registrar que o trabalho terminou ou não seguirá.

**Você:** Terminei a instalação do Carlos.

**Taliya:** Instalação marcada como concluída. O saldo registrado continua em R$250.

**O que a Taliya organiza:** Atualiza o serviço, sem alterar o que foi pago ou o saldo.

**O que fica registrado:** Instalação concluída · Saldo: R$250 · Pagamentos e histórico preservados.

**O que você pode fazer depois:** Consultar o saldo; para cancelamento, pedir explicitamente “Cancela esse serviço”.

Contexto da encenação: Contrato de R$750; recebido de R$500; saldo de R$250. | Não publicar: Cancelar serviço não é cancelar só horário. Entrada não some e estorno nunca é automático.

# S07.AG — Agenda

**Título da frente**

> Marque, remarque e consulte sem perder o contexto.

**Descrição**

> Horários ficam ligados ao serviço. Mudanças não precisam virar outro cadastro.

Fontes de escopo: S2 §9; S3 OP-AGENDA-01/03/05/06. Asset lógico: VIS-FR-AG.

## AG01 · Agendar

**Quando você usa:** Você combinou um atendimento com data e duração.

**Você:** Marca a avaliação da Júlia amanhã às 14h por uma hora.

**Taliya:** Avaliação da Júlia marcada para 19/09, das 14h às 15h.

**O que a Taliya organiza:** Registra cliente, serviço e ocorrência com intervalo conhecido.

**O que fica registrado:** Avaliação da Júlia · 19/09, 14h–15h · Valor não definido.

**O que você pode fazer depois:** Consultar a agenda ou informar o valor mais tarde.

Contexto da encenação: Sem conflito; hoje 18/09; Julia inequívoca. | Não publicar: Não pedir preço para agendar nem afirmar confirmação enviada à cliente.

## AG02 · Consultar

**Quando você usa:** Você quer saber os compromissos registrados.

**Você:** Como está minha agenda amanhã?

**Taliya:** Amanhã: avaliação da Júlia, 14h–15h; limpeza da Luana, 16h–18h.

**O que a Taliya organiza:** Organiza os atendimentos do período com cliente e serviço.

**O que fica registrado:** Agenda de 19/09 consultada. Nenhum compromisso alterado.

**O que você pode fazer depois:** Pedir detalhes de um atendimento ou consultar outro dia.

Contexto da encenação: Dois agendamentos fictícios na base. | Não publicar: Não tratar ausência de registros como disponibilidade universal.

## AG03 · Disponibilidade

**Quando você usa:** Você precisa encontrar um intervalo conhecido como livre.

**Você:** Tenho um horário livre de uma hora na sexta?

**Taliya:** Na sexta, 25/09, há uma janela de 9h às 10h, considerando seu horário de atendimento e os compromissos registrados.

**O que a Taliya organiza:** Cruza horário de atendimento e ocupações conhecidas; informa os limites da consulta.

**O que fica registrado:** Disponibilidade consultada para 25/09. Nada agendado.

**O que você pode fazer depois:** Pedir para agendar nesse intervalo; a disponibilidade será conferida de novo.

Contexto da encenação: Expediente das 8h às 18h configurado; ocupações conhecidas das 8h às 9h e das 10h às 18h. | Não publicar: Sem expediente, mostrar ocupações e pedir período. Consulta não autoriza agendar.

## AG04 · Remarcar

**Quando você usa:** O horário mudou, mas o trabalho é o mesmo.

**Você:** Passa a visita do Carlos de quinta para sexta às 10h.

**Taliya:** Visita remarcada para 25/09, das 10h às 11h.

**O que a Taliya organiza:** Move a mesma ocorrência e conserva a duração conhecida.

**O que fica registrado:** Mesma visita · Antes: 24/09, 14h–15h · Agora: 25/09, 10h–11h.

**O que você pode fazer depois:** Consultar a nova agenda; lembrete relativo acompanha quando existir.

Contexto da encenação: Duração de 1h conhecida, destino livre. | Não publicar: Não duplicar serviço, pagamento ou sessão.

## AG05 · Cancelar horário

**Quando você usa:** O atendimento não vai acontecer naquela data.

**Você:** Cancela só o atendimento da Ana de amanhã.

**Taliya:** Cancelei o atendimento de 19/09. O serviço e os pagamentos registrados foram mantidos.

**O que a Taliya organiza:** Cancela a ocorrência indicada e preserva o restante do serviço.

**O que fica registrado:** Atendimento de 19/09 cancelado · Serviço e pagamentos preservados.

**O que você pode fazer depois:** Combinar outra data depois, sem perder o histórico.

Contexto da encenação: Uma ocorrência inequívoca em19/09. | Não publicar: Não cancelar plano/pacote, perdoar saldo ou devolver entrada por inferência.

## AG06 · Recorrência

**Quando você usa:** Você combinou datas que se repetem por um período.

**Você:** Marca a manutenção do Carlos nas próximas quatro sextas, das 8h às 9h, começando em 25 de setembro.

**Taliya:** Marquei 25/09, 02/10, 09/10 e 16/10, das 8h às 9h.

**O que a Taliya organiza:** Registra as ocorrências no serviço existente, com alcance finito.

**O que fica registrado:** Quatro visitas de 1h · Mesmo serviço · Datas: 25/09, 02/10, 09/10 e 16/10.

**O que você pode fazer depois:** Pedir mudança só de uma data ou das próximas, esclarecendo o alcance.

Contexto da encenação: Manutenção ativa, sem conflitos, capacidade única. | Não publicar: Recorrência de agenda não cria plano comercial nem cobrança por visita.

# S07.OR — Orçamentos

**Título da frente**

> Prepare a proposta sem perder o combinado.

**Descrição**

> Crie, ajuste e encontre versões no contexto do serviço. A aprovação precisa ser informada.

Fontes de escopo: S2 §§5–6; S3 contratos documentais. Asset lógico: VIS-FR-OR.

## OR01 · Criar

**Quando você usa:** Você precisa apresentar escopo e preço ao cliente.

**Você:** Faz um orçamento para a Marina: R$650 de instalação e R$200 de material.

**Taliya:** Preparei o orçamento de R$850 da Marina para você revisar.

**O que a Taliya organiza:** Organiza os itens cobrados e prepara uma proposta para revisão.

**O que fica registrado:** Orçamento v1: R$850 · Serviço em negociação · Documento para revisão.

**O que você pode fazer depois:** Revisar, gerar o PDF e compartilhar pelo canal que escolher.

Contexto da encenação: Itens e valores completos informados. | Não publicar: Não inventar preço de material; não emitir nota fiscal; preparar não significa enviar.

## OR02 · Itens

**Quando você usa:** O escopo da proposta mudou antes da aprovação.

**Você:** Adiciona R$200 de material ao orçamento da instalação de R$650.

**Taliya:** Incluí R$200 de material. O orçamento agora soma R$850.

**O que a Taliya organiza:** Inclui o item na proposta e atualiza o total apresentado.

**O que fica registrado:** Instalação: R$650 · Material cobrado: R$200 · Total proposto: R$850.

**O que você pode fazer depois:** Revisar o escopo e confirmar qual versão compartilhar.

Contexto da encenação: Proposta em revisão, não aprovada; alteração versionada. | Não publicar: Trata material como item comercial, não controle de custo, estoque ou compra.

## OR03 · Revisar

**Quando você usa:** Você precisa enviar uma alternativa ao que já foi combinado.

**Você:** Faz uma nova versão do orçamento da Marina com R$100 de desconto.

**Taliya:** Preparei a versão 2 por R$800. O combinado aprovado de R$900 continua valendo até você registrar a nova aprovação.

**O que a Taliya organiza:** Cria uma revisão sem substituir um combinado já aprovado por conta própria.

**O que fica registrado:** Versão 1 aprovada: R$900 · Versão 2 em proposta: R$800.

**O que você pode fazer depois:** Revisar a versão e informar se o cliente aceitou.

Contexto da encenação: Cenário de revisão após aprovação; não houve novo aceite. | Não publicar: Não recalcular recebíveis com proposta ainda não aprovada.

## OR04 · Aprovação

**Quando você usa:** O cliente aceitou uma proposta e você quer registrar esse fato.

**Você:** A Marina aprovou a versão 2 do orçamento, de R$800.

**Taliya:** Aprovação registrada. A versão 2 de R$800 é o combinado vigente da instalação.

**O que a Taliya organiza:** Atualiza o combinado do mesmo serviço para a versão explicitamente aprovada.

**O que fica registrado:** Mesmo serviço confirmado · Combinado vigente: R$800 · Versão 1 no histórico.

**O que você pode fazer depois:** Agendar o trabalho ou registrar uma entrada.

Contexto da encenação: Sem pagamentos anteriores neste cenário; versão 2 identificada. | Não publicar: Não criar outro serviço por “conversão” de orçamento. Com pagamentos anteriores, revisar os efeitos antes.

## OR05 · Encontrar

**Quando você usa:** Você precisa recuperar a proposta certa.

**Você:** Cadê a versão aprovada do orçamento da Marina?

**Taliya:** Aqui está a versão aprovada: orçamento da instalação, R$900.

**O que a Taliya organiza:** Busca a versão marcada como aprovada para aquele trabalho.

**O que fica registrado:** Versão aprovada localizada. Nenhuma alteração no combinado.

**O que você pode fazer depois:** Consultar os itens ou pedir outra versão quando necessário.

Contexto da encenação: Cenário alternativo: versão 1 aprovada por R$900; versão 2 rascunho. | Não publicar: Não devolver a mais nova como aprovada sem conferir seu estado.

# S07.RC — Recebimentos

**Título da frente**

> Saiba quanto entrou e quanto ainda falta.

**Descrição**

> Você informa os pagamentos. A Taliya organiza os valores no serviço certo.

Fontes de escopo: S2 §7; S3 OP-FIN-01/02/03. Asset lógico: VIS-FR-RC.

## RC01 · Recebeu tudo

**Quando você usa:** O cliente quitou o valor conhecido de um serviço.

**Você:** A Luana pagou os R$250 da limpeza.

**Taliya:** Registrei R$250 recebidos da Luana. Não ficou saldo dessa limpeza.

**O que a Taliya organiza:** Registra o pagamento no serviço e atualiza o restante.

**O que fica registrado:** Combinado: R$250 · Recebido: R$250 · Restante: R$0.

**O que você pode fazer depois:** Consultar o histórico ou revisar a informação no app.

Contexto da encenação: Sem pagamentos prévios; total conhecido. | Não publicar: Sem total conhecido, não afirmar quitação. Não confirmar banco/Pix.

## RC02 · Parcial

**Quando você usa:** O pagamento foi menor que o total combinado.

**Você:** A Ana pagou R$300 pela limpeza. Ficaram faltando R$150.

**Taliya:** Registrei R$300 recebidos. Restam R$150 da limpeza da Ana.

**O que a Taliya organiza:** Mantém pagamento e saldo associados à contratação.

**O que fica registrado:** Combinado: R$450 · Recebido: R$300 · Restante: R$150 · Parcial.

**O que você pode fazer depois:** Consultar o saldo ou criar um lembrete de cobrança.

Contexto da encenação: Uma limpeza da Ana; nenhum pagamento anterior. | Não publicar: Somente registrar o fato informado, sem enviar mensagem à cliente.

## RC03 · Sinal

**Quando você usa:** Você recebeu uma entrada antes de executar o serviço.

**Você:** A Marina pagou R$300 de sinal da instalação de R$900.

**Taliya:** Entrada de R$300 registrada. Ficam R$600 para receber da instalação.

**O que a Taliya organiza:** Registra a entrada sem tratar o trabalho como concluído.

**O que fica registrado:** Combinado: R$900 · Recebido: R$300 · Restante: R$600.

**O que você pode fazer depois:** Combinar a agenda e consultar o restante depois.

Contexto da encenação: Contrato confirmado; sem pagamento prévio. | Não publicar: Entrada não prova execução e não altera automaticamente o estado do serviço.

## RC04 · Saldo

**Quando você usa:** Você precisa saber o que está em aberto.

**Você:** Quanto falta receber da instalação da Marina?

**Taliya:** Restam R$600 dos R$900 combinados. Há R$300 registrados como recebidos.

**O que a Taliya organiza:** Consulta o combinado e os pagamentos registrados.

**O que fica registrado:** Combinado: R$900 · Recebido: R$300 · Restante: R$600 · Consulta sem alteração.

**O que você pode fazer depois:** Consultar outros serviços ou preparar o próximo contato.

Contexto da encenação: Contrato de R$900; recebido de R$300; fonte explícita. | Não publicar: Resumos gerais dizem “valores registrados”, não receita total ou lucro.

## RC05 · Corrigir

**Quando você usa:** Você informou um valor errado.

**Você:** Corrige o pagamento da limpeza da Ana: foram R$350, não R$300.

**Taliya:** Corrigi para R$350 recebidos. Restam R$100 dos R$450 combinados.

**O que a Taliya organiza:** Corrige o registro identificado, preservando a trilha da alteração.

**O que fica registrado:** Recebido corrigido: R$350 · Restante: R$100 · Correção no histórico.

**O que você pode fazer depois:** Consultar o resultado no app ou continuar pela conversa.

Contexto da encenação: Um pagamento original de R$300 identificado. | Não publicar: Correção não é novo pagamento nem estorno bancário. Não apagar o histórico.

## RC06 · Ciclos

**Quando você usa:** Você acompanha uma mensalidade ou outro período de um plano.

**Você:** O Carlos pagou os R$350 da jardinagem de outubro.

**Taliya:** Registrei R$350 recebidos no ciclo de outubro da jardinagem do Carlos.

**O que a Taliya organiza:** Registra o pagamento no ciclo indicado do plano.

**O que fica registrado:** Plano de jardinagem · Ciclo de outubro · Recebido: R$350.

**O que você pode fazer depois:** Consultar o próximo ciclo quando existir ou revisar o histórico.

Contexto da encenação: Plano com início em 01/10; obrigação do ciclo já materializada. | Não publicar: Não criar várias cobranças por visita nem dizer que um mês futuro foi pago sem informação.

# S07.LE — Lembretes

**Título da frente**

> Guarde a próxima ação com o contexto certo.

**Descrição**

> Peça um aviso sobre cliente, serviço ou documento, sem depender só da memória.

Fontes de escopo: S2 §8; S3 regras de canal. Asset lógico: VIS-FR-LE.

## LE01 · Cobrar

**Quando você usa:** Ficou um valor para receber e você quer retomar depois.

**Você:** Me lembra segunda às 9h de cobrar os R$150 da Ana.

**Taliya:** Lembrete criado para 21/09, às 9h: cobrar R$150 da Ana pela limpeza.

**O que a Taliya organiza:** Cria um lembrete para você sobre o saldo daquele serviço.

**O que fica registrado:** Lembrete: cobrar R$150 da Ana · 21/09, 9h · Vinculado à limpeza.

**O que você pode fazer depois:** Consultar, remarcar ou cancelar o lembrete.

Contexto da encenação: Hoje18/09; saldo de R$150 conhecido. | Não publicar: Aviso ao dono, não mensagem automática à cliente; entrega depende do canal habilitado.

## LE02 · Cliente

**Quando você usa:** Você quer lembrar de entrar em contato com alguém.

**Você:** Me lembra terça às 10h de falar com a Júlia.

**Taliya:** Lembrete criado para 22/09, às 10h: falar com a Júlia.

**O que a Taliya organiza:** Guarda o assunto e o momento informado.

**O que fica registrado:** Lembrete: falar com a Júlia · 22/09, 10h · Sem serviço obrigatório.

**O que você pode fazer depois:** Complementar o assunto ou alterar o horário.

Contexto da encenação: Júlia inequívoca; momento explícito. | Não publicar: Não iniciar conversa externa nem criar follow-up como módulo.

## LE03 · Serviço

**Quando você usa:** Há algo para preparar antes de um trabalho.

**Você:** Me lembra amanhã às 8h de levar o equipamento para a limpeza da Luana.

**Taliya:** Lembrete criado para 19/09, às 8h: levar o equipamento para a limpeza da Luana.

**O que a Taliya organiza:** Mantém o aviso ligado ao serviço para recuperar o contexto.

**O que fica registrado:** Lembrete: levar o equipamento · 19/09, 8h · Limpeza da Luana.

**O que você pode fazer depois:** Consultar o serviço e o lembrete juntos.

Contexto da encenação: Limpeza da Luana existente. | Não publicar: Lembrete não é compromisso que ocupa a agenda nem controle de estoque.

## LE04 · Documento e rotina

**Quando você usa:** Você revisa propostas com uma frequência definida.

**Você:** Toda segunda às 9h, me lembra de revisar os orçamentos em aberto.

**Taliya:** Lembrete recorrente criado para segundas às 9h: revisar os orçamentos em aberto.

**O que a Taliya organiza:** Cria a rotina de lembrete sem alterar documentos ou aprovações.

**O que fica registrado:** Lembrete recorrente · Segundas, 9h · Próximo aviso: 21/09.

**O que você pode fazer depois:** Pausar a rotina ou mudar a frequência quando precisar.

Contexto da encenação: Não depende de um cliente específico. | Não publicar: Recorrência do lembrete não cria tarefa, cobrança ou envio de proposta.

## LE05 · Antes do atendimento

**Quando você usa:** Você quer um aviso que acompanhe a data do serviço.

**Você:** Me lembra uma hora antes da visita do Carlos.

**Taliya:** Lembrete definido para uma hora antes da visita: 24/09, às 13h.

**O que a Taliya organiza:** Relaciona o aviso ao horário da ocorrência.

**O que fica registrado:** Visita: 24/09, 14h · Lembrete relativo: 24/09, 13h.

**O que você pode fazer depois:** Se a visita for remarcada, o horário relativo acompanha.

Contexto da encenação: Uma visita identificada; início às 14h. | Não publicar: Com cancelamento, não manter alerta relativo de comparecimento sem sentido. Não prometer entrega sem canal elegível.

## LE06 · Se ainda estiver aberto

**Quando você usa:** Você só quer ser avisado se o saldo continuar pendente.

**Você:** Na segunda às 9h, me avisa se os R$150 da Ana ainda estiverem em aberto.

**Taliya:** Registrei o aviso para 21/09, às 9h. Ele depende de o saldo continuar em aberto na Taliya.

**O que a Taliya organiza:** Verifica o estado registrado no momento do lembrete.

**O que fica registrado:** Aviso condicional · 21/09, 9h · Verificar se R$150 continuam em aberto.

**O que você pode fazer depois:** Informar o pagamento quando acontecer para manter a condição correta.

Contexto da encenação: Um recebível identificado; condição observável na base. | Não publicar: Não afirmar que sabe se houve Pix fora do sistema. Se pago e informado, evitar alerta desnecessário.

# S07.AR — Arquivos e documentos

**Título da frente**

> Encontre o material pelo trabalho a que ele pertence.

**Descrição**

> Fotos, PDFs e versões ficam no contexto do serviço, para consultar depois.

Fontes de escopo: S2 §§5–6; S3 contratos documentais. Asset lógico: VIS-FR-AR.

## AR01 · Guardar

**Quando você usa:** Você recebeu um material e quer manter o vínculo com o trabalho.

**Você:** Guarda esse PDF na instalação da Marina.

**Taliya:** PDF anexado à instalação da Marina.

**O que a Taliya organiza:** Associa o arquivo enviado ao serviço indicado.

**O que fica registrado:** Arquivo anexado à instalação da Marina · contrato-marina.pdf.

**O que você pode fazer depois:** Pedir o arquivo novamente ou consultar os demais materiais do serviço.

Contexto da encenação: Upload concluído antes de confirmar; serviço inequívoco. | Não publicar: Não afirmar que anexou se upload falhou; não ler todas as pastas do celular.

## AR02 · Encontrar

**Quando você usa:** Você não lembra o nome exato de um arquivo.

**Você:** Me mostra o contrato da instalação da Empresa Norte.

**Taliya:** Encontrei o contrato da instalação da Empresa Norte.

**O que a Taliya organiza:** Busca o documento dentro do contexto informado.

**O que fica registrado:** Contrato localizado no serviço. Nenhuma modificação.

**O que você pode fazer depois:** Abrir ou compartilhar o arquivo pelo canal que escolher.

Contexto da encenação: Um contrato disponível no serviço. | Não publicar: Se houver várias versões, identificar a vigente; sem resultados é diferente de erro de consulta.

## AR03 · Versões

**Quando você usa:** Chegou uma revisão de um documento.

**Você:** Esse PDF é a versão nova do orçamento da Marina.

**Taliya:** Nova versão anexada ao serviço da Marina. A aprovação anterior não foi alterada.

**O que a Taliya organiza:** Guarda a revisão e preserva as versões anteriores.

**O que fica registrado:** Nova versão vinculada · Versão anterior e aprovação preservadas.

**O que você pode fazer depois:** Revisar e informar qual versão foi aprovada.

Contexto da encenação: PDF enviado; orçamento existente. | Não publicar: Upload não equivale a aprovação. Não substituir combinado financeiro silenciosamente.

## AR04 · Orçamento, contrato ou recibo

**Quando você usa:** Você quer preparar um documento com os dados já conhecidos.

**Você:** Prepara um recibo dos R$300 que registrei da instalação da Marina.

**Taliya:** Preparei o recibo de R$300 para você revisar.

**O que a Taliya organiza:** Monta o documento com base no pagamento informado e no modelo disponível.

**O que fica registrado:** Recibo de R$300 para revisão · Pagamento original mantido.

**O que você pode fazer depois:** Conferir os dados e compartilhar a versão final.

Contexto da encenação: Pagamento de R$300 existente; modelo de recibo habilitado. | Não publicar: Documento não é nota fiscal, comprovante bancário nem garantia de validade jurídica. Dados indispensáveis podem ser pedidos.

## AR05 · Corrigir relação

**Quando você usa:** Um arquivo ficou associado ao trabalho errado.

**Você:** Esse arquivo é da instalação da Marina, não da limpeza da Ana.

**Taliya:** Corrigi o vínculo do arquivo para a instalação da Marina.

**O que a Taliya organiza:** Confirma o alvo correto e ajusta o vínculo do arquivo identificado.

**O que fica registrado:** Arquivo vinculado à instalação da Marina · Histórico preservado.

**O que você pode fazer depois:** Encontrá-lo depois no serviço certo.

Contexto da encenação: Arquivo único selecionado e destino identificado. | Não publicar: Não transferir automaticamente pagamentos ou demais documentos; preservar regras de acesso.

# S08. Fluxos reais — substitui a calculadora

**Título**

> Um serviço muda. A Taliya mantém o fio.

**Subtítulo**

> Veja como a conversa continua entre orçamento, agenda, recebimento, lembrete e arquivo. Não é um caminho obrigatório: você pode usar só uma parte.

**reuse:** Usar container, card de contexto e cards de resultado da área de ROI; trocar sliders por seletor de cinco cenários e seletor de passos.

**initial:** FL01, passo1; primeira mensagem e resultado visíveis sem interação.

**stepRule:** Clicar num passo carrega o estado acumulado desse passo, sem exigir que o visitante clique nos anteriores. Não misturar snapshots entre cenários.

**motion:** Sem autoplay de conversa; botão Próximo passo ou seleção explícita.

**summaryCard:** Cliente, serviço, combinado, agenda e documentos continuam no mesmo contexto.

**zeroROI:** Não manter fórmula, moeda recuperada, tempo economizado ou campos antigos de alunos/mensalidade.



| Cenário | Função na venda |
| --- | --- |
| Orçamento e agenda | O serviço mantém cliente, proposta, horário e saldo no mesmo contexto. |
| Marcou, mudou, cancelou | Remarcar não duplica. Cancelar horário não apaga o serviço nem um pagamento. |
| Recebeu, consultou, lembrou | A Taliya organiza o saldo, lembra você e pode ajudar a preparar o texto. O envio à cliente é seu. |
| Pacote e sessões | Agendada não é realizada. O saldo distingue o que aconteceu e o que já está reservado. |
| Arquivo e contexto | O material fica ligado ao trabalho e pode ser recuperado pela conversa ou pelo app. |

## FL01 — Orçamento e agenda

**Título do cenário**

> Da proposta ao horário, sem refazer o cadastro.

Contexto fictício: Uma instalação para Marina; cenário independente, sem pagamento inicial.

### 1. Preparou

**Você:** Faz um orçamento de instalação para a Marina: R$650 de mão de obra e R$250 de material.

**Taliya:** Preparei o orçamento de R$900 para revisão.

**Resultado:** Marina · Instalação · Orçamento v1 · R$900 · Em negociação.

Material é cobrança, não gasto. Nenhum recebimento por emissão.

### 2. Aprovou

**Você:** A Marina aprovou esse orçamento.

**Taliya:** Aprovação registrada. A instalação está confirmada por R$900.

**Resultado:** Mesmo serviço · v1 aprovada · Combinado R$900.

### 3. Agendou

**Você:** Marca para 24 de setembro às 9h, por três horas.

**Taliya:** Marquei a instalação para 24/09, das 9h às 12h.

**Resultado:** Mesmo serviço · 24/09 9h–12h · Agenda livre no exemplo.

### 4. Entrou o sinal

**Você:** Ela pagou R$300 de entrada.

**Taliya:** Entrada registrada. Restam R$600 da instalação.

**Resultado:** Combinado R$900 · Recebido R$300 · Restante R$600.

**Fechamento do cenário**

> O serviço mantém cliente, proposta, horário e saldo no mesmo contexto.

Não publicar: Gerar orçamento não cria novo serviço no aceite; pagamento só existe após informação do dono.

**Controles:** Passo anterior · Próximo passo · Recomeçar exemplo. Nenhuma ação é executada no produto.

## FL02 — Marcou, mudou, cancelou

**Título do cenário**

> O horário muda. O histórico não se perde.

Contexto fictício: Visita de manutenção do Carlos; uma hora de duração; sem outras ocorrências nesta série.

### 1. Marcou

**Você:** Marca a visita do Carlos para 24 de setembro, das 14h às 15h.

**Taliya:** Visita marcada para 24/09, das 14h às 15h.

**Resultado:** Visita do Carlos · 24/09 14h–15h.

### 2. Remarcou

**Você:** Passa essa visita para sexta às 10h.

**Taliya:** Remarquei para 25/09, das 10h às 11h.

**Resultado:** Mesma ocorrência · 25/09 10h–11h.

### 3. Cancelou só o horário

**Você:** Cancela só essa visita. Depois combinamos outra data.

**Taliya:** Visita cancelada. Mantive o serviço e o histórico.

**Resultado:** Ocorrência Cancelada · Serviço mantido · Sem horário ativo.

### 4. Consultou

**Você:** Como ficou o serviço do Carlos?

**Taliya:** O serviço foi mantido, com a última visita cancelada e sem nova data marcada.

**Resultado:** Histórico preservado · Nenhum novo atendimento criado.

**Fechamento do cenário**

> Remarcar não duplica. Cancelar horário não apaga o serviço nem um pagamento.

Não publicar: Não mostrar comunicação automática com Carlos; não inferir cancelamento de contrato.

**Controles:** Passo anterior · Próximo passo · Recomeçar exemplo. Nenhuma ação é executada no produto.

## FL03 — Recebeu, consultou, lembrou

**Título do cenário**

> Registrar hoje facilita a cobrança de depois.

Contexto fictício: Limpeza de Ana: total R$450; sem pagamentos antes do primeiro passo.

### 1. Recebeu uma parte

**Você:** A Ana pagou R$300 da limpeza.

**Taliya:** Registrei R$300 recebidos. Restam R$150.

**Resultado:** Combinado R$450 · Recebido R$300 · Restante R$150.

### 2. Voltou para consultar

**Você:** Quanto falta receber da limpeza da Ana?

**Taliya:** Ainda há R$150 em aberto nesse serviço.

**Resultado:** Consulta do mesmo saldo; nenhuma nova cobrança.

### 3. Pediu um aviso

**Você:** Me lembra segunda às 9h de cobrar esse restante.

**Taliya:** Lembrete criado para 21/09, às 9h: cobrar R$150 da Ana.

**Resultado:** Lembrete para o dono · R$150 · Limpeza da Ana.

### 4. Preparou o contato

**Você:** Escreve uma mensagem curta para eu cobrar a Ana.

**Taliya:** Sugestão: “Oi, Ana! Tudo bem? Ficaram R$150 da limpeza do sofá. Pode me confirmar quando consegue fazer o pagamento?”

**Resultado:** Texto preparado para o profissional revisar e enviar.

**Fechamento do cenário**

> A Taliya organiza o saldo, lembra você e pode ajudar a preparar o texto. O envio à cliente é seu.

Não publicar: Não gerar Pix/link de cobrança; não marcar mensagem enviada; rascunho não é cobrança automática.

**Controles:** Passo anterior · Próximo passo · Recomeçar exemplo. Nenhuma ação é executada no produto.

## FL04 — Pacote e sessões

**Título do cenário**

> O pacote não precisa virar uma contagem paralela.

Contexto fictício: João contratou oito aulas por R$600. Datas sem conflito e duração de uma hora informada.

### 1. Vendeu

**Você:** João fechou oito aulas por R$600.

**Taliya:** Pacote registrado com oito aulas e valor de R$600.

**Resultado:** Contratadas: 8 · Realizadas: 0 · Reservadas: 0 · Disponíveis: 8.

### 2. Marcou duas

**Você:** Marca as duas primeiras nos dias 22 e 24 de setembro, das 7h às 8h.

**Taliya:** Duas aulas marcadas. Restam seis unidades disponíveis para agendar.

**Resultado:** Contratadas: 8 · Realizadas: 0 · Reservadas: 2 · Disponíveis: 6.

### 3. Informou realização

**Você:** A aula do dia 22 aconteceu.

**Taliya:** Registrei essa aula como realizada.

**Resultado:** Contratadas: 8 · Realizadas: 1 · Reservadas: 1 · Disponíveis: 6.

Este passo ocorre em um momento posterior do exemplo, depois da aula; não no relógio inicial 18/09.

### 4. Consultou

**Você:** Quantas aulas ainda faltam?

**Taliya:** Faltam sete aulas para realizar: uma está agendada e seis estão disponíveis para agendar.

**Resultado:** Realizadas: 1 · Agendadas: 1 · Disponíveis: 6.

**Fechamento do cenário**

> Agendada não é realizada. O saldo distingue o que aconteceu e o que já está reservado.

Não publicar: Não concluir por passagem de tempo; passadas sem confirmação mantêm reserva. Não confundir sete a realizar com seis disponíveis.

**Controles:** Passo anterior · Próximo passo · Recomeçar exemplo. Nenhuma ação é executada no produto.

## FL05 — Arquivo e contexto

**Título do cenário**

> Ache o documento sem lembrar o nome do arquivo.

Contexto fictício: Instalação da Empresa Norte; contrato e uma revisão enviados pelo próprio profissional.

### 1. Guardou

**Você:** Guarda esse PDF na instalação da Empresa Norte.

**Taliya:** PDF anexado ao serviço da Empresa Norte.

**Resultado:** Serviço · Arquivo contrato-v1.pdf · Vínculo confirmado.

### 2. Identificou

**Você:** Esse documento é o contrato daquela instalação.

**Taliya:** Identifiquei o arquivo como contrato da instalação.

**Resultado:** Tipo contrato · Mesmo arquivo e serviço.

### 3. Encontrou depois

**Você:** Cadê o contrato da instalação da Empresa Norte?

**Taliya:** Encontrei o contrato ligado a esse serviço.

**Resultado:** Documento recuperado para consulta.

### 4. Acrescentou a revisão

**Você:** Guarda este PDF como uma nova versão, mantendo a anterior.

**Taliya:** Nova versão guardada. A anterior continua no histórico.

**Resultado:** Versão2 · Versão1 preservada · Sem aprovação implícita.

**Fechamento do cenário**

> O material fica ligado ao trabalho e pode ser recuperado pela conversa ou pelo app.

Não publicar: Aprovação comercial não vem de upload. Mockup não deve permitir download de documento inexistente.

**Controles:** Passo anterior · Próximo passo · Recomeçar exemplo. Nenhuma ação é executada no produto.

# S09. Como começar — quatro etapas

**Título**

> Comece pequeno. Continue do seu jeito.

**Subtítulo — pré-lançamento**

> Este é o caminho planejado para os primeiros testes. Você não precisa preparar o negócio inteiro para começar.

**Subtítulo — lançamento**

> Comece com o básico e registre algo que já faz parte da sua rotina.



| Etapa | Título | Copy final |
| --- | --- | --- |
| 1 | Crie sua conta | Informe o básico sobre você e seu negócio. A conta mantém seus registros no lugar certo. |
| 2 | Conte o que você faz | Adicione os serviços habituais ou escolha completar conforme usar. Não precisa definir todos os preços e horários agora. |
| 3 | Registre algo da rotina | Depois de vincular seu número, fale com a Taliya pelo WhatsApp. Ou use o app para registrar um serviço, um horário ou um lembrete. |
| 4 | Volte quando precisar | Consulte, corrija e acrescente informações. O que você não usa não vira uma etapa obrigatória. |

1 / regra: Identidade/configuração inicial no fluxo do app; não alegar zero cadastro.

2 / regra: Padrão reutilizável só é salvo com confirmação; evitar “aprende tudo sozinho”.

3 / regra: Primeiro recebimento exige seu contexto mínimo, não lançamento financeiro sem serviço.

4 / regra: Uso parcial não habilita respostas completas sobre dados ausentes.

Remover do onboarding da landing: conectar mídias sociais, migrar WhatsApp Business do studio, escolher agentes, configurar respostas automáticas e treinamento consultivo obrigatório. Não trocar apenas “studio” por “negócio”.

# S10. Entrada e oferta

**Pré-lançamento — título**

> Quer testar a Taliya primeiro?

**Texto**

> Estamos preparando uma forma mais simples de organizar a rotina de quem presta serviços. Deixe seu contato para receber um aviso sobre os primeiros testes.

**Aviso**

> Cadastro de interesse. O produto ainda não está disponível e não há cobrança nesta etapa.

Este é o destino #comecar de todos os CTAs primários no modo ativo. Renderizar o formulário WAITLIST abaixo. Sem tabela de planos, cobrança ou contador de vagas.

## Formulário de interesse — copy e estados



| Campo | Label / placeholder | Erro |
| --- | --- | --- |
| name | Seu nome<br>Como você prefere ser chamado? | Informe seu nome. |
| email | Seu e-mail<br>voce@exemplo.com | Confira o e-mail informado. |
| contactPermission | Quero receber avisos por e-mail sobre os testes e o lançamento da Taliya.<br> | Confirme que deseja receber o aviso para continuar. |

**privacyText:** Usaremos este contato para os avisos que você pediu. Consulte como seus dados serão tratados.

**privacyLinkLabel:** Política de privacidade

**submit:** Quero testar primeiro

**submitting:** Enviando cadastro…

**successTitle:** Cadastro recebido.

**success:** Seu interesse foi registrado. Não há cobrança nem acesso imediato ao produto nesta etapa.

**errorTitle:** Não conseguimos concluir agora.

**error:** Seus dados continuam aqui. Tente novamente.

**retry:** Tentar novamente

**unknown:** Estamos conferindo se o cadastro foi recebido. Não envie de novo ainda.

**back:** Voltar para os exemplos

Contato padrão por e-mail. Não exigir telefone, CNPJ, ticket ou diagnóstico para entrar na lista. O checkbox expressa o pedido de contato; tratamento, base legal e retenção precisam constar da política final.

## Oferta de lançamento — pronta, mas bloqueada

**Título**

> Um plano. Sua rotina conectada.

**Apoio**

> WhatsApp e app no mesmo plano, sem escolher um agente para cada necessidade.



| Período | Preço | Descrição |
| --- | --- | --- |
| Mensal | R$59,90 | por mês<br>Assinatura mensal. |
| Anual | R$599 | por ano<br>Assinatura anual. O total do período é R$599. |

- Clientes e serviços no mesmo contexto.

- Agenda, remarcações e cancelamentos.

- Orçamentos, arquivos e histórico.

- Recebimentos e lembretes.

- Operação pelo WhatsApp e edição no app.

**Teste**

> 14 dias para testar, sem cartão.

**CTA:** Começar 14 dias grátis

Confira os termos, as condições de uso e a forma de assinatura antes de contratar.

Gerencie a renovação no canal em que fez a assinatura. O caminho fica indicado na sua conta.

- Preço e período iguais no site, app e checkout.

- Trial de14 dias sem cartão real.

- Política e limites de uso definidos.

- Destino de onboarding configurado e testado.

Oferta de referência: S3 p.25; valores são a oferta especificada, não uma cotação nova nem preços verificados em produção.

**Fundador — não renderizar por padrão**

> Oferta de fundador: R$39,90 por mês por 12 meses. Válida apenas para as primeiras 100 contas elegíveis; confira a elegibilidade antes de contratar.

Oferta de fundador existe na especificação de produto, mas depende de elegibilidade/limite. Não publicar contador, urgência ou preço promocional universal. Não acrescentar “sem limites”, desconto fictício ou promessa de preço permanente.

# S11. Prova real — reservada, sem renderizar

Não renderizar a seção enquanto não houver caso real aprovado. Não exibir skeleton, estrelas, perfis ou depoimentos de exemplo no site público. Não transforma creators pagos em clientes satisfeitos.

**Título futuro, só com prova**

> Como a Taliya entra na rotina de quem trabalha por conta

- identificação autorizada

- rotina real utilizada

- relato autorizado

- data e contexto

- evidência de qualquer número publicado

Não preencher um card com “nome do cliente”, lorem ipsum ou foto de banco de imagens para parecer depoimento. A ausência de prova real não deve bloquear uma landing honesta de pré-lançamento.

# S12. FAQ — 14 respostas completas

**Título**

> Dúvidas antes de começar?

**Subtítulo**

> Entenda os canais, o que fica registrado e os limites da proposta.

Reutilizar accordion atual, com todas as perguntas fechadas inicialmente. Deep link para FAQ abre somente a pergunta indicada. Dois grupos visuais são permitidos, mas a ordem de leitura permanece contínua. Não inserir avisos de desenvolvimento dentro da resposta de lançamento.

## O que é a Taliya?

**ID:** faq-produto

**Pré-lançamento:** A Taliya está sendo criada para organizar a rotina de quem trabalha por conta e presta serviços. A proposta reúne clientes, serviços, agenda, orçamentos, recebimentos, lembretes e arquivos no mesmo contexto. As demonstrações desta página mostram a experiência planejada.

**Lançamento:** A Taliya organiza a rotina de quem trabalha por conta e presta serviços. Você registra, consulta e ajusta informações pelo WhatsApp ou pelo app, mantendo clientes, serviços, horários, documentos e recebimentos relacionados.

## Posso usar só pelo WhatsApp no dia a dia?

**ID:** faq-whatsapp

**Pré-lançamento:** Esse é um dos objetivos: depois de criar a conta e vincular seu número, registrar, consultar e ajustar a rotina pela conversa. O app complementa a experiência e pode ser necessário para conta, permissões, privacidade ou assinatura. Não estamos prometendo que nunca será preciso abri-lo.

**Lançamento:** Depois de criar a conta e vincular seu número, você pode resolver a rotina coberta pela Taliya pelo WhatsApp: registrar serviços, consultar horários, remarcar, informar pagamentos e pedir lembretes. O app oferece visão geral e edição manual; conta, permissões, privacidade e assinatura podem exigir app ou página segura.

## Preciso ter WhatsApp Business?

**ID:** faq-business

**Pré-lançamento:** Não para a experiência principal que estamos construindo. Você conversa com o número da Taliya usando seu WhatsApp comum. Isso é diferente de conectar o número comercial que atende seus clientes.

**Lançamento:** Não para conversar com a Taliya. Você usa seu WhatsApp comum para falar com o número da Taliya. Não é necessário conectar as conversas do seu negócio com os clientes para usar a proposta principal.

## A Taliya lê minhas outras conversas?

**ID:** faq-conversas

**Pré-lançamento:** Não. A proposta usa o que você informa na conversa com a Taliya e os dados de integrações que você autorizar. Ela não ganha acesso automático aos seus outros chats.

**Lançamento:** Não. Falar com a Taliya não dá acesso automático às suas outras conversas. Você precisa informar ou encaminhar o que for relevante, ou autorizar uma integração disponível.

## Preciso cadastrar tudo ou usar todas as funções?

**ID:** faq-cadastro

**Pré-lançamento:** Não. Estamos preparando um início com dados mínimos e cadastro progressivo. A ideia é começar por agenda, recebimentos de serviços ou lembretes, sem percorrer todas as etapas. Cada consulta depende do que estiver registrado.

**Lançamento:** Não. Comece pela parte de que precisa. A Taliya pergunta o dado que faltar para aquela ação; informações opcionais podem ser completadas depois. Você não precisa acompanhar início, conclusão e pagamento de todo serviço só porque o agendou.

## Serve para meu jeito de prestar serviços?

**ID:** faq-encaixe

**Pré-lançamento:** A primeira versão foi planejada para profissionais solo e pequenos negócios com uma agenda operacional, trabalhando com serviços avulsos, pacotes, mensalidades, várias datas ou recorrência. Equipes com agendas independentes, turmas, estoque e gestão de projetos especializada não estão incluídos nessa proposta.

**Lançamento:** A Taliya atende diferentes modelos de serviço: avulso, pacote de sessões, plano por período, várias datas e recorrência. O foco desta versão é uma operação de agenda única. Ela não substitui recursos especializados de turmas, estoque, prontuário ou gestão de equipes com agendas independentes.

## Dá para preparar e revisar orçamentos?

**ID:** faq-orcamentos

**Pré-lançamento:** Sim, isso está previsto: preparar uma proposta com escopo e preço, revisar versões e registrar a aprovação no mesmo serviço. Gerar o documento não significa que ele foi enviado, aprovado ou pago.

**Lançamento:** Você pode pedir um orçamento com as informações do serviço, revisar itens e valores, gerar uma versão e registrar quando o cliente aprovar. A proposta e o combinado ficam no mesmo serviço. O envio ao cliente é uma ação separada.

## Como funcionam recebimentos e cobrança?

**ID:** faq-cobranca

**Pré-lançamento:** Você informa quanto recebeu e a que serviço o pagamento pertence. A Taliya foi planejada para mostrar recebido e restante, lembrar você de cobrar e ajudar a preparar o texto. Não estamos prometendo detecção automática de Pix, movimentação bancária ou cobrança enviada ao cliente.

**Lançamento:** Você informa os pagamentos, e a Taliya mantém o saldo do serviço. Também pode criar um lembrete e preparar um texto para você enviar. Ela não movimenta seu dinheiro nem sabe automaticamente de um Pix que não foi informado ou recebido por integração autorizada disponível.

## E se eu remarcar ou cancelar?

**ID:** faq-mudancas

**Pré-lançamento:** A experiência planejada atualiza o mesmo atendimento, sem recriar o trabalho. Cancelar só um horário é diferente de cancelar a contratação. Pagamentos e histórico não devem desaparecer com o cancelamento.

**Lançamento:** Ao remarcar, a Taliya atualiza a mesma ocorrência e verifica os conflitos conhecidos. Ao cancelar, considera o alcance do seu pedido. Cancelar um horário não cancela automaticamente o serviço nem devolve valores recebidos.

## Posso vender pacotes ou cobrar mensalidade?

**ID:** faq-pacotes

**Pré-lançamento:** Esses modelos estão previstos. Pacote é uma quantidade total de sessões; plano é uma contratação por período. As sessões agendadas e realizadas são tratadas separadamente, e a cobrança não é multiplicada pelo número de visitas por acidente.

**Lançamento:** Sim. Registre um pacote com quantidade total ou um plano por período. Os horários podem ser marcados depois. Uma sessão só conta como realizada quando esse fato é registrado; consulta de saldo distingue realizadas, reservas e unidades disponíveis.

## E se a Taliya entender algo errado?

**ID:** faq-correcao

**Pré-lançamento:** A proposta inclui confirmar o resultado da ação e permitir correção pelo WhatsApp ou pelo app. Se houver duas interpretações importantes, a conversa deve esclarecer antes de alterar o registro.

**Lançamento:** Confira a resposta e informe a correção pela conversa ou edite no app. A próxima consulta usa a informação atualizada. Operações ambíguas ou sensíveis podem precisar de esclarecimento ou confirmação.

## Onde ficam fotos, PDFs e documentos?

**ID:** faq-arquivos

**Pré-lançamento:** A ideia é guardar os materiais junto ao negócio ou serviço correspondente, para recuperar pelo contexto. Um arquivo anexado não deve virar aprovação comercial ou confirmação bancária por conta própria.

**Lançamento:** Os materiais ficam vinculados ao contexto indicado, como o serviço da Marina. Você pode encontrá-los depois pela conversa ou pelo app. Versões e aprovações são distintas; anexar um PDF não significa aprovar seus termos.

## A Taliya fala com meus clientes ou deixa eles agendarem?

**ID:** faq-clientes

**Pré-lançamento:** Não na proposta-base desta primeira versão. Aqui, quem conversa com a Taliya é o profissional. Atendimento automático ao cliente, envio ativo e link público de autoagendamento não devem ser confundidos com o copiloto descrito nesta página.

**Lançamento:** A proposta-base é você conversando com a Taliya para organizar o trabalho. Ela pode preparar textos e documentos para você compartilhar, mas não oferece nesta versão atendimento automático aos clientes nem link público de autoagendamento.

## Quanto custa e como começo?

**ID:** faq-preco

**Pré-lançamento:** Ainda não estamos abrindo assinaturas. Você pode entrar na lista de interesse, sem cobrança, para receber um aviso sobre os primeiros testes. Preço e condições serão apresentados antes de qualquer contratação.

**Lançamento:** A Taliya custa R$59,90 por mês ou R$599 por ano, com 14 dias de teste sem cartão. Confira as condições na tela de assinatura. Para gerenciar a renovação ou cancelar, use o canal de compra indicado na sua conta.

# S13. Seu trabalho funciona de outro jeito?

**Título**

> Seu trabalho funciona de outro jeito?

**Texto**

> Conte uma rotina que você precisa organizar. Isso ajuda a entender onde a Taliya se encaixa, onde atende só uma parte e o que deve ficar para depois.



| Campo | Label / placeholder | Erro |
| --- | --- | --- |
| routine | Qual rotina você precisa organizar?<br>Ex.: recebo uma entrada, faço o serviço em três dias e cobro o saldo na entrega. Ou vendo oito sessões sem horário fixo. | Conte brevemente a rotina que você quer organizar. |
| email | Seu e-mail<br>voce@exemplo.com | Confira o e-mail informado. |

**helper:** Não inclua dados de clientes, documentos pessoais ou informações sensíveis.

**privacyText:** Seu contato será usado para tratar este relato. Este formulário não inscreve você automaticamente em campanhas.

**submit:** Enviar minha rotina

**submitting:** Enviando rotina…

**successTitle:** Rotina recebida.

**success:** Obrigado por contar como você trabalha. O envio não garante uma funcionalidade sob medida nem uma data de lançamento.

**errorTitle:** Não conseguimos enviar agora.

**error:** Seu texto foi mantido. Tente novamente.

**retry:** Tentar novamente

Reaproveitar a textarea de “agente específico”. O conteúdo não promete criar agente sob medida, retorno comercial imediato nem suporte a qualquer profissão. Este envio não ativa uma inscrição de marketing sem pedido separado.

## Contrato comum dos formulários

- Validação antes do envio; erro junto ao campo; foco no primeiro erro.

- Enviar apenas ao endpoint configurado. Identificar formKind e requestId único por tentativa lógica.

- Sucesso somente com confirmação do servidor. Em timeout de resultado desconhecido, verificar antes de reenviar; não simular sucesso com timer.

- Deduplicar solicitações por chave; não revelar se um terceiro já está cadastrado.

- Reusar e-mail preenchido nesta sessão, com revisão visível. Não ler contatos do aparelho.

- Não salvar texto sensível em analytics. Rate limit e proteção de abuso são responsabilidades da integração.

- Nome/email/rotina não são enviados à camada de eventos de marketing.

- Sem endpoint ativo, publicação da captura fica bloqueada: não trocar por um formulário decorativo.

# S14. CTA final, footer e flutuante

**Título final**

> Seu negócio não precisa ficar só na sua cabeça.

**Texto — pré-lançamento**

> Acompanhe a Taliya desde o começo. Cadastre-se para saber quando os primeiros testes estiverem disponíveis.

**Texto — lançamento**

> Comece por uma rotina. Registre, consulte e continue pelo WhatsApp ou pelo app.

**CTA principal:** herdado do modo ativo; não inventar novo destino no rodapé.

**Tagline**

> Taliya organiza o contexto de quem trabalha por conta: clientes, serviços, agenda, orçamentos, recebimentos, lembretes e arquivos.



| Link | Destino |
| --- | --- |
| Privacidade | /privacidade |
| Termos de uso | /termos |
| Dados usados | /privacidade#dados |
| IA e WhatsApp | /privacidade#ia-whatsapp |
| Pagamento | /privacidade#pagamento |
| Seus direitos | /privacidade#direitos |

**Suporte:** Equipe Taliya · contato@taliya.com.br

© 2026 Taliya. Todos os direitos reservados.

**CTA flutuante:** modes[activeMode].primaryCta

No mobile, evitar sobreposição com campos, teclado e controles das demos. Suporte humano aparece como alternativa, não como chatbot em funcionamento.

Remover avatar e bolinha “1” que simulam uma notificação não ocorrida. Usar a marca. O contato humano não é o número do produto e deve estar identificado como equipe. Confirmar endereço e destino antes de publicar.

# Anexo A. Biblioteca completa — 84 mensagens

Cada frente tem 12 mensagens. Elas não são comandos obrigatórios; são amostras de linguagem. Mensagens incompletas dependem do contexto ou de esclarecimento. O JSON traz uma nota de contexto por frase; não publicar essas notas como promessa de execução imediata.

## Clientes



| ID | Mensagem publicável | Destino |
| --- | --- | --- |
| MSG-CL01 | Cadastra a Marina com esse contato. | CL01 |
| MSG-CL02 | Qual é o telefone da Empresa Norte? | CL02 |
| MSG-CL03 | O que eu já fiz para o Carlos? | CL04 |
| MSG-CL04 | Quando foi o último serviço concluído da Júlia? | CL04 |
| MSG-CL05 | Me mostra os serviços ativos da Marina. | CL02 |
| MSG-CL06 | O que ficou combinado com a Ana? | CL02 |
| MSG-CL07 | A Empresa Norte tem algum valor em aberto? | CL02 |
| MSG-CL08 | Atualiza o e-mail da Marina para marina@example.com. | CL03 |
| MSG-CL09 | Aquela instalação é da Camila, não da Carla. | CL05 |
| MSG-CL10 | Me mostra o histórico desse cliente. | CL04 |
| MSG-CL11 | É a Marina do telefone final 8421. | CL01 |
| MSG-CL12 | O endereço dessa visita é Rua das Flores, 120. | CL03 |

## Serviços



| ID | Mensagem publicável | Destino |
| --- | --- | --- |
| MSG-SV01 | Fechei uma limpeza de sofá para a Luana por R$250. | SV02 |
| MSG-SV02 | Registra a instalação do Carlos por R$750. | SV02 |
| MSG-SV03 | Ana pediu um orçamento de limpeza. | SV01 |
| MSG-SV04 | João fechou oito aulas por R$600. | SV03 |
| MSG-SV05 | Vou marcar as sessões do pacote depois. | SV03 |
| MSG-SV06 | Carlos entrou no plano mensal de R$350 a partir de outubro. | SV04 |
| MSG-SV07 | Essa pintura vai de segunda a quarta. | SV05 |
| MSG-SV08 | Esse trabalho tem duas visitas, nos dias 22 e 24. | SV05 |
| MSG-SV09 | Terminei o serviço inteiro da Marina. | SV06 |
| MSG-SV10 | Cancela a contratação da instalação do Carlos. | SV06 |
| MSG-SV11 | A mensalidade da jardinagem é fixa, não por visita. | SV04 |
| MSG-SV12 | Esse valor é só para esta instalação. | SV02 |

## Agenda



| ID | Mensagem publicável | Destino |
| --- | --- | --- |
| MSG-AG01 | Marca a Júlia amanhã às 14h por uma hora. | AG01 |
| MSG-AG02 | Agenda a manutenção sexta às 10h por duas horas. | AG01 |
| MSG-AG03 | O que eu tenho hoje? | AG02 |
| MSG-AG04 | Como está minha agenda amanhã? | AG02 |
| MSG-AG05 | Quem é meu primeiro cliente amanhã? | AG02 |
| MSG-AG06 | Quais horários já tenho ocupados na sexta? | AG02 |
| MSG-AG07 | Passa a Júlia de quinta para sexta às 10h. | AG04 |
| MSG-AG08 | Muda a visita da Empresa Norte para as 14h. | AG04 |
| MSG-AG09 | Cancela só o atendimento da Ana de amanhã. | AG05 |
| MSG-AG10 | Marca quatro aulas, às terças, das 7h às 8h, a partir do dia 22. | AG06 |
| MSG-AG11 | Tenho uma janela livre de uma hora na sexta? | AG03 |
| MSG-AG12 | Remarca só esta sessão, não as próximas. | AG04 |

## Orçamentos



| ID | Mensagem publicável | Destino |
| --- | --- | --- |
| MSG-OR01 | Faz um orçamento de instalação de R$850 para a Marina. | OR01 |
| MSG-OR02 | Orça duas luminárias por R$300 cada e instalação por R$250. | OR01 |
| MSG-OR03 | Adiciona R$180 de material ao orçamento. | OR02 |
| MSG-OR04 | Inclui a instalação de R$250 nessa proposta. | OR02 |
| MSG-OR05 | Troca a mão de obra da proposta para R$550. | OR03 |
| MSG-OR06 | Remove esse item do orçamento. | OR02 |
| MSG-OR07 | Faz uma nova versão com R$100 de desconto. | OR03 |
| MSG-OR08 | A Marina aprovou a versão 2 do orçamento. | OR04 |
| MSG-OR09 | O cliente recusou esta proposta. | OR04 |
| MSG-OR10 | Qual foi o último orçamento que preparei para o Carlos? | OR05 |
| MSG-OR11 | Cadê a versão aprovada da Empresa Norte? | OR05 |
| MSG-OR12 | Gera o PDF da versão atual para eu compartilhar. | OR05 |

## Recebimentos



| ID | Mensagem publicável | Destino |
| --- | --- | --- |
| MSG-RC01 | A Ana pagou os R$450 da limpeza. | RC01 |
| MSG-RC02 | Recebi R$250 da Luana pelo sofá. | RC01 |
| MSG-RC03 | A Marina pagou R$300 e ainda faltam R$150. | RC02 |
| MSG-RC04 | Entraram R$500 daquele serviço. | RC02 |
| MSG-RC05 | Ele pagou metade hoje. | RC02 |
| MSG-RC06 | Recebi R$200 de sinal da instalação do Carlos. | RC03 |
| MSG-RC07 | Quanto falta a Ana pagar pela limpeza? | RC04 |
| MSG-RC08 | Qual é o saldo do serviço da Marina? | RC04 |
| MSG-RC09 | Quem ainda tem valor em aberto? | RC04 |
| MSG-RC10 | Quanto registrei como recebido neste mês? | RC04 |
| MSG-RC11 | Corrige aquele pagamento: foram R$350, não R$300. | RC05 |
| MSG-RC12 | O Carlos pagou a mensalidade de outubro. | RC06 |

## Lembretes



| ID | Mensagem publicável | Destino |
| --- | --- | --- |
| MSG-LE01 | Me lembra segunda às 9h de cobrar os R$150 da Ana. | LE01 |
| MSG-LE02 | Amanhã às 10h me lembra do restante da Marina. | LE01 |
| MSG-LE03 | Me lembra terça às 10h de falar com a Júlia. | LE02 |
| MSG-LE04 | Daqui a 30 dias, às 9h, me lembra de procurar o Carlos. | LE02 |
| MSG-LE05 | Me lembra amanhã às 8h de levar o equipamento. | LE03 |
| MSG-LE06 | Uma hora antes, me lembra dessa visita. | LE05 |
| MSG-LE07 | Me lembra segunda às 9h de revisar o orçamento. | LE04 |
| MSG-LE08 | Toda segunda às 9h me lembra de revisar as propostas. | LE04 |
| MSG-LE09 | Sexta às 9h me avisa se esses R$300 ainda estiverem em aberto. | LE06 |
| MSG-LE10 | Quais lembretes eu tenho para amanhã? | LE02 |
| MSG-LE11 | Muda esse lembrete para sexta às 10h. | LE01 |
| MSG-LE12 | Pausa o lembrete semanal de revisar propostas. | LE04 |

## Arquivos e documentos



| ID | Mensagem publicável | Destino |
| --- | --- | --- |
| MSG-AR01 | Guarda esse PDF no serviço da Marina. | AR01 |
| MSG-AR02 | Salva essa foto na instalação do Carlos. | AR01 |
| MSG-AR03 | Esse é o contrato da instalação da Empresa Norte. | AR01 |
| MSG-AR04 | Guarda esse comprovante na limpeza da Ana. | AR01 |
| MSG-AR05 | Anexa essas fotos ao trabalho da Júlia. | AR01 |
| MSG-AR06 | Cadê o orçamento aprovado da Marina? | AR02 |
| MSG-AR07 | Me mostra as fotos daquele serviço. | AR02 |
| MSG-AR08 | Procura o contrato da Empresa Norte. | AR02 |
| MSG-AR09 | Me mostra os documentos dessa instalação. | AR02 |
| MSG-AR10 | Esse PDF é uma nova versão da proposta. | AR03 |
| MSG-AR11 | Esse arquivo é da Marina, não da Ana. | AR05 |
| MSG-AR12 | Prepara um recibo daquele pagamento de R$300. | AR04 |

# Anexo B. Contratos de implementação

**stageSwitch:** Resolver modos em um único lugar. Não permitir hero de waitlist com checkout ativo no footer nem trial no preço sem trial no onboarding.

**publicData:** Somente strings voltadas ao visitante são renderizadas. Guardrails, fontes, contextos técnicos e nulls de runtime não aparecem no HTML público.

**sourceOfTruth:** Editar o JSON e regenerar documentos quando mudar copy. PDF é leitura humana, não origem para extração de textos.

**noNewAppModules:** Não criar módulos de Orçamentos, Arquivos ou Histórico no app por existirem frentes da landing.

## B1. Rotas, âncoras e legado



| Origem | Destino / tratamento |
| --- | --- |
| / | Nova home horizontal<br>Remover redirecionamento antigo para /pilates. |
| /pilates | /<br>Redirecionamento permanente quando o produto antigo não estiver mais em oferta; conservar o fragmento e aplicar aliases no cliente. |
| /pilates/planos | /#comecar<br>Retirar a oferta antiga da jornada; redirecionar somente quando o pivot estiver publicado. |



| Âncora antiga | Alias novo |
| --- | --- |
| intencoes | na-pratica |
| diagnostico-operacional | sem-com |
| agentes | o-que-resolve |
| dinheiro-na-mesa | fluxos |
| faq | duvidas |
| cta-final | final |
| vendas | comecar |

Não presumir que um fragmento chega ao servidor. O código da página de destino deve reconhecer os aliases e rolar para o bloco novo. Manter uma única rota canônica para a nova home; apagar o redirecionamento inverso antes de ativar os destinos antigos.

## B2. Metadados prontos

**Title:** Taliya | Seu negócio organizado. É só falar.

**Canonical:** https://www.taliya.com.br/

**Description — pré-lançamento:** Conheça a Taliya: organização de serviços pelo WhatsApp e app. Veja exemplos de agenda, orçamentos e recebimentos e acompanhe os primeiros testes.

**Description — lançamento:** Organize serviços, agenda, orçamentos e recebimentos pelo WhatsApp. Consulte e corrija sua rotina na conversa ou veja os mesmos registros no app.

**OG title:** Taliya — Seu negócio organizado. É só falar.

**OG description:** A rotina de quem presta serviços, conectada pelo WhatsApp e pelo app.

**OG imageSpec:** Composição original com marca + promessa + conversa ilustrativa; sem números de usuários ou tela bancária.

**OG imageSizeDesign:** 1200 × 630

**OG alt:** Taliya: mensagem do profissional e resumo do mesmo serviço.

- Um H1 no hero; títulos de seção H2 e subtítulos H3.

- Metadados do pré-lançamento não afirmam disponibilidade.

- Sem avaliações/estrelas inventadas em dados estruturados.

- Políticas, sitemap e imagem social seguem o domínio canônico.

- Não criar novas páginas verticais vazias para SEO.

## B3. Comportamentos e microcopy compartilhados



| Estado | Copy |
| --- | --- |
| previousExample | Exemplo anterior |
| nextExample | Próximo exemplo |
| restart | Recomeçar exemplo |
| showResult | Resultado do exemplo |
| playDemo | Reproduzir demonstração |
| pauseDemo | Pausar demonstração |
| unavailable | Não foi possível carregar este exemplo. |
| retry | Tentar novamente |
| imageFallback | O exemplo em texto continua disponível abaixo. |
| invalidDeepLink | Abrir primeiro exemplo |
| noRealAction | Demonstração: nenhuma ação real será executada. |

- Verificar em 320, 390, 768, 1280 e 1440 px; são larguras de QA, não breakpoints impostos ao projeto.

- Não alterar tokens visuais sem necessidade demonstrada.

- Dois níveis de tabs no máximo; regiões horizontais não expandem a largura do body.

- Chat legível sem zoom; resultado no fluxo da página e não escondido num modal obrigatório.

- Preservar posição do usuário na troca de tab; anchor respeita altura do header.

- Faixa de confiança: quatro itens no desktop; duas ou uma coluna no mobile, conforme os tokens existentes.

- Mural estático no primeiro carregamento; reduzir movimento por preferência.

- Não adicionar vídeo pesado ou carregamento de app real para demonstrar interação.

- Carrosséis com botão anterior/próximo e seleção direta; swipe opcional, não único controle.

- Todos os botões têm foco visível e label acessível; textos informativos não dependem só de cor.

## B4. Instrumentação

Eventos sem transcrição, nome, e-mail, telefone, anexos ou relato de rotina. Click não equivale a lead; lead só após servidor.



| Evento | Propriedades permitidas |
| --- | --- |
| landing_cta_click | section_id, cta_id, mode |
| selector_case_change | case_id, mode |
| comparison_change | front_id, side |
| how_tab_change | tab_id |
| message_example_open | message_id, front_id, subtype_id |
| front_example_change | front_id, subtype_id |
| flow_step_change | scenario_id, step_index |
| faq_open | faq_id |
| lead_submit_success | form_kind, mode |
| lead_submit_error | form_kind, error_class |
| billing_period_change | period, mode |

Reutilizar a medição existente e política de consentimento aplicável; parâmetros de campanha são metadados separados. Não criar eventos first_operation ou pagamento por assistir uma demo.

## B5. Gates reais, não novas pendências de copy



| Gate | Condição | Efeito |
| --- | --- | --- |
| G01 | leadEndpoint ausente ou sem teste | Bloqueia envio do formulário e publicação da jornada de captura. |
| G02 | políticas/termos não revisados para o pivot | Bloqueia publicação da captura; esta especificação não reescreve contratos legais. |
| G03 | produto não funcional ou onboardingUrl ausente | Mantém prelaunch; bloqueia trial/checkout e CTA de uso imediato. |
| G04 | oferta e limites de uso não confirmados | Oculta preço, fundador e alegações de uso ilimitado. |
| G05 | não há prova de cliente real | S11 continua sem renderizar; não bloqueia o restante. |
| G06 | assets reais indisponíveis | Permite mock fiel rotulado; não permite chamar de gravação real. Dados JSON não são capturas da interface aprovada. |

Os nulls no runtime representam dependências externas ainda não fornecidas, não texto incompleto da landing. Quem implementar deve conectar URLs e endpoint reais; não inventar destinos de checkout, políticas ou sucesso de captura.

# Anexo C. Assets e cenários

24 grupos lógicos de assets: 1 hero, 5 seletor, 6 funcionamento, 7 frentes e 5 fluxos. Os estados são definidos no JSON. Não se trata de 24 imagens de interface prontas nem de telas de produto já executadas.



| Asset ID | Seção | Uso |
| --- | --- | --- |
| VIS-HERO | S01 | Conversa de aprovação/entrada e card da instalação da Marina |
| VIS-NP01 | S03 | Fechei um serviço |
| VIS-NP02 | S03 | Mudou o horário |
| VIS-NP03 | S03 | Recebi uma parte |
| VIS-NP04 | S03 | Quero um orçamento |
| VIS-NP05 | S03 | Vendi um pacote |
| VIS-CF01 | S05 | Conte do jeito que for mais fácil. |
| VIS-CF02 | S05 | Não precisa contar a mesma história de novo. |
| VIS-CF03 | S05 | Só falta uma informação? Responda só ela. |
| VIS-CF04 | S05 | O combinado acompanha o serviço. |
| VIS-CF05 | S05 | Sua rotina na conversa. A visão completa no app. |
| VIS-CF06 | S05 | Um jeito de organizar. Vários jeitos de trabalhar. |
| VIS-FR-CL | S07 | Clientes — estados derivados dos subtipos |
| VIS-FR-SV | S07 | Serviços — estados derivados dos subtipos |
| VIS-FR-AG | S07 | Agenda — estados derivados dos subtipos |
| VIS-FR-OR | S07 | Orçamentos — estados derivados dos subtipos |
| VIS-FR-RC | S07 | Recebimentos — estados derivados dos subtipos |
| VIS-FR-LE | S07 | Lembretes — estados derivados dos subtipos |
| VIS-FR-AR | S07 | Arquivos e documentos — estados derivados dos subtipos |
| VIS-FL01 | S08 | Da proposta ao horário, sem refazer o cadastro. |
| VIS-FL02 | S08 | O horário muda. O histórico não se perde. |
| VIS-FL03 | S08 | Registrar hoje facilita a cobrança de depois. |
| VIS-FL04 | S08 | O pacote não precisa virar uma contagem paralela. |
| VIS-FL05 | S08 | Ache o documento sem lembrar o nome do arquivo. |

- Não entregar novas telas como se fossem a galeria aprovada. Reusar a linguagem visual existente; compor mock fiel com a legenda de estágio.

- Nenhum cliente real, contato ou documento identificável. Todos os valores da demo são fictícios.

- Avatares dos antigos agentes não representam agentes da nova Taliya; remover ou substituir pelo símbolo de categoria/brand.

- Sem screenshot disponível, manter resultado textual acessível e rotulado. Não deixar imagem quebrada.

- Telas com saldo, agenda e orçamento seguem o mesmo estado do roteiro, inclusive ao voltar passos.

- No lançamento, as demos só podem representar capacidades verificadas na versão liberada; gravar novamente quando a interface mudar.

- As datas são de um cenário fixo referenciado em 18/09/2026. Não usar Date.now() só nos títulos e deixar os resultados antigos. Ao atualizar datas, regenerar a sequência inteira de cada cenário.

# Anexo D. QA e passagem para desenvolvimento

Checklist para quem implementar. Status de todos os testes do site: não executado nesta entrega. A validação estrutural do dataset foi executada; isso não equivale a testar o produto ou a nova landing.

## Conteúdo



| ID / prioridade | Aceite |
| --- | --- |
| QA01 / P0 | Os 14 slots S01–S14 existem na configuração; S11 fica oculto sem prova. |
| QA02 / P0 | Há 5 casos no seletor, 7 posições Sem/Com, 6 tabs Como funciona, 7 frentes e 39 subtipos. |
| QA03 / P0 | A biblioteca possui 84 mensagens e 24 IDs iniciais válidos; nenhuma aponta para subtipo ausente. |
| QA04 / P0 | Header, hero, oferta, FAQ, CTA final e flutuante usam o mesmo modo. |
| QA05 / P0 | Não há “studio de Pilates”, seleção de agentes nem planos Base/Essencial/Avance/Completo na nova jornada. |
| QA06 / P0 | Mural usa copy própria; não copia a frase longa da marca concorrente. |

## Produto



| ID / prioridade | Aceite |
| --- | --- |
| QA07 / P0 | A conversa representa dono→número da Taliya; nunca cliente→agente do studio. |
| QA08 / P0 | Não afirma leitura automática de outros chats, Pix, Open Finance, emissão fiscal, autoagendamento ou equipe. |
| QA09 / P0 | Agenda sem duração pede só a duração; preço opcional não impede registrar horário. |
| QA10 / P0 | NP05 mostra uma pergunta necessária, sem inventar duração padrão. |
| QA11 / P0 | Em FL01, aprovação muda o mesmo serviço; geração de PDF não significa enviado/aprovado. |
| QA12 / P0 | FL02 cancela a ocorrência e mantém serviço/histórico; pagamentos não desaparecem. |
| QA13 / P0 | FL03 prepara texto de cobrança para o dono; nunca o marca enviado ao cliente. |
| QA14 / P0 | FL04 mostra 8 contratadas, 1 realizada, 1 reservada, 6 disponíveis e 7 a realizar no último passo. |
| QA15 / P0 | Anexar comprovante em AR01 não confirma recebimento nem movimenta banco. |
| QA16 / P0 | Resumo financeiro é sobre valores registrados; não chama de lucro sem despesas. |
| QA17 / P0 | Correção RC05 troca R$300 por R$350, com total de R$450 e saldo de R$100; não soma R$350 como novo pagamento. |
| QA18 / P0 | Sem horário de atendimento, disponibilidade não afirma dia inteiro livre. |

## Estágio



| ID / prioridade | Aceite |
| --- | --- |
| QA19 / P0 | Pré-lançamento tem aviso visível e demos identificadas; nenhum CTA de checkout/uso imediato. |
| QA20 / P0 | Preço/trial não aparecem antes de produto, oferta e destino estarem validados. |
| QA21 / P0 | Prova social não renderiza dados fictícios, skeletons ou estrelas. |

## Formulários



| ID / prioridade | Aceite |
| --- | --- |
| QA22 / P0 | Erro por campo preserva o preenchimento; envio não simula sucesso. |
| QA23 / P0 | Timeout de resultado desconhecido não duplica lead; sucesso depende do servidor. |
| QA24 / P0 | Cadastro de rotina não inscreve em marketing automaticamente. |
| QA25 / P0 | Política/termos revisados e links reais antes da captura. |

## Interação



| ID / prioridade | Aceite |
| --- | --- |
| QA26 / P0 | Trocar frente reinicia subtipo de forma previsível e atualiza todos os textos/resultados. |
| QA27 / P0 | Trocar cenário não carrega saldo/cliente de outro exemplo. |
| QA28 / P1 | Link profundo inválido usa estado inicial, sem erro de página. |
| QA29 / P1 | Todas as opções funcionam sem autoplay; pause/restart são acessíveis quando houver animação. |
| QA30 / P0 | Clique em balão apenas abre exemplo; não envia WhatsApp nem registra dado de negócio. |

## Mobile



| ID / prioridade | Aceite |
| --- | --- |
| QA31 / P0 | Revisar 320, 390, 768, 1280 e 1440 px: sem overflow horizontal da página e sem texto cortado. |
| QA32 / P0 | Botão flutuante não cobre teclado, formulário ou controles e se oculta no formulário. |
| QA33 / P0 | Texto do chat e resultado é legível sem zoom; sem frases dependentes só de cor. |

## Acessibilidade



| ID / prioridade | Aceite |
| --- | --- |
| QA34 / P0 | Foco visível, nome dos controles, teclado, tab selecionada e painel associado funcionam juntos. |
| QA35 / P1 | Movimento reduzido desativa rolagem automática; imagem tem texto alternativo. |

## Rotas



| ID / prioridade | Aceite |
| --- | --- |
| QA36 / P0 | Raiz não redireciona à landing antiga; /pilates e /pilates/planos têm destino definido. |
| QA37 / P1 | Aliases antigos de âncora abrem os blocos novos corretos. |

## SEO



| ID / prioridade | Aceite |
| --- | --- |
| QA38 / P0 | Title, description, canonical, OG e sitemap não descrevem o produto de Pilates. |

## Analytics



| ID / prioridade | Aceite |
| --- | --- |
| QA39 / P0 | Eventos só levam IDs; nenhum e-mail, telefone, relato ou transcrição é enviado. |
| QA40 / P0 | Ver uma demo não dispara first_operation, compra, lead ou teste iniciado. |

## Entrega



| ID / prioridade | Aceite |
| --- | --- |
| QA41 / P1 | Comparação visual com base existente confirma reaproveitamento de tokens e componentes. |
| QA42 / P0 | A revisão final percorre 39 subtipos, 5 fluxos e todas as perguntas; registrar limitações reais. |

## Ordem de execução

**1.** Mapear o repositório e associar os slots/conceitos a componentes reais; não adivinhar caminhos de arquivos.

**2.** Aplicar primeiro o modo prelaunch: texto, âncoras, tags e CTAs sem compra.

**3.** Atualizar componentes existentes: hero, seletor, Sem/Com, 6 tabs, 7 frentes, 4 passos e FAQ.

**4.** Adicionar faixa de confiança e mural; substituir calculadora por cenários de continuidade.

**5.** Conectar os formulários a backend real, com validação, deduplicação e privacidade.

**6.** Revisar todos os cenários e vínculos entre valores, datas e respostas.

**7.** Executar QA responsivo e acessível e revisar as rotas/legado antes de publicar.

**8.** Manter modo launch desligado até comprovar gates de produto, preço e onboarding.

**Definição de pronto desta entrega**

> Conteúdo e comportamento estão especificados. O aceite da implementação exige testar o site; esta entrega não publica a landing, não cria screenshots finais do app e não implementa endpoint.

# Referências e rastreabilidade

Esta especificação transforma a auditoria aprovada em conteúdo de implementação. Não mede conversão nem comprova aderência de mercado. A ordem e as funções dos blocos vêm de S1; fidelidade funcional vem de S2/S3; estágio de publicação vem de S4.

## [S1] Taliya_Auditoria_Final_Landing_vs_Meu_Assessor_2026-09-18.pdf

**Localização:** 20 páginas; especialmente pp. 6–14 e 17–19

**Uso:** Ordem, sete frentes, reaproveitamento, remoção do ROI, novos blocos e limites comerciais.

## [S2] Product_Bible_Copiloto_Servicos_v1_7.md

**Localização:** §§ 1–9, 12, 13 e 22; edição de 14/09/2026

**Uso:** Serviço único; documentos e versões; agenda, reservas e recebimentos independentes; uso parcial; canais.

## [S3] Documento_Mestre_Implementacao_Copiloto_v1_0(1).pdf

**Localização:** p.25 COP-CF08; pp.45–46 OP-CFG-01 / OP-READ-01; pp.55–57 operações de agenda e pagamentos

**Uso:** Oferta especificada; identidade/configuração; preferências por conversa; alterações atômicas; nenhuma movimentação bancária.

## [S4] Decisões desta conversa

**Localização:** Solicitação de manter componentes e aprofundar casos; produto ainda em desenvolvimento

**Uso:** WhatsApp para rotina, app complementar; conteúdo de pré-lançamento; sem reauditoria ou publicação nesta entrega.

Ajustes de precisão aplicados: “orçamento aprovado” mantém o mesmo Serviço; material é item cobrado, não módulo de despesas; cancelamento de horário não cancela contrato; cobrança por texto é preparação/aviso ao dono; regra global não muda sem confirmação; nenhuma promessa de “nunca abrir o app”.

O arquivo estruturado é a referência para os IDs e strings. Capturas, rotas externas e integração de leads precisam ser associadas ao repositório real, sem alterar a arquitetura do produto.
