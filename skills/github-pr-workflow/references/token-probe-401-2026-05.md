# GitHub Token Probe — 2026-05-23

## O que aconteceu

Usuário pediu para fazer GitOps (branch, commit, push, PR, merge, build).
O `gh auth status` retornou 401, indicando token inválido.

Tentativas:
- `gh pr create` → HTTP 401 (token expirado)
- `gh auth status` confirmando token inválido em `~/.config/gh/hosts.yml`

## Solução aplicada

Adicionado probe de token no github-pr-workflow:

```bash
# Probe token validity BEFORE attempting operations
if [ -n "$GITHUB_TOKEN" ]; then
  curl -sS -o /dev/null -w "%{http_code}" \
    -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/user 2>/dev/null | grep -q "200" || {
    echo "WARN: GitHub token inválido/expirado."
    unset GITHUB_TOKEN
  }
fi
```

## Alternativa quando token expirado

Se o token está inválido e o repo também existe no Gitea local, tentar a rota Gitea.
Se Gitea também não tem repo criado, reportar ao usuário com o link manual:
`https://github.com/zapprosite/homelab-context/pull/new/feature/secretaria-jarvis-identity-update`

## Contexto

- Branch criado e push para GitHub: `feature/secretaria-jarvis-identity-update`
- Commit: `00eafc0` (atualização SOUL.md — identidade Secretaria→Jarvis)
- gh token: armazenado em `~/.config/gh/hosts.yml`, expira ou foi revogado