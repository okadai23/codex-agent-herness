# プロダクト開発標準 & Agent Harness 仕様書 v1.0

- Status: Draft v1  
- 作成日: 2026-05-16  
- 対象: 少数リポジトリから開始するプロダクト開発標準化。Backstageはv1では対象外。  
- 前提: React frontend、TypeScript backend、Python AI service、Codex/APM/Copierを用いたAgent Harness。

---

## 1. 目的

本仕様は、複数プロダクトに共通適用できる開発標準を定義する。

1. プロダクト開発の技術スタックを統一する。
2. 新規プロダクトを短時間で安全に開始できる雛形を提供する。
3. 既存プロダクトにもセクション単位で段階適用できるようにする。
4. Agent Harnessを標準化し、CodexなどのAIコーディングエージェントが安全かつ一貫した挙動を取れるようにする。
5. Clean Architecture、TDD、E2E、API contract、mock、docs maintenance、DB lifecycle、AI evalsを標準品質ゲートに入れる。
6. TypeScript系プロダクトとPython AI serviceで、必要なSkill/Subagentを切り替えられるようにする。

## 2. 非目的

v1では以下を非目的とする。

- Backstageによるセルフサービスポータル化。
- 全社横断のダッシュボード。
- 複雑なマルチテナント標準管理。
- 本番デプロイ基盤の完全標準化。
- AIモデルプロバイダの単一化。
- すべての既存プロダクトへの一括適用。

Backstageは、`standardctl` とテンプレート運用が安定した後に導入する。

## 3. 基本方針

### 3.1 2つの管理対象を分ける

| 領域 | 管理ツール | 管理対象 |
|---|---|---|
| リポジトリ雛形 / コード標準 | Copier | ディレクトリ構成、package.json、pyproject.toml、CI、scripts、docs、OpenAPI、DB、tests |
| Agent Harness | APM | instructions、skills、subagents、prompts、hooks、MCP宣言、AGENTS.md生成 |

APMはAI agent設定を `apm.yml` で宣言し、`apm.lock.yaml` で再現性を確保する。Copierは `copier.yml` と `.copier-answers.yml` により、プロジェクト生成と後続更新を扱う。

### 3.2 セクション単位で部分適用する

標準は一括導入しない。`standard.yml` に適用済みセクションを記録し、必要に応じて1セクションずつPR化する。

### 3.3 Stack-aware Agent Harness

TypeScript fullstack、Python AI service、hybrid repositoryでは必要なSkill/Subagentが異なる。APM packageはstackごとに分割し、各repoは必要なAPM packageのみを依存に持つ。

### 3.4 Safety by default

AI agentの自由度は、以下の多層防御で制限する。

- sandbox
- filesystem deny
- network deny
- prohibited command rules
- secret scanning hooks
- APM policy/audit
- generated file edit prevention
- CI verification

### 3.5 Generated outputは直接編集しない

以下は生成物として扱い、原則直接編集しない。

- `apm.lock.yaml`
- `AGENTS.md`
- `.agents/skills/**`
- `.codex/agents/**`
- `.codex/hooks.json`
- `packages/api-client/src/generated/**`
- `packages/api-mocks/src/generated/**`
- OpenAPIから生成される型・client・mock
- `.copier-answers.yml`

## 4. 標準リポジトリ

v1では以下の2〜3リポジトリで開始する。

```txt
org/product-standard-template
  Copier template。
  React + TypeScript backend + Python AI service のrepo雛形を管理する。

org/product-agent-harness
  APM packages。
  Agent instructions / skills / subagents / hooks / MCP / prompts を管理する。

org/product-standard-docs
  任意。
  標準仕様、導入ガイド、更新手順、運用ルールを管理する。
  小規模開始時は product-standard-template/docs/ に統合してよい。
```

推奨開始構成:

```txt
org/
  product-standard-template/
  product-agent-harness/
```

## 5. プロダクトrepoの標準ファイル

各プロダクトrepoには以下を置く。

```txt
apm.yml
apm.lock.yaml
standard.yml
.copier-answers.yml
AGENTS.md
.codex/
.agents/
scripts/
docs/
.github/workflows/
```

### 5.1 `standard.yml`

`standard.yml` は標準適用状態を記録する。

```yaml
standard:
  name: org-product-standard
  version: 1.0.0

template:
  source: github.com/org/product-standard-template
  version: v1.0.0
  profile: hybrid-product

agentHarness:
  apmPackages:
    - name: org/product-agent-harness-core
      version: v1.0.0
    - name: org/product-agent-harness-ts-fullstack
      version: v1.0.0
    - name: org/product-agent-harness-python-ai
      version: v1.0.0

sections:
  base-toolchain:
    status: applied
    version: v1.0.0

  agent-harness-core:
    status: applied
    version: v1.0.0

  ts-fullstack:
    status: applied
    version: v1.0.0

  api-contract-openapi:
    status: applied
    version: v1.0.0

  frontend-e2e-monkey:
    status: partial
    version: v1.0.0

  docs-maintenance:
    status: applied
    version: v1.0.0

  db-lifecycle:
    status: applied
    version: v1.0.0

  python-ai-core:
    status: applied
    version: v1.0.0

  ai-evals:
    status: planned
    version: null

  ai-safety:
    status: planned
    version: null
```

### 5.2 `apm.yml`

TypeScript fullstack repo例:

```yaml
name: product-a-web-api
version: 1.0.0

dependencies:
  apm:
    - org/product-agent-harness-core#v1.0.0
    - org/product-agent-harness-docs#v1.0.0
    - org/product-agent-harness-template-adoption#v1.0.0
    - org/product-agent-harness-ts-fullstack#v1.0.0
    - org/product-agent-harness-api-contract#v1.0.0
    - org/product-agent-harness-frontend-e2e#v1.0.0
    - org/product-agent-harness-db#v1.0.0
```

Python AI service repo例:

```yaml
name: product-a-ai-service
version: 1.0.0

dependencies:
  apm:
    - org/product-agent-harness-core#v1.0.0
    - org/product-agent-harness-docs#v1.0.0
    - org/product-agent-harness-template-adoption#v1.0.0
    - org/product-agent-harness-python-core#v1.0.0
    - org/product-agent-harness-python-ai#v1.0.0
    - org/product-agent-harness-ai-evals#v1.0.0
    - org/product-agent-harness-ai-safety#v1.0.0
```

Hybrid repo例:

```yaml
name: product-a
version: 1.0.0

dependencies:
  apm:
    - org/product-agent-harness-core#v1.0.0
    - org/product-agent-harness-docs#v1.0.0
    - org/product-agent-harness-template-adoption#v1.0.0
    - org/product-agent-harness-ts-fullstack#v1.0.0
    - org/product-agent-harness-api-contract#v1.0.0
    - org/product-agent-harness-frontend-e2e#v1.0.0
    - org/product-agent-harness-db#v1.0.0
    - org/product-agent-harness-python-core#v1.0.0
    - org/product-agent-harness-python-ai#v1.0.0
    - org/product-agent-harness-ai-evals#v1.0.0
    - org/product-agent-harness-ai-safety#v1.0.0
```

## 6. 標準セクション

| Section | 概要 | 主な成果物 |
|---|---|---|
| `base-toolchain` | 基本ツールチェーン | pnpm、uv、CI、verify scripts、standardctl |
| `agent-harness-core` | Agent安全制御 | AGENTS、Codex config、hooks、rules、secret防止 |
| `ts-fullstack` | React + TypeScript backend | apps/web、apps/api、Clean Architecture、Vitest |
| `api-contract-openapi` | API契約 | OpenAPI、Orval、MSW、Prism、Playwright API tests |
| `frontend-e2e-monkey` | UI/E2E/探索 | Playwright E2E、monkey tests、repair requests |
| `docs-maintenance` | Docs as Code | docs/_meta、doc-index、docs verify、changelog |
| `db-lifecycle` | DB migration/seed | migrations、seed catalog、test DB reset、scenario fixtures |
| `python-ai-core` | Python AI service基盤 | uv、pyproject、FastAPI、pytest、Ruff |
| `ai-evals` | AI評価 | golden evals、regression evals、eval reports |
| `ai-safety` | AI安全性 | prompt injection tests、PII rules、safety policy |
| `cross-repo-contract` | 分離repo間契約 | product-set.yml、contract sync、consumer tests |

## 7. Copier template仕様

### 7.1 Template repo構成

```txt
product-standard-template/
  copier.yml
  CHANGELOG.md
  README.md

  docs/
    adoption-guide.md
    update-guide.md
    sections/
      base-toolchain.md
      agent-harness-core.md
      ts-fullstack.md
      api-contract-openapi.md
      frontend-e2e-monkey.md
      docs-maintenance.md
      db-lifecycle.md
      python-ai-core.md
      ai-evals.md
      ai-safety.md

  template/
    standard.yml.jinja
    apm.yml.jinja
    package.json.jinja
    pnpm-workspace.yaml.jinja
    pyproject.toml.jinja
    .python-version.jinja

    AGENTS.md.jinja
    .codex/
      config.toml.jinja
      rules/
        default.rules.jinja

    apps/
      web/
      api/

    services/
      ai/

    packages/
      api-contract/
      api-client/
      api-mocks/
      db/
      test-harness/

    tests/
      api/
      e2e/
      monkey/

    scripts/
      verify.sh
      verify-fast.sh
      standard/
        doctor.mjs
        drift.mjs
        apply-section.mjs
      docs/
      api/
      db/
      ai/

    docs/
      _meta/
        doc-index.yaml.jinja
      harness/
      architecture/
      api/
      db/
      ai/

    .github/
      workflows/
        quality.yml.jinja
        apm-audit.yml.jinja
        docs.yml.jinja
        ai-quality.yml.jinja
```

### 7.2 `copier.yml` profile

```yaml
_min_copier_version: "9.0.0"
_subdirectory: template

project_name:
  type: str
  help: Product or service name

profile:
  type: str
  default: ts-fullstack
  choices:
    - ts-fullstack
    - python-ai-service
    - hybrid-product

frontend:
  type: bool
  default: true

backend:
  type: bool
  default: true

python_ai_service:
  type: bool
  default: false

package_manager:
  type: str
  default: pnpm
  choices:
    - pnpm

python_package_manager:
  type: str
  default: uv
  choices:
    - uv

db:
  type: str
  default: postgres
  choices:
    - none
    - postgres

orm:
  type: str
  default: prisma
  choices:
    - none
    - prisma
    - drizzle

sections:
  type: yaml
  default:
    base-toolchain: true
    agent-harness-core: true
    docs-maintenance: true
    ts-fullstack: true
    api-contract-openapi: true
    frontend-e2e-monkey: true
    db-lifecycle: true
    python-ai-core: false
    ai-evals: false
    ai-safety: false

_tasks:
  - "apm install"
  - "apm compile --validate"
```

### 7.3 生成profile

#### `ts-fullstack`

```txt
apps/web
apps/api
packages/api-contract
packages/api-client
packages/api-mocks
packages/db
packages/test-harness
tests/api
tests/e2e
tests/monkey
pnpm-workspace.yaml
package.json
```

#### `python-ai-service`

```txt
services/ai or src/<package>
pyproject.toml
uv.lock
tests/
evals/
prompts/
policies/
contracts/openapi.yaml
scripts/ai/
docs/ai/
```

#### `hybrid-product`

```txt
ts-fullstack + python-ai-service
product-set.yml
cross-service contract scripts
```

## 8. APM package仕様

### 8.1 APM package一覧

```txt
org/product-agent-harness-core
org/product-agent-harness-docs
org/product-agent-harness-template-adoption

org/product-agent-harness-ts-fullstack
org/product-agent-harness-api-contract
org/product-agent-harness-frontend-e2e
org/product-agent-harness-db

org/product-agent-harness-python-core
org/product-agent-harness-python-ai
org/product-agent-harness-ai-evals
org/product-agent-harness-ai-safety

org/product-agent-harness-cross-repo-contract
```

### 8.2 `product-agent-harness` repo構成

```txt
product-agent-harness/
  README.md
  CHANGELOG.md

  packages/
    core/
      apm.yml
      .apm/
        instructions/
        skills/
        agents/
        prompts/
        hooks/

    docs/
      apm.yml
      .apm/

    template-adoption/
      apm.yml
      .apm/

    ts-fullstack/
      apm.yml
      .apm/

    api-contract/
      apm.yml
      .apm/

    frontend-e2e/
      apm.yml
      .apm/

    db/
      apm.yml
      .apm/

    python-core/
      apm.yml
      .apm/

    python-ai/
      apm.yml
      .apm/

    ai-evals/
      apm.yml
      .apm/

    ai-safety/
      apm.yml
      .apm/
```

### 8.3 Core APM package

```txt
skills:
  - harness-evolution
  - product-standard-adoption
  - standard-section-applier
  - standard-template-update
  - notion-mcp-read
  - notion-mcp-write
  - github-mcp-read

subagents:
  - harness_safety_reviewer
  - standard_adoption_planner
  - template_drift_reviewer
  - apm_policy_reviewer

instructions:
  - secret-handling
  - forbidden-commands
  - generated-files
  - docs-as-deliverable
```

### 8.4 TypeScript APM packages

```txt
ts-fullstack skills:
  - clean-tdd-prototype

api-contract skills:
  - api-contract-lifecycle

frontend-e2e skills:
  - frontend-monkey-repair

db skills:
  - db-lifecycle-maintenance

subagents:
  - architecture_reviewer
  - api_spec_reviewer
  - api_contract_tester
  - e2e_reviewer
  - frontend_monkey_tester
  - db_maintainer
```

### 8.5 Python AI APM packages

```txt
python-core skills:
  - python-service-tdd
  - python-package-maintenance
  - python-api-contract-lifecycle

python-ai skills:
  - ai-feature-lifecycle
  - prompt-lifecycle
  - model-integration-testing
  - ai-observability-maintenance

ai-evals skills:
  - ai-eval-maintenance
  - golden-dataset-maintenance
  - eval-failure-triage

ai-safety skills:
  - ai-safety-review
  - prompt-injection-review
  - pii-data-review

subagents:
  - python_architecture_reviewer
  - python_dependency_reviewer
  - python_test_reviewer
  - ai_eval_reviewer
  - eval_dataset_reviewer
  - prompt_security_reviewer
  - data_privacy_reviewer
  - model_cost_latency_reviewer
  - safety_policy_reviewer
```

## 9. Agent Harness安全仕様

### 9.1 Codex config

`.codex/config.toml` はCopier管理とする。

必須要件:

```toml
sandbox_mode = "workspace-write"
approval_policy = "untrusted"

[features]
codex_hooks = true
multi_agent = true

[sandbox_workspace_write]
network_access = false
exclude_slash_tmp = true
exclude_tmpdir_env_var = true

[shell_environment_policy]
inherit = "core"
exclude = [
  "*KEY*",
  "*SECRET*",
  "*TOKEN*",
  "*PASSWORD*",
  "AWS_*",
  "GITHUB_TOKEN",
  "OPENAI_API_KEY",
  "DATABASE_URL"
]
```

### 9.2 禁止コマンド

`.codex/rules/default.rules` に最低限以下を禁止または承認制にする。

```txt
forbidden:
  - sudo
  - rm -rf
  - chmod -R 777
  - chown -R
  - git push --force
  - npm publish
  - pnpm publish
  - curl ... | sh
  - wget ... | sh
  - cloud CLI direct access

prompt:
  - curl
  - wget
  - external network tools
  - package install outside standard flow
```

### 9.3 Hooks

必須hooks:

```txt
UserPromptSubmit:
  - prompt_secret_scan.py

PreToolUse:
  - pre_tool_use_policy.py

PermissionRequest:
  - pre_tool_use_policy.py

Stop:
  - stop_quality_gate.py
```

### 9.4 APM audit

CIでは必ず以下を実行する。

```bash
apm install --frozen
apm audit --ci --policy org
apm compile --validate
```

## 10. TypeScript fullstack標準

### 10.1 Frontend

```txt
React
TypeScript
Vite
Vitest
Playwright
MSW
generated API client
```

### 10.2 Backend

```txt
TypeScript
Clean Architecture
domain/application/adapters/infrastructure
Vitest
Playwright API tests
OpenAPI contract
Prisma or Drizzle
```

### 10.3 API contract

```txt
packages/api-contract/openapi.yaml
packages/api-client/src/generated
packages/api-mocks/src/generated
orval.config.ts
prism mock server
Playwright API tests
optional Schemathesis
```

### 10.4 Verification

```bash
pnpm verify:fast
pnpm api:verify
pnpm e2e:mock
pnpm e2e:real
pnpm docs:verify
```

## 11. Python AI service標準

### 11.1 Stack

```txt
Python
uv
FastAPI
pytest
Ruff
optional Pydantic
optional OpenAI/Anthropic/provider adapters
optional vector store adapters
```

### 11.2 構成

```txt
services/ai/
  pyproject.toml
  uv.lock
  src/
    <package>/
      domain/
      application/
      adapters/
        inbound/http/
        outbound/llm/
        outbound/vector_store/
      infrastructure/
      main.py

  tests/
    unit/
    integration/
    api/

  evals/
    datasets/
      golden/
      redteam/
    reports/
    runners/

  prompts/
  policies/
  contracts/openapi.yaml
  scripts/
  docs/ai/
```

### 11.3 AI feature原則

- PR-blocking testでは本物のmodel APIを呼ばない。
- LLM providerはport/interface越しに呼ぶ。
- unit testではfake providerを使う。
- evalはPR suiteとnightly suiteに分ける。
- promptはversioned artifactとして `prompts/` に置く。
- eval datasetに本物のPIIや顧客データを入れない。
- red-team / prompt injection caseを安全性ゲートに含める。

### 11.4 Verification

```bash
uv sync --frozen
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/run_evals.py --suite pr
```

## 12. DB lifecycle標準

### 12.1 目的

- migrationをレビュー可能にする。
- seedを決定的かつ安全にする。
- E2E/monkeyの再現性を高める。
- destructive migrationを検出する。

### 12.2 構成

```txt
packages/db/
  prisma/ or drizzle/
  migrations/
  seeds/
    base.seed.ts
    e2e.seed.ts
    monkey.seed.ts
    scenarios/
  factories/
  scripts/
    reset-test-db.ts
    verify-db.ts
```

### 12.3 Seed scenario

必須scenario:

```txt
base
empty
admin
waitlist-success
waitlist-duplicate
pagination
permissions
monkey
```

### 12.4 Migration safety

以下を含むmigrationはrisk noteを必須にする。

```txt
DROP TABLE
DROP COLUMN
type narrowing
NOT NULL without default/backfill
unique constraint on existing data
foreign key constraint on existing data
```

## 13. Docs maintenance標準

### 13.1 Docs structure

```txt
docs/
  README.md
  architecture/
  api/
  db/
  ai/
  operations/
  testing/
  harness/
  releases/
  _meta/
    doc-index.yaml
    public-env-vars.yaml
    generated-sections.yaml
```

### 13.2 doc-index

`docs/_meta/doc-index.yaml` は、コード変更と更新すべきdocsの対応表である。

```yaml
documents:
  - path: docs/api/overview.md
    type: curated
    update_when:
      - packages/api-contract/**
      - apps/api/src/adapters/inbound/http/**
    checks:
      - markdownlint
      - links

  - path: docs/ai/evals.md
    type: curated
    update_when:
      - evals/**
      - prompts/**
      - services/ai/src/**
    checks:
      - markdownlint
      - links
      - snippets
```

### 13.3 Verification

```bash
pnpm docs:impact
pnpm docs:generate
pnpm docs:lint
pnpm docs:links
pnpm docs:snippets
pnpm docs:secrets
pnpm docs:stale
```

## 14. Repair request標準

探索テスト、API contract mismatch、AI eval failureなどで即修復できない問題はrepair requestとして残す。

```txt
packages/test-harness/repair-requests/
evals/repair-requests/
docs/harness/repair-requests/
```

Template:

```md
# Repair Request: <title>

## Type

ui_bug | api_spec_mismatch | mock_mismatch | db_seed_gap | ai_eval_failure | harness_gap

## Severity

low | medium | high

## Reproduction

Command:

```bash
...
```

## Evidence

- Trace:
- Screenshot:
- Eval report:
- Logs:

## Expected behavior

## Actual behavior

## Suspected root cause

## Suggested repair

## Suggested skill
```

## 15. `standardctl`仕様

Backstageなしのv1では、エンジニア向けCLIとして `standardctl` を使う。

### 15.1 コマンド

```bash
standardctl init --profile ts-fullstack
standardctl init --profile python-ai-service
standardctl init --profile hybrid-product

standardctl doctor
standardctl drift

standardctl apply --section api-contract-openapi
standardctl apply --section python-ai-core
standardctl apply --section ai-evals

standardctl update-template
standardctl update-harness
standardctl explain
```

### 15.2 責務

`standardctl` は独自ロジックを肥大化させず、既存ツールのラッパーとする。

```txt
standardctl init
  -> copier copy
  -> apm install
  -> apm compile --validate
  -> verify

standardctl apply
  -> copier update --defaults --data sections.<name>=true
  -> apm install <package>
  -> apm install
  -> apm compile --validate
  -> section verification
  -> standard.yml update

standardctl update-template
  -> copier check-update
  -> copier update --defaults

standardctl update-harness
  -> apm outdated
  -> apm update
  -> apm audit --ci
```

## 16. 標準ワークフロー

### 16.1 新規TypeScript product

```bash
standardctl init --profile ts-fullstack
pnpm install
apm install
apm compile --validate
pnpm verify:fast
pnpm api:verify
pnpm docs:verify
```

### 16.2 新規Python AI service

```bash
standardctl init --profile python-ai-service
uv sync
apm install
apm compile --validate
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/run_evals.py --suite pr
```

### 16.3 既存repoへのsection適用

```bash
git checkout -b platform/apply-api-contract-openapi
standardctl apply --section api-contract-openapi
git status
```

1 PR = 1 sectionを原則とする。

### 16.4 標準更新

```bash
git checkout -b platform/update-standard
standardctl update-template
standardctl update-harness
standardctl doctor
```

## 17. Cross-repo contract

Python AI serviceとTypeScript backendを分離repoにする場合は、`product-set.yml` を使う。

```yaml
product:
  id: product-a
  owner: team-a

repos:
  web_api:
    url: github.com/org/product-a-web-api
    standardProfile: ts-fullstack

  ai_service:
    url: github.com/org/product-a-ai-service
    standardProfile: python-ai-service

contracts:
  ai_service_api:
    provider:
      repo: ai_service
      path: contracts/openapi.yaml
    consumer:
      repo: web_api
      path: packages/ai-service-contract/openapi.yaml
```

標準Skill:

```txt
cross-repo-contract-sync
```

責務:

- provider OpenAPIとconsumer copyのdrift検出
- client再生成
- consumer integration test実行
- repair request生成

## 18. Verification matrix

| 対象 | コマンド |
|---|---|
| APM | `apm install --frozen`, `apm audit --ci --policy org`, `apm compile --validate` |
| Copier | `copier check-update`, `standardctl drift` |
| TypeScript | `pnpm lint`, `pnpm typecheck`, `pnpm test:unit`, `pnpm verify:fast` |
| API | `pnpm api:lint`, `pnpm api:generate`, `pnpm api:test` |
| Frontend | `pnpm e2e:mock`, `pnpm e2e:real`, `pnpm monkey` |
| Docs | `pnpm docs:verify` |
| DB | `pnpm db:verify`, `pnpm db:seed:e2e` |
| Python | `uv sync --frozen`, `uv run ruff check .`, `uv run pytest` |
| AI | `uv run python scripts/run_evals.py --suite pr` |

## 19. CI標準

### 19.1 Common

```yaml
name: quality

on:
  pull_request:
  push:
    branches: [main]

jobs:
  ap
```



## 13. Codex前提リポジトリをClaude Codeでも利用するための変更方針

### 13.1 方針

- **Agent依存物を抽象化**し、`Codex専用` と `Claude共通` を分離する。
- 生成物（`AGENTS.md` / `.codex/**` / `.agents/**`）は「単一ツール依存の固定資産」ではなく、**agent profileごとに再生成**できる状態にする。
- リポジトリ運用は `standard.yml` で「どのAgent profileを適用済みか」を追跡する。

### 13.2 追加する標準セクション

`standard.yml` の sections に次を追加する。

- `agent-harness-claude-core`
- `agent-harness-shared`

`agent-harness-shared` は以下を格納する。

- 言語別 verify コマンド（`pnpm verify:fast` / `uv run pytest` など）
- generated file edit 禁止ルール
- secret / PII / destructive command の共通安全ルール
- docs 影響判定と更新手順

`agent-harness-claude-core` は以下を格納する。

- Claude Code 向けの system / project instructions
- Claude 側での subagent 相当運用（必要時）
- Claude 用の tool/use policy（許可・禁止コマンド）

### 13.3 テンプレート変更（Copier）

`copier.yml` に `agent_runtime` 変数を追加し、最低でも以下を選択可能にする。

- `codex`
- `claude`
- `dual`（両対応）

`template/` では以下を実装する。

1. `agent_runtime=codex` の場合のみ `.codex/**` を生成。
2. `agent_runtime=claude` の場合のみ Claude 用設定ファイル群を生成。
3. `dual` の場合は両方生成し、READMEに「優先する実行ランタイム」と「生成物の責務」を記載。

### 13.4 Harnessパッケージ変更（APM）

現行 `product-agent-harness-core` を以下に分割する。

- `product-agent-harness-shared-core`
- `product-agent-harness-codex-core`
- `product-agent-harness-claude-core`

既存スキルは次の原則で再配置する。

- Codex固有API/記法に依存しないもの → `shared-core`
- Codex専用（`.codex/**` 前提） → `codex-core`
- Claude専用（Claude Codeの実行制約前提） → `claude-core`

### 13.5 ドキュメント変更

最低限以下を追加する。

- `docs/agent-runtimes/codex.md`
- `docs/agent-runtimes/claude.md`
- `docs/agent-runtimes/dual-runtime-policy.md`

`dual-runtime-policy` には次を明記する。

- どのファイルが共通管理か
- どのファイルがCodex専用/Claude専用か
- 両方が同一PRで編集された場合のレビュー観点

### 13.6 CI / 検証コマンド変更

CIを runtime matrix 化し、少なくとも次を実行する。

- `standardctl doctor --runtime codex`
- `standardctl doctor --runtime claude`
- `standardctl drift --runtime codex`
- `standardctl drift --runtime claude`

`standardctl` には `--runtime` オプションを追加し、存在チェック対象を切り替える。

### 13.7 移行手順（既存Codex前提repo）

1. `standard.yml` に `agent-harness-shared` と `agent-harness-claude-core` を `planned` で追加。  
2. `standardctl apply --section agent-harness-shared` を適用。  
3. `standardctl apply --section agent-harness-claude-core` を適用。  
4. CI matrix に `runtime=claude` を追加。  
5. dual runtimeで1〜2スプリント運用し、不要なCodex専用依存を削減。  

### 13.8 受け入れ条件（Claude対応完了の定義）

- Claude runtimeで、必須 verify（lint/test/docs）が実行可能。
- Codex runtimeとClaude runtimeで、共通生成物の差分ポリシーが衝突しない。
- `standardctl doctor/drift` が両runtimeで成功する。
- リポジトリREADMEに Claude 実行手順が明記されている。

---

## 23. v1.0追補（2026-05-17）: 本リポジトリ実装との整合メモ

本追補は、v1.0本文（第1〜22章）を置き換えるものではなく、**このリポジトリの現実装に対する差分管理メモ**である。

### 23.1 位置づけ

- 仕様本文は第1〜22章を正とする。
- 第13章「Codex前提リポジトリをClaude Codeでも利用するための変更方針」は、**v1.1候補の拡張方針**として扱う。
- v1.0の必須要件と、v1.1候補（runtime二重対応）は区別して運用する。

### 23.2 v1.0時点で実装済み（このrepo）

- `copier.yml` に `agent_runtime`（`codex` / `claude` / `dual`）が存在する。
- `template/standard.yml` に `agentRuntime` および `agent-harness-shared` / `agent-harness-claude-core` セクションが存在する。
- `scripts/standard/standardctl.py` に `doctor --runtime` / `drift --runtime` が存在する。

### 23.3 未完了（v1.1候補として継続管理）

以下は第13章要件に対して未完了のため、`tasks.md` 側で継続タスク化する。

- `agent_runtime` に連動した runtime別生成物（`.codex/**` と Claude設定群）のテンプレート分岐実装。
- `docs/agent-runtimes/codex.md` / `claude.md` / `dual-runtime-policy.md` の追加。
- CIのruntime matrix化（`standardctl doctor/drift --runtime codex|claude`）。
- APM package分割（`shared-core` / `codex-core` / `claude-core`）。

### 23.4 運用ルール（暫定）

- 当面、`agent_runtime` は `standard.yml` 記録用途と `standardctl` 検証用途を主目的とする。
- runtime別生成物が揃うまでは、テンプレート利用側READMEに「未実装項目」を明示する。
- v1.1化時に第13章内容を独立章として再採番し、CI受け入れ条件と合わせて昇格させる。
