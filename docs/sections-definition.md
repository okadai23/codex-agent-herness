# 標準セクション定義

| Section | 目的 | 対象ファイル | 検証コマンド |
|---|---|---|---|
| base-toolchain | 開発基盤 | package manager / CI / scripts | pnpm verify:fast, uv run pytest |
| agent-harness-core | Agent安全制御 | AGENTS, .codex, .agents | apm compile --validate |
| ts-fullstack | TSフルスタック | apps/web, apps/api | pnpm verify:fast |
| api-contract-openapi | API契約 | packages/api-contract | pnpm api:lint, pnpm api:generate |
| frontend-e2e-monkey | E2E探索 | tests/e2e, tests/monkey | pnpm e2e:mock, pnpm monkey |
| docs-maintenance | docs保守 | docs/** | pnpm docs:verify |
| db-lifecycle | DB運用 | packages/db | pnpm db:verify |
| python-ai-core | Python基盤 | services/ai, pyproject.toml | uv run ruff check ., uv run pytest |
| ai-evals | AI評価 | evals/** | uv run python scripts/run_evals.py --suite pr |
| ai-safety | AI安全 | policies/**, prompts/** | safety eval command |
| cross-repo-contract | 複数repo契約 | product-set.yml | contract sync command |

`standard.yml` schema の例は `docs/standard-yml-example.yaml` を参照。
