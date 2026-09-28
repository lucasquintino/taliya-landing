# Quickstart local — cópia de referência

Use apenas para inspecionar a base antes da migração. Não configure credenciais reais nem conecte serviços externos.

```bash
npm ci
npm run dev
```

Abra `http://localhost:3000/pilates` para o baseline da experiência existente. A rota `/` ainda redireciona para `/pilates` na revisão original.

## Limites

- Não executar scripts `eval:*` do agente; não fazem parte do baseline visual da landing.
- Não enviar formulários a serviços reais.
- Não usar `npm run build` ou testes como evidência de que a migração foi verificada; nenhum código da landing foi migrado nesta etapa.
- Registrar separadamente falhas preexistentes do ambiente ou da aplicação.
