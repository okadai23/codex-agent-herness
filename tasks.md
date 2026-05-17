# プロダクト開発標準 & Agent Harness 実装タスクリスト v1.0

Status: Draft v1  
作成日: 2026-05-16  
前提: Backstageなし。APM + Copier + standardctlで開始する。  
記法: 各タスクは Goal、Definition of Done、Acceptance Criteria を持つ。

---

## Phase 0: 標準設計と管理repo作成

### T00-01: 管理repoを作成する ✅ DONE

**Goal**  
標準を管理する最小repoセットを作成し、役割を明確にする。

**Scope**

```txt
org/product-standard-template
org/product-agent-harness
```

任意で以下を追加する。

```txt
org/product-standard-docs
org/product-standard-examples
```

**Definition of Done**

- `product-standard-template` repoが作成されている。
- `product-agent-harness` repoが作成されている。
- 各repoにREADME、CODEOWNERS、CHANGELOGがある。
- 各repoの役割がREADMEに明記されている。

**Acceptance Criteria**

- `product-standard-template` のREADMEに「Copier template管理repo」と明記されている。
- `product-agent-harness` のREADMEに「APM packages管理repo」と明記されている。
- 両repoに初期ブランチ保護ルールが設定されている、または設定手順がdocsに記載されている。

---

### T00-02: 標準セクション定義を確定する ✅ DONE

**Goal**  
プロダクト標準をセクション単位で適用できるようにする。

**Definition of Done**

- 標準セクション一覧が文書化されている。
- 各セクションの目的、対象ファイル、検証コマンドが定義されている。
- `standard.yml` のschema案がある。

**Acceptance Criteria**

- 次のセクションが定義されている。
  - `base-toolchain`
  - `agent-harness-core`
  - `ts-fullstack`
  - `api-contract-openapi`
  - `frontend-e2e-monkey`
  - `docs-maintenance`
  - `db-lifecycle`
  - `python-ai-core`
  - `ai-evals`
  - `ai-safety`
  - `cross-repo-contract`
- セクションは1つずつ適用PRを作れる粒度になっている。
- `standard.yml` の例がdocsに掲載されている。

---

### T00-03: ファイル所有権ルールを定義する ✅ DONE

**Goal**  
APM生成物、Copier生成物、product-local編集対象の境界を明確にする。

**Definition of Done**

- ファイル所有権マトリクスが仕様書またはdocsにある。
- 直接編集禁止ファイルが明記されている。
- Agent向けのgenerated file edit禁止ルールが定義されている。

**Acceptance Criteria**

- `AGENTS.md`、`.agents/skills/**`、`.codex/agents/**`、`.codex/hooks.json` はAPM生成物として扱われている。
- `.codex/config.toml`、`.codex/rules/**`、scripts、CIはCopier管理として扱われている。
- `.copier-answers.yml` と `apm.lock.yaml` は手編集禁止として明記されている。

---

## Phase 1: Copier template 実装

### T01-01: Copier templateの基本構成を作成する ✅ DONE

**Goal**  
`product-standard-template` をCopier templateとして利用可能にする。

**Definition of Done**

- `copier.yml` が作成されている。
- `_subdirectory: template` が設定されている。
- `template/` 以下に最低限のファイルがある。
- `copier copy` で新規repoを生成できる。

**Acceptance Criteria**

- `copier copy <template> <dest> --data profile=ts-fullstack` が成功する。
- 生成先に `.copier-answers.yml` が作成される。
- 生成先に `standard.yml` と `apm.yml` が作成される。
- 生成先repoで `git status` が確認できる状態になっている。

---

### T01-02: `ts-fullstack` profileを実装する ✅ DONE

**Goal**  
React frontend + TypeScript backendプロダクトを生成できるようにする。

**Definition of Done**

- `apps/web` が生成される。
- `apps/api` が生成される。
- `packages/api-contract`、`api-client`、`api-mocks` が生成される。
- `packages/db` と `packages/test-harness` が生成される。
- pnpm workspaceが動作する。

**Acceptance Criteria**

- `pnpm install` が成功する。
- `pnpm verify:fast` が成功する。
- `pnpm api:lint` が成功する。
- `pnpm api:generate` が成功する。
- `pnpm docs:verify` が少なくともno-opまたは初期状態で成功する。

---

### T01-03: `python-ai-service` profileを実装する ✅ DONE

**Goal**  
Python AI service用repoを生成できるようにする。

**Definition of Done**

- `pyproject.toml` が生成される。
- `uv.lock` を生成できる構成になっている。
- `src/` または `services/ai/src/` にClean Architecture風の構成がある。
- `tests/`、`evals/`、`prompts/`、`policies/`、`contracts/` が生成される。
- Ruff、pytest、FastAPIの初期設定がある。

**Acceptance Criteria**

- `uv sync` が成功する。
- `uv run ruff check .` が成功する。
- `uv run ruff format --check .` が成功する。
- `uv run pytest` が成功する。
- `uv run python scripts/run_evals.py --suite pr` が成功または初期no-opで成功する。

---

### T01-04: `hybrid-product` profileを実装する ✅ DONE

**Goal**  
TypeScript frontend/backendとPython AI serviceを同一monorepoで管理できるようにする。

**Definition of Done**

- `ts-fullstack` と `python-ai-service` の主要構成が同時生成される。
- TypeScriptとPythonの検証コマンドが共存する。
- `product-set.yml` または同等のcross-service manifestが生成される。
- 共通docsにTS/Python両方の開発手順がある。

**Acceptance Criteria**

- `pnpm verify:fast` が成功する。
- `uv run pytest` が成功する。
- `apm install` が成功する。
- `standard.yml` にTS系とPython AI系のセクションが記録される。

---

### T01-05: Copier update flowを検証する ✅ DONE

**Goal**  
テンプレート更新を生成済みrepoへ再適用できるようにする。

**Definition of Done**

- `copier check-update` の運用手順がdocsにある。
- `copier update --defaults --conflict rej` の運用手順がdocsにある。
- conflict marker検出のCIまたはscriptがある。

**Acceptance Criteria**

- templateをtag `v0.1.0` で生成したrepoに対し、`v0.1.1` への更新を試験できる。
- 更新後に `.rej` またはconflict markerが検出される場合、CIまたはscriptが失敗する。
- `.copier-answers.yml` を手編集しない運用がREADMEに明記されている。

---

## Phase 2: APM Agent Harness 実装

### T02-01: `product-agent-harness-core` packageを実装する

**Goal**  
全repo共通のAgent Harness基盤をAPM packageとして提供する。

**Definition of Done**

- `packages/core/apm.yml` がある。
- `.apm/instructions`、`.apm/skills`、`.apm/agents` がある。
- core packageに以下が含まれている。
  - secret handling instruction
  - generated file edit禁止instruction
  - harness-evolution skill
  - product-standard-adoption skill
  - standard-section-applier skill
  - harness_safety_reviewer subagent
  - standard_adoption_planner subagent

**Acceptance Criteria**

- 生成済みrepoの `apm.yml` にcore packageを追加できる。
- `apm install` が成功する。
- `apm compile --validate` が成功する。
- `AGENTS.md`、`.agents/skills/**`、`.codex/agents/**` が期待通り生成される。

---

### T02-02: `product-agent-harness-docs` packageを実装する

**Goal**  
docs maintenanceをAgent Harnessとして標準化する。

**Definition of Done**

- `doc-maintenance` skillがある。
- `doc_impact_reviewer`、`technical_writer`、`doc_quality_reviewer` subagentがある。
- docs impact、generated section、secret scan、stalenessの指示が含まれている。

**Acceptance Criteria**

- `$doc-maintenance` を明示呼び出しできる。
- docs影響がある変更に対して、更新対象docsを列挙できる。
- generated sectionを手編集しないルールがSkillに含まれている。

---

### T02-03: `product-agent-harness-template-adoption` packageを実装する

**Goal**  
既存repoへの標準適用と標準更新をAgentが支援できるようにする。

**Definition of Done**

- `product-standard-adoption` skillがある。
- `standard-section-applier` skillがある。
- `standard-template-update` skillがある。
- `template_drift_reviewer` subagentがある。
- `apm_policy_reviewer` subagentがある。

**Acceptance Criteria**

- 既存repoに対して適用状況matrixを出力できる。
- 1 sectionのみ適用する手順がSkillに定義されている。
- APM/Copier更新時のdiff review手順がSkillに定義されている。

---

### T02-04: `product-agent-harness-ts-fullstack` packageを実装する

**Goal**  
TypeScript frontend/backend開発のAgent Harnessを提供する。

**Definition of Done**

- `clean-tdd-prototype` skillがある。
- `architecture_reviewer` subagentがある。
- Clean Architecture、TDD、E2E先行、verify実行が明記されている。

**Acceptance Criteria**

- `$clean-tdd-prototype` により受け入れ条件、失敗テスト、最小実装、verifyの手順が提示される。
- domain/application/adapters/infrastructureの境界ルールがSkillに含まれる。
- `architecture_reviewer` がread-onlyで使用できる。

---

### T02-05: `product-agent-harness-api-contract` packageを実装する

**Goal**  
OpenAPI、mock生成、実APIテストをAgent Harness化する。

**Definition of Done**

- `api-contract-lifecycle` skillがある。
- `api_spec_reviewer` subagentがある。
- `api_contract_tester` subagentがある。
- OpenAPI更新、Orval生成、MSW、Prism、Playwright API testの手順がある。

**Acceptance Criteria**

- 新規API要求に対し、OpenAPI更新を先に行う指示になっている。
- generated client/mockを手編集しないルールが含まれている。
- API mismatch時にrepair requestを作る手順がある。

---

### T02-06: `product-agent-harness-frontend-e2e` packageを実装する

**Goal**  
Playwright E2E、monkey test、BrowserUse/Playwright MCP探索をAgent Harness化する。

**Definition of Done**

- `frontend-monkey-repair` skillがある。
- `frontend_monkey_tester` subagentがある。
- seed付きmonkey test、trace/screenshot/log収集、repair request作成手順がある。
- MCP使用時の安全ルールがある。

**Acceptance Criteria**

- monkey test失敗からrepair requestを作れる。
- seed、step count、trace、screenshot、console errorが記録対象として定義されている。
- BrowserUse/Playwright MCPは探索用途でありCI合否判定の唯一の根拠にしないと明記されている。

---

### T02-07: `product-agent-harness-db` packageを実装する

**Goal**  
DB migration、seed、test DB maintenanceをAgent Harness化する。

**Definition of Done**

- `db-lifecycle-maintenance` skillがある。
- `db_maintainer` subagentがある。
- destructive migration checklistがある。
- seed scenario catalogのルールがある。

**Acceptance Criteria**

- `DROP TABLE`、`DROP COLUMN`、type narrowingなどを高リスクとして扱う。
- seedは決定的、冪等、PIIなしで作るルールがある。
- E2E seed scenarioとの連携手順が含まれる。

---

### T02-08: `product-agent-harness-python-core` packageを実装する

**Goal**  
Python serviceのTDD、package、API contract開発をAgent Harness化する。

**Definition of Done**

- `python-service-tdd` skillがある。
- `python-package-maintenance` skillがある。
- `python-api-contract-lifecycle` skillがある。
- `python_architecture_reviewer`、`python_dependency_reviewer`、`python_test_reviewer` subagentがある。

**Acceptance Criteria**

- Python serviceでClean Architecture境界を守る指示がある。
- `uv run pytest`、`uv run ruff check .`、`uv run ruff format --check .` がverifyに含まれる。
- provider SDKやDB clientをdomain/applicationに入れないルールがある。

---

### T02-09: `product-agent-harness-python-ai` packageを実装する

**Goal**  
AI feature、prompt、LLM provider連携をAgent Harness化する。

**Definition of Done**

- `ai-feature-lifecycle` skillがある。
- `prompt-lifecycle` skillがある。
- `model-integration-testing` skillがある。
- `prompt_reviewer`、`llm_integration_reviewer`、`model_cost_latency_reviewer` subagentがある。

**Acceptance Criteria**

- PR-blocking testsではreal model APIを呼ばないルールがある。
- promptをversioned artifactとして扱うルールがある。
- LLM providerはport/interface経由で扱うルールがある。
- cost/latency/retry/fallback観点がreviewに含まれる。

---

### T02-10: `product-agent-harness-ai-evals` packageを実装する

**Goal**  
AI eval dataset、golden tests、regression testをAgent Harness化する。

**Definition of Done**

- `ai-eval-maintenance` skillがある。
- `golden-dataset-maintenance` skillがある。
- `eval-failure-triage` skillがある。
- `ai_eval_reviewer`、`eval_dataset_reviewer`、`regression_triage_agent` subagentがある。

**Acceptance Criteria**

- evalはPR suiteとnightly suiteに分離されている。
- eval datasetにPIIを入れないルールがある。
- eval failureからrepair requestを作る手順がある。

---

### T02-11: `product-agent-harness-ai-safety` packageを実装する

**Goal**  
AI safety、prompt injection、PII対応をAgent Harness化する。

**Definition of Done**

- `ai-safety-review` skillがある。
- `prompt-injection-review` skillがある。
- `pii-data-review` skillがある。
- `prompt_security_reviewer`、`data_privacy_reviewer`、`safety_policy_reviewer` subagentがある。

**Acceptance Criteria**

- user inputを含むpromptにはinjection testを要求する。
- eval dataset、logs、fixturesのPIIチェック手順がある。
- unsafe tool useやdata exfiltration riskのreview観点がある。

---

## Phase 3: standardctl 実装

### T03-01: `standardctl doctor` を実装する ✅ DONE

**Goal**  
repoが標準に準拠しているかを簡単に確認できるようにする。

**Definition of Done**

- `standardctl doctor` コマンドまたは `scripts/standard/doctor.*` がある。
- `standard.yml`、`apm.yml`、`apm.lock.yaml`、`.copier-answers.yml` の有無を確認する。
- profileに応じた必須ファイルを確認する。

**Acceptance Criteria**

- 標準repoで `standardctl doctor` が成功する。
- `apm.lock.yaml` がない場合は失敗する。
- `.copier-answers.yml` がない場合は警告または失敗する。
- profileと実ディレクトリの不一致を検出する。

---

### T03-02: `standardctl drift` を実装する ✅ DONE

**Goal**  
テンプレート、APM harness、生成物のdriftを検出する。

**Definition of Done**

- `copier check-update` を呼び出す。
- `apm outdated` または同等の確認を呼び出す。
- OpenAPI生成物、docs生成物、APM生成物のdriftを確認する。

**Acceptance Criteria**

- template updateがある場合に検出される。
- APM package updateがある場合に検出される。
- generated client/mockがOpenAPIとずれている場合に検出される。
- outputは人間がPRに貼れる形式になっている。

---

### T03-03: `standardctl apply --section` を実装する ✅ DONE

**Goal**  
既存repoに1セクションだけ標準を適用できるようにする。

**Definition of Done**

- `--section` 引数を受け取る。
- 対象sectionに応じてCopier update、APM install、verifyを実行する。
- `standard.yml` を更新する。
- adoption reportを生成する。

**Acceptance Criteria**

- `standardctl apply --section api-contract-openapi` が実行できる。
- 1 section以外の不要なファイル変更が出ない。
- `docs/harness/adoptions/<date>-<section>.md` が生成される。
- verifyに失敗した場合、失敗内容がreportに残る。

---

### T03-04: `standardctl update-template` を実装する ✅ DONE

**Goal**  
Copier template更新を標準化する。

**Definition of Done**

- `copier check-update` を実行する。
- updateがある場合は `copier update --defaults --conflict rej` を実行する。
- conflict検出を行う。
- update reportを出す。

**Acceptance Criteria**

- updateなしの場合はno-opとして成功する。
- updateありの場合は差分が生成される。
- `.rej` またはconflict markerがある場合は失敗する。
- `standard.yml.template.version` が更新される。

---

### T03-05: `standardctl update-harness` を実装する ✅ DONE

**Goal**  
APM Agent Harness更新を標準化する。

**Definition of Done**

- `apm outdated` を実行する。
- `apm update` を実行する。
- `apm audit --ci --policy org` を実行する。
- `apm compile --validate` を実行する。

**Acceptance Criteria**

- APM更新なしの場合はno-opとして成功する。
- APM更新ありの場合は `apm.lock.yaml` が更新される。
- policy違反がある場合は失敗する。
- `standard.yml.agentHarness.apmPackages` が更新される。

---

## Phase 4: TypeScript fullstack標準機能

### T04-01: OpenAPI + Orval + MSW生成を実装する

**Goal**  
API contractから型、client、mockを生成できるようにする。

**Definition of Done**

- `packages/api-contract/openapi.yaml` がある。
- `orval.config.ts` がある。
- generated client/mocksの出力先がある。
- `pnpm api:generate` がある。

**Acceptance Criteria**

- `pnpm api:lint` が成功する。
- `pnpm api:generate` が成功する。
- generated filesに手編集禁止コメントがある。
- frontendからgenerated clientをimportできる。

---

### T04-02: Prism mock serverを実装する

**Goal**  
backend未完成でもOpenAPIからmock APIを使えるようにする。

**Definition of Done**

- `pnpm api:mock` がある。
- Prism mock serverがOpenAPIを読む。
- docsに起動方法がある。

**Acceptance Criteria**

- `pnpm api:mock` でローカルmock serverが起動する。
- frontendのlocal devでmock serverを使える。
- OpenAPI exampleが不十分な場合、lintまたはtestで検出できる。

---

### T04-03: Playwright API testを実装する

**Goal**  
実backendがOpenAPI契約に合っているか検証する。

**Definition of Done**

- `tests/api` がある。
- `pnpm api:test` がある。
- happy pathと主要error pathのtestがある。

**Acceptance Criteria**

- 実backend起動後に `pnpm api:test` が成功する。
- response schema mismatchが検出される。
- API test結果がCIで実行される。

---

### T04-04: Playwright E2E mock/real modeを実装する

**Goal**  
frontend E2Eをmock APIとreal APIの両方で実行できるようにする。

**Definition of Done**

- `pnpm e2e:mock` がある。
- `pnpm e2e:real` がある。
- Playwright configにprojectまたはenv分岐がある。

**Acceptance Criteria**

- mock modeでbackendなしにE2Eが通る。
- real modeでbackend込みE2Eが通る。
- 主要ユーザーフローのhappy pathが最低1本ある。

---

### T04-05: Playwright monkey testを実装する

**Goal**  
UI crash、console error、navigation dead-endを探索できるようにする。

**Definition of Done**

- `tests/monkey` がある。
- seed付きrandom操作がある。
- trace/screenshot/console/network evidenceを保存する。
- `pnpm monkey` がある。

**Acceptance Criteria**

- `MONKEY_SEED=example MONKEY_STEPS=20 pnpm monkey` が実行できる。
- 失敗時にseedとreproduction commandが出力される。
- app root visibility、console errorなし、unexpected 4xx/5xxなしのinvariantがある。

---

## Phase 5: DB lifecycle実装

### T05-01: DB schema/migration基盤を実装する

**Goal**  
PrismaまたはDrizzleでmigrationを標準管理できるようにする。

**Definition of Done**

- ORM選択に応じたschema/migrationディレクトリがある。
- `pnpm db:migrate:dev`、`pnpm db:migrate:deploy` がある。
- migration safety scriptまたはreview checklistがある。

**Acceptance Criteria**

- test DBにmigrationを適用できる。
- migration SQLまたは差分をreviewできる。
- destructive migrationを検出または報告できる。

---

### T05-02: Seed scenario catalogを実装する

**Goal**  
E2E、API test、monkey testで再現可能なseedを使えるようにする。

**Definition of Done**

- `base`、`empty`、`admin`、`pagination`、`permissions`、`monkey` scenarioがある。
- seedは冪等である。
- dummy dataのみを使う。

**Acceptance Criteria**

- `pnpm db:seed:e2e` が成功する。
- `pnpm db:reset:test` が成功する。
- `example.test` domainが使われている。
- seed scenario一覧がdocsにある。

---

### T05-03: E2Eからseed scenarioを利用できるようにする

**Goal**  
E2Eテストが安定した初期状態で実行できるようにする。

**Definition of Done**

- E2E support helperがある。
- testごとにscenarioを指定できる。
- reset対象はtest DBに限定される。

**Acceptance Criteria**

- E2Eテスト内で `seedScenario("waitlist-duplicate")` 相当の呼び出しができる。
- production DB URLではresetが拒否される。
- seed不足がある場合にrepair requestを作れる。

---

## Phase 6: Python AI service標準機能

### T06-01: Python service基盤を実装する

**Goal**  
uv/Ruff/pytest/FastAPIを用いたPython serviceを標準生成できるようにする。

**Definition of Done**

- `pyproject.toml` がある。
- `uv.lock` を生成できる。
- Ruff設定がある。
- pytest設定がある。
- FastAPI app skeletonがある。

**Acceptance Criteria**

- `uv sync` が成功する。
- `uv run ruff check .` が成功する。
- `uv run ruff format --check .` が成功する。
- `uv run pytest` が成功する。
- `/health` または同等のhealth endpointがある。

---

### T06-02: Python Clean Architecture境界を実装する

**Goal**  
Python AI serviceでもdomain/applicationをframework/providerから分離する。

**Definition of Done**

- `domain/`、`application/`、`adapters/`、`infrastructure/` がある。
- LLM provider port/interfaceがある。
- fake providerを使ったunit testがある。

**Acceptance Criteria**

- domain/applicationがFastAPIやprovider SDKに依存しない。
- unit testでreal model APIを呼ばない。
- architecture boundary checkがある、またはreview scriptがある。

---

### T06-03: AI prompt lifecycleを実装する

**Goal**  
promptをversioned artifactとして管理する。

**Definition of Done**

- `prompts/` ディレクトリがある。
- prompt frontmatter schemaがある。
- promptごとにowner、version、input/output schema、safety notesを記録する。
- prompt関連evalがある。

**Acceptance Criteria**

- prompt fileにversionとownerがある。
- user inputを含むpromptにはinjection caseがある。
- prompt変更時にeval実行が要求される。

---

### T06-04: AI eval基盤を実装する

**Goal**  
AI機能のgolden/regression/safety evalを実行できるようにする。

**Definition of Done**

- `evals/datasets/golden` がある。
- `evals/datasets/redteam` がある。
- `scripts/run_evals.py` がある。
- PR suiteとnightly suiteが分かれている。

**Acceptance Criteria**

- `uv run python scripts/run_evals.py --suite pr` が成功する。
- eval reportが `evals/reports/` に生成される。
- eval datasetにPIIがないことを検査できる。
- eval failureからrepair requestを生成できる。

---

### T06-05: AI safety checksを実装する

**Goal**  
prompt injection、PII、unsafe outputの最低限の検査を標準化する。

**Definition of Done**

- `policies/safety-policy.md` がある。
- `policies/pii-policy.md` がある。
- prompt injection testsがある。
- PII scan scriptがある。

**Acceptance Criteria**

- PR suiteに最低限のsafety evalが含まれる。
- PIIらしき文字列がeval datasetにある場合、検査が失敗する。
- unsafe tool useに関するreview checklistがある。

---

## Phase 7: Docs maintenance実装

### T07-01: doc-indexを実装する

**Goal**  
コード変更から更新すべきdocsを検出できるようにする。

**Definition of Done**

- `docs/_meta/doc-index.yaml` がある。
- `scripts/docs/doc-impact.*` がある。
- `pnpm docs:impact` がある。

**Acceptance Criteria**

- API関連ファイル変更時にAPI docsがimpact対象として表示される。
- AI関連ファイル変更時にAI docsがimpact対象として表示される。
- docs影響なしの場合はno-opとして成功する。

---

### T07-02: docs verificationを実装する

**Goal**  
docsのlint、link、snippet、secret、stalenessを検査できるようにする。

**Definition of Done**

- `pnpm docs:verify` がある。
- docs lintがある。
- docs secret scanがある。
- stale checkがある。

**Acceptance Criteria**

- 初期repoで `pnpm docs:verify` が成功する。
- docs内にsecret-like stringがある場合に失敗する。
- stale期限切れdocを検出できる。

---

### T07-03: harness changelog/adoption reportsを実装する

**Goal**  
標準適用とHarness変更履歴を追跡できるようにする。

**Definition of Done**

- `docs/harness/changelog.md` がある。
- `docs/harness/adoptions/` がある。
- `standardctl apply` がadoption reportを生成する。

**Acceptance Criteria**

- section適用時にadoption reportが作成される。
- reportには変更内容、検証コマンド、未解決リスクが含まれる。
- harness変更時にchangelog更新が求められる。

---

## Phase 8: CI / policy / safety

### T08-01: APM audit CIを実装する

**Goal**  
Agent Harness依存と生成物をCIで検査する。

**Definition of Done**

- GitHub ActionsにAPM jobがある。
- `apm install --frozen` が実行される。
- `apm audit --ci --policy org` が実行される。
- `apm compile --validate` が実行される。

**Acceptance Criteria**

- `apm.lock.yaml` がない場合、CIが失敗する。
- policy違反がある場合、CIが失敗する。
- APM生成物driftが検出される。

---

### T08-02: TypeScript quality CIを実装する

**Goal**  
TypeScript fullstackの品質ゲートをCIで実行する。

**Definition of Done**

- `pnpm install --frozen-lockfile` が実行される。
- `pnpm verify:fast` が実行される。
- `pnpm api:verify` が実行される。
- `pnpm docs:verify` が実行される。

**Acceptance Criteria**

- lint/typecheck/unit/API/docsがCIで検査される。
- generated client/mockの未commit差分が検出される。
- CI結果がPR上で確認できる。

---

### T08-03: Python AI quality CIを実装する

**Goal**  
Python AI serviceの品質ゲートをCIで実行する。

**Definition of Done**

- `uv sync --frozen` が実行される。
- `uv run ruff check .` が実行される。
- `uv run ruff format --check .` が実行される。
- `uv run pytest` が実行される。
- `uv run python scripts/run_evals.py --suite pr` が実行される。

**Acceptance Criteria**

- Python lint/format/test/evalがCIで検査される。
- PR suite evalが失敗した場合、CIが失敗する。
- nightly suiteはPR必須ではない。

---

### T08-04: Codex safety hooks/rulesを検証する

**Goal**  
禁止コマンド、secret access、generated file editをAgent Harnessで抑止できるようにする。

**Definition of Done**

- pre_tool_use_policy scriptがある。
- prompt_secret_scan scriptがある。
- stop_quality_gate scriptがある。
- rules self-testがある。

**Acceptance Criteria**

- `.env` 読み取りを試みるコマンドが拒否される。
- `rm -rf` が拒否される。
- `curl ... | sh` が拒否される。
- `pnpm verify:fast` は許可される。
- hook/rule self-testが成功する。

---

## Phase 9: Cross-repo contract

### T09-01: `product-set.yml` を実装する

**Goal**  
TypeScript repoとPython AI service repoの関係を明示する。

**Definition of Done**

- `product-set.yml` schemaがある。
- provider/consumer contractが記録できる。
- docsに記載例がある。

**Acceptance Criteria**

- Python AI serviceをprovider、TS backendをconsumerとして記録できる。
- contract file pathが明示されている。
- ownerとrepo URLが記録されている。

---

### T09-02: `cross-repo-contract-sync` skillを実装する

**Goal**  
provider/consumer間のOpenAPI driftをAgentが検出・修復提案できるようにする。

**Definition of Done**

- `cross-repo-contract-sync` skillがある。
- provider contractとconsumer copyの比較手順がある。
- client再生成とconsumer integration test手順がある。

**Acceptance Criteria**

- driftがある場合に検出できる。
- 修復手順がprovider-first、consumer-secondで定義されている。
- 片方のrepoしか更新できない場合、repair requestを作る。

---

## Phase 10: Example repo / pilot adoption

### T10-01: TypeScript example repoを作成する

**Goal**  
標準の動作確認用にfullstack exampleを作る。

**Definition of Done**

- `product-standard-examples/fullstack-react-ts-postgres` がある。
- Copier templateから生成されている。
- APM harnessが入っている。
- CIが成功している。

**Acceptance Criteria**

- `pnpm verify` が成功する。
- `pnpm api:verify` が成功する。
- `pnpm e2e:mock` が成功する。
- `standardctl doctor` が成功する。

---

### T10-02: Python AI example repoを作成する

**Goal**  
Python AI service標準の動作確認用exampleを作る。

**Definition of Done**

- `product-standard-examples/python-ai-service` がある。
- Copier templateから生成されている。
- APM harnessが入っている。
- PR suite evalがある。

**Acceptance Criteria**

- `uv sync --frozen` が成功する。
- `uv run ruff check .` が成功する。
- `uv run pytest` が成功する。
- `uv run python scripts/run_evals.py --suite pr` が成功する。
- `standardctl doctor` が成功する。

---

### T10-03: Hybrid example repoを作成する

**Goal**  
TypeScript frontend/backend + Python AI serviceの同一monorepo例を検証する。

**Definition of Done**

- `product-standard-examples/hybrid-product` がある。
- TypeScriptとPythonの両方の検証が通る。
- cross-service contractの例がある。

**Acceptance Criteria**

- `pnpm verify:fast` が成功する。
- `uv run pytest` が成功する。
- `pnpm api:verify` が成功する。
- `standardctl doctor` が成功する。

---

### T10-04: 既存repoにpilot適用する

**Goal**  
実プロダクトに標準を小さく適用して運用上の問題を発見する。

**Definition of Done**

- pilot対象repoが選定されている。
- `product-standard-adoption` skillでassessmentが作成されている。
- 最初の1 sectionがPR適用されている。
- feedbackが標準repoに反映されている。

**Acceptance Criteria**

- pilot PRは1 sectionのみ変更している。
- PRにadoption reportが添付されている。
- CIが成功する、または失敗理由と次対応が明記されている。
- pilot結果から少なくとも1つの改善issueが作られている。

---

## Phase 11: 運用文書

### T11-01: エンジニア向けQuick Startを作成する

**Goal**  
エンジニアがBackstageなしで標準を利用できるようにする。

**Definition of Done**

- 新規TypeScript product作成手順がある。
- 新規Python AI service作成手順がある。
- 既存repoへのsection適用手順がある。
- 更新手順がある。

**Acceptance Criteria**

- `standardctl init --profile ts-fullstack` の手順がある。
- `standardctl init --profile python-ai-service` の手順がある。
- `standardctl apply --section ...` の手順がある。
- troubleshootingがある。

---

### T11-02: Agent Harness運用ガイドを作成する

**Goal**  
APM package、Skill、Subagent、MCP、policyの運用ルールを文書化する。

**Definition of Done**

- APM package追加手順がある。
- Skill追加・更新手順がある。
- Subagent追加・更新手順がある。
- MCP追加時の安全審査手順がある。
- APM audit/policy手順がある。

**Acceptance Criteria**

- 「APM生成物を直接編集しない」ルールが記載されている。
- stack別APM packageの使い分けが記載されている。
- MCP tokenをmanifestに直接書かないルールが記載されている。
- policy違反時の対応手順がある。

---

### T11-03: Python AI開発ガイドを作成する

**Goal**  
Python AI serviceの開発・テスト・eval・safety運用を標準化する。

**Definition of Done**

- uv/Ruff/pytestの使い方がある。
- FastAPI service開発手順がある。
- prompt lifecycleがある。
- eval lifecycleがある。
- safety/PIIルールがある。

**Acceptance Criteria**

- real model APIをPR-blocking testで呼ばないルールが記載されている。
- fake providerを使うtest例がある。
- eval datasetのPII禁止が記載されている。
- PR suite/nightly suiteの違いが説明されている。

---

## Phase 12: v1リリース

### T12-01: v1 release checklistを作成する

**Goal**  
v1標準を再現可能にリリースする。

**Definition of Done**

- template repoにtag `v1.0.0` がある。
- agent harness packageにtag `v1.0.0` がある。
- example repoがv1.0.0で生成されている。
- changelogがある。

**Acceptance Criteria**

- `copier copy gh:org/product-standard-template --vcs-ref v1.0.0` が成功する。
- `apm install org/product-agent-harness-core#v1.0.0` が成功する。
- examplesのCIが成功する。
- v1 release notesに導入手順、既知制約、次期課題がある。

---

### T12-02: v1運用開始判定を行う

**Goal**  
実プロダクトで使える最低品質を満たしたか判定する。

**Definition of Done**

- v1仕様書が承認されている。
- 実装タスクの必須項目が完了している。
- pilot repoで少なくとも1 section適用済みである。
- blocking issueが整理されている。

**Acceptance Criteria**

- Product standard ownerがv1開始を承認する。
- エンジニアがQuick Startだけで新規repoを作れる。
- APM auditと標準verifyがCIで動いている。
- 未完了項目はv1.1 backlogに移されている。


## 実装ログ (2026-05-17)
- [DONE] [Phase0] 管理repo骨子・標準セクション定義・所有権ルールを追加
  - README/CODEOWNERS/CHANGELOG と branch protection 手順を追加
  - セクション定義と standard.yml schema 例を docs 化
  - APM生成物/Copier管理/手編集禁止ファイルを明文化
- [DONE] [Phase1] Copier template 基本構成と 3 profile の最小実装を追加
  - `copier.yml` と `template/` の基本ファイルを作成
  - ts/python/hybrid を選べる profile 設定を追加
  - update 手順と conflict 検出スクリプトを追加
- [DONE] [Phase2] APM Agent Harness package 群（core/docs/template-adoption/ts/api/e2e/db/python/ai）を追加
  - `packages/*/apm.yml` と `.apm/instructions|skills|agents` を新規作成し、各タスクで要求された skill / subagent 名を実装
  - core に secret handling と generated file edit 禁止ルールを明文化
  - api-contract / frontend-e2e / db / python / ai-evals / ai-safety で受け入れ条件に対応する実務ルールを追加

- [DONE] [Phase3] standardctl コマンド群を実装
  - `scripts/standard/standardctl.py` に doctor/drift/apply/update-template/update-harness を追加
  - `tests/standard/test_standardctl.py` で doctor と apply の主要ユースケースをテスト
  - adoption report の自動生成先を `docs/harness/adoptions/` に統一
