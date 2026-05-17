# generated-file-edit-policy

- `AGENTS.md` / `.agents/skills/**` / `.codex/agents/**` / `.codex/hooks.json` は生成物として扱い、直接編集しない。
- 変更が必要な場合は source package (`packages/**/.apm/**`) を修正し、`apm compile --validate` で再生成する。
- `apm.lock.yaml` と `.copier-answers.yml` は手編集禁止。
