# Docs-only runtime registration PRs

Use this reference when the work already happened locally or on an operator node, and the repository should record only the official contract, evidence, rollback and memory seed.

## When to use

- A local runtime/operator library was created outside the repo (for example under `~/.hermes`).
- The repo must document state without copying runtime artifacts, real config, allowlists, credentials, DSNs, logs with secrets, or generated local files.
- The user asks for a docs-only PR and explicitly forbids runtime changes, ready/merge, or moving local files into Git.

## Workflow

1. Run the task-specific preflight first (for homelab/Hermes Core this means `homelab-preflight` and MCP read-only checks).
2. Verify the repo base SHA/branch the user named before branching.
3. Create a purpose-specific docs branch.
4. Create docs that describe:
   - contract and operator posture;
   - evidence paths as paths only, not copied file contents;
   - validation results;
   - non-goals/safety constraints;
   - rollback commands;
   - memory seed/update.
5. Update current-state/next-batches/decision-ledger/TODO files only as needed to reflect reviewed state.
6. Run a staged secret scan on docs/memory before commit. Report only status and finding class; never print secret values.
7. Review `git diff --cached --stat` and `git diff --cached --name-status` before commit.
8. Commit with a docs conventional commit.
9. Push the branch and open a draft PR. Do not mark ready or merge unless the user explicitly asks and the relevant PR gate passes.

## Pitfalls

- Do not copy real runtime configs such as `~/.hermes/config.yaml` into the repo. Document their paths and backup paths instead.
- Do not copy hook allowlists, DSNs, tokens, or shell environment files.
- Do not let a docs-only PR imply a runtime change happened in the repo. Be explicit: runtime artifacts remain local/unversioned.
- If the docs mention secrets as a policy topic, validate that no assignment-like secret value or DSN literal appears in staged files.

## Minimal validation snippet

```bash
git diff --cached --name-only
python3 - <<'PY'
from pathlib import Path
import re, subprocess, sys
patterns = [
    ('postgres_dsn', re.compile(r'postgres(?:ql)?://[^\s`"\']+', re.I)),
    ('openai_sk', re.compile(r'\bsk-[A-Za-z0-9][A-Za-z0-9_-]{16,}\b')),
    ('private_key', re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----')),
    ('assignment_secret_like', re.compile(r'(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s`"\']+')),
]
issues = []
for rel in subprocess.check_output(['git','diff','--cached','--name-only'], text=True).splitlines():
    p = Path(rel)
    if not p.exists() or not rel.endswith(('.md', '.txt', '.yaml', '.yml')):
        continue
    text = p.read_text(encoding='utf-8', errors='ignore')
    for name, pat in patterns:
        if pat.search(text):
            issues.append((rel, name))
if issues:
    for rel, name in issues:
        print(f'{rel}: {name}')
    sys.exit(1)
print('staged_secret_scan: OK')
PY
```
