---
name: mcp-core-usage
description: "Guia de uso seguro e correto dos tools MCP do homelab_core. #usa-mcp"
category: mcp
platforms: [linux]
---

> **ATENÇÃO (2026-06-01):** Antes de usar esta skill, confirme que o pacote Python `mcp` está instalado no venv do Hermes M3. Sintoma de falta: painel mostra "MCP server (stdio) — failed" e `hermes mcp test X` retorna `requires the 'mcp' Python SDK, but it is not installed`. Fix: `uv pip install --python /home/will/.hermes/hermes-agent-next/.venv/bin/python mcp`. Veja skill `mcp-server-debug-playbook` para fluxo completo de diagnóstico.

# Uso seguro do MCP homelab_core

## Quando usar
Sempre que consultar Hermes Core via MCP.

## Objetivo
Usar MCP homelab_core como ferramenta oficial read-only, sem contornar por shell quando MCP responde.

## Procedimento
1. Usar ordem padrão: health -> services.status -> fs.read_doc current state -> fs.read_doc next batches -> Qdrant staging se necessário -> postgres.status -> query SELECT se necessário.
2. SQL somente SELECT.
3. Qdrant apenas staging.
4. Redis apenas status.
5. Não imprimir secrets.

## Tools MCP permitidas
hermes.health, hermes.services.status, hermes.qdrant.search_staging, hermes.postgres.status, hermes.postgres.query_readonly somente SELECT, hermes.fs.read_doc, hermes.redis.status, hermes.skills.list.

## Comandos proibidos
git push; git clone; reinstalar Hermes Agent; alterar provider/model/API; copiar DSN/secret; abrir portas; mexer em PC1 runtime; SQL diferente de SELECT; Qdrant production; ler/copiar env master; mascarar SKIP como PASS.

## Saída esperada
- Estado observado com fonte: MCP, arquivo local, git ou teste.
- Riscos e bloqueios explícitos.
- Próximo passo seguro.
- Secrets sempre como `[REDACTED]`.

## Qdrant staging: embedding endpoint dependency (2026-05-27)

`hermes.qdrant.search_staging` calls embedding via `{EMBEDDING_URL}/v1/embeddings` internally.
EMBEDDING_URL is hardcoded at line 71 of `hermes_mcp_server.py` on PC1 as `http://127.0.0.1:8002`.

If the PC1 nomic-embed service (embedding-local.service) was moved to PC2 GPU, the MCP server
will return `{"ok": false, "error": "embedding generation failed — is embedding-local active?"}`.

**Fix when embedding migrates to PC2:**
```bash
ssh pc1 "sed -i 's|EMBEDDING_URL = \"http://127.0.0.1:8002\"|EMBEDDING_URL = \"http://100.87.53.54:8012\"|' /srv/apps/homelab-context/runtime/mcp/hermes_mcp_server.py"
# Then restart the MCP server (it runs as python -m runtime.mcp.hermes_mcp_server, multiple PIDs)
ssh pc1 "kill \$(pgrep -f 'runtime.mcp.hermes_mcp_server') && sleep 1 && cd /srv/apps/homelab-context && nohup .venv/bin/python -m runtime.mcp.hermes_mcp_server &>/tmp/mcp-server.log &"
```

**Verify:**
```bash
ssh pc1 "curl -s -m 3 http://100.87.53.54:8012/v1/embeddings -X POST -H 'Content-Type: application/json' -d '{\"input\":\"test\",\"model\":\"hermes-embedding-pc2\"}' | python3 -c 'import sys,json; d=json.load(sys.stdin); print(\"dim:\", len(d.get(\"data\",[{}])[0].get(\"embedding\",[])))'"
```

## Critérios de sucesso
Consulta feita pela allowlist, sem shell bypass, sem produção Qdrant, sem SQL write.

## Rollback se aplicável
Não aplicável; se arquivo local/config PC2 for alterado, restaurar backup explicitado no relatório.
