# Implementar a nova landing da Taliya

Trabalhe no repositório autorizado e use `landing.content.pt-BR.json` e a especificação PDF/DOCX como fonte desta migração. Não publique, compre serviços ou envie mensagens sem autorização do responsável.

## Objetivo

Migrar a landing de Taliya Studios para um único copiloto operacional para quem trabalha por conta e presta serviços. Preservar identidade visual, componentes e padrões existentes. Não copiar personagens, textos extensos ou identidade do Meu Assessor.

## Regras

- Começar em `prelaunch`: aviso de desenvolvimento, exemplos identificados e captura real de interesse.
- Não refazer design system, criar arquitetura de agentes nem novos módulos do aplicativo.
- Mapear o código atual antes de editar: header, hero, seletor, Sem/Com, 6 tabs, 7 categorias/subtabs, calculadora, etapas, FAQ, formulário e footer.
- Reutilizar esses componentes. Remover a matemática de ROI e os sliders; a área vira 5 fluxos de continuidade, após as sete frentes.
- Mural fica entre Como funciona e Sete frentes. Usar 24 mensagens iniciais da biblioteca de 84; redução mobile e navegação manual previstas.
- As 7 frentes comerciais têm 39 subtipos. Histórico e contexto são transversais. Orçamento aprovado permanece no mesmo Serviço.
- WhatsApp é a conversa do dono com o número Taliya, não acesso aos outros chats. App permite visão/revisão e pode ser necessário para conta, permissões e assinatura.
- Não dizer que a Taliya detecta Pix, movimenta dinheiro, emite nota fiscal, cobra o cliente automaticamente ou oferece equipe/autoagendamento público nesta V1.
- Não criar conteúdo placeholder público para prova social. Não ligar trial/preço antes dos gates.
- Não criar endpoints/destinos fictícios. Os nulls do runtime são dependências a resolver com configuração real.
- Nenhum formulário usa timer para simular sucesso. Não enviar PII ou texto de rotina a analytics.
- As cenas são locais e fictícias; clicar não chama o LLM ou o backend do produto.

## Execução

1. Apresente o mapa de componentes reais que receberão cada slot e registre divergências necessárias.
2. Aplique a copy do modo ativo usando o JSON, mantendo o layout e os estados acessíveis.
3. Conecte as referências internas e os cenários sem recomeçar a página a cada troca de tab.
4. Conecte as rotas reais de captura, políticas e suporte. Caso não existam, reporte o bloqueio; não publique uma captura falsa.
5. Execute a validação estrutural local e os testes do repositório.
6. Teste todos os 39 subtipos, 20 passos de fluxos, 14 FAQs e formulários; capture evidências responsivas.
7. Entregue arquivos alterados, testes realizados, evidências e pendências reais. Não afirmar que algo foi implementado ou testado sem executá-lo.

A validação deste pacote não substitui os testes da implementação. Não alterar a Product Bible para fazer uma demo caber.
