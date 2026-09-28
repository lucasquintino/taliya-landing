# Política de rastreamento — notas de implantação

O exemplo permite todo conteúdo público. Ele não configura autenticação de nenhum dado.

Para aparecer em busca, não bloquear OAI-SearchBot e conferir acesso na CDN/WAF e IPs oficiais. A escolha sobre GPTBot é independente. Caso a Taliya decida não permitir treinamento, pode adicionar um grupo específico para GPTBot com Disallow: /. Isso é uma opção de política, NÃO uma recomendação de ranking.

Se forem criados grupos específicos de outros agentes, revisar se eles passam a substituir o grupo User-agent: *; não presumir que restrições se somem. Não expor arquivos privados por depender de Disallow. Não bloquear CSS/JS público necessário. No staging usar controle de acesso.

Arquivo precisa responder como texto no host correto. Verificar todos os hosts antes de decidir redirecionamentos. Revalidar regras e faixas IP na documentação oficial, sem listas estáticas copiadas desta auditoria.
