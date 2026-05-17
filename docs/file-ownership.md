# ファイル所有権ルール

## APM生成物（直接編集禁止）
- `AGENTS.md`
- `.agents/skills/**`
- `.codex/agents/**`
- `.codex/hooks.json`

## Copier管理（テンプレート側で編集）
- `.codex/config.toml`
- `.codex/rules/**`
- `scripts/**`
- `.github/workflows/**`

## 手編集禁止
- `.copier-answers.yml`
- `apm.lock.yaml`

Agent は生成物に対して直接編集を避け、元テンプレートまたは APM package を更新すること。
