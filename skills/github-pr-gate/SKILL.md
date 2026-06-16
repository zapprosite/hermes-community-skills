---
name: github-pr-gate
description: "Gate de qualidade no GitHub antes de PR ser aprovado para merge. #gate-pr"
category: github
platforms: [linux]
---

# Gate GitHub antes de PR ready/merge

## Quando usar
Antes de marcar PR como ready, revisar, aprovar ou mergear.

## Objetivo
Impedir PR pronto/mergeado sem evidência real, rollback e diff limpo.

## Procedimento
1. Confirmar base HEAD e head SHA esperado.
2. Verificar branch não é main para push.
3. Conferir diff.
4. Rodar secret scan.
5. Validar contagem de testes e logs.
6. Confirmar snapshots PRE/POST quando runtime.
7. Confirmar rollback.
8. Conferir PR body sem exagero e coerente com evidência.
9. Só marcar ready se mergeable=true e draft=false for justificado.
10. Merge somente com expected head SHA.

## Tools MCP permitidas
hermes.health, hermes.services.status, hermes.qdrant.search_staging, hermes.postgres.status, hermes.postgres.query_readonly somente SELECT, hermes.fs.read_doc, hermes.redis.status, hermes.skills.list.

## Comandos proibidos
git push; git clone; reinstalar Hermes Agent; alterar provider/model/API; copiar DSN/secret; abrir portas; mexer em PC1 runtime; SQL diferente de SELECT; Qdrant production; ler/copiar env master; mascarar SKIP como PASS.

## Saída esperada
- Estado observado com fonte: MCP, arquivo local, git ou teste.
- Riscos e bloqueios explícitos.
- Próximo passo seguro.
- Secrets sempre como `[REDACTED]`.

## Critérios de sucesso
Sem secrets, contagens consistentes, CI/testes claros, rollback documentado, expected head SHA preservado.

## Rollback se aplicável
Não aplicável; se arquivo local/config PC2 for alterado, restaurar backup explicitado no relatório.
