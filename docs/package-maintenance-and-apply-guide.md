# APM Package メンテナンス＆適用ガイド

このドキュメントは、`packages/*` にある APM package を**どう保守するか**、および**実際の環境/既存リポジトリへどう適用するか**をまとめた運用ガイドです。

## 1. まず押さえる原則

- `packages/*` は Agent Harness の配布単位です。
- package の中身（`.apm/instructions`, `.apm/skills`, `.apm/agents`）を変更したら、`apm install` / `apm compile --validate` / `apm audit --ci --policy org` で検証します。
- 生成先リポジトリでは `AGENTS.md` や `.codex/agents/**` などの**生成物を直接編集せず**、この管理repoの package 側を直して再適用します。

## 2. Package 一覧（役割と適用先）

| Package | 主な責務 | 典型的な適用先 |
|---|---|---|
| `core` | 共通ルール/共通スキル | 全repo |
| `shared-core` | runtime 非依存の共通資産 | codex/claude 併用repo |
| `codex-core` | Codex 固有資産 | Codex runtime repo |
| `claude-core` | Claude 固有資産 | Claude runtime repo |
| `docs` | docs保守運用 | docs更新が多いrepo |
| `template-adoption` | 既存repoへの段階適用支援 | 既存repo |
| `ts-fullstack` | TS frontend/backend開発支援 | TS fullstack repo |
| `api-contract` | OpenAPI/生成物運用 | API契約駆動repo |
| `frontend-e2e` | E2E/monkey運用 | frontendを持つrepo |
| `db` | migration/seed運用 | DBを持つrepo |
| `python-core` | Python service基盤 | Python service repo |
| `python-ai` | Prompt/モデル統合運用 | Python AI repo |
| `ai-evals` | eval dataset/回帰運用 | AI機能を持つrepo |
| `ai-safety` | injection/PII/safety運用 | AI機能を持つrepo |

## 3. メンテナンス手順（この管理repo内）

1. 変更対象 package を決める（例: `packages/api-contract`）。
2. package 配下の `.apm/*` を更新する。
3. 動作確認を実行する。

```bash
apm install
apm compile --validate
apm audit --ci --policy org
```

4. 必要に応じて `README.md` / `docs/` の運用説明を更新する。

### バージョン運用（最小）

- 互換性を壊さない修正: patch 相当で更新。
- 運用手順追加や新スキル追加: minor 相当で更新。
- 既存運用を壊す変更: major 相当として扱う。

> 実際のバージョン更新単位（tag/lock更新）は、各組織のリリースポリシーに合わせてください。

## 4. 新規リポジトリへの適用（初期導入）

1. テンプレート生成または既存repo準備。
2. `apm.yml` に必要 package を定義。
3. 以下を実行。

```bash
apm install
apm compile --validate
```

4. 生成物が期待通りかを確認。

```bash
python scripts/standard/standardctl.py doctor --runtime codex
# Claude runtime を使う場合
python scripts/standard/standardctl.py doctor --runtime claude
```

## 5. 既存リポジトリへの段階適用（推奨）

一括導入ではなく、`standardctl apply --section` で1セクションずつ適用します。

```bash
python scripts/standard/standardctl.py apply --section api-contract-openapi
python scripts/standard/standardctl.py apply --section python-ai-core
```

- 適用後は `docs/harness/adoptions/` のレポートを確認。
- CIで `doctor` / `drift` / 言語別 verify を必ず実行。

## 6. 更新運用（テンプレート/ハーネス追随）

- テンプレート更新確認:

```bash
python scripts/standard/standardctl.py update-template
```

- Harness更新確認:

```bash
python scripts/standard/standardctl.py update-harness
```

- 差分健全性確認:

```bash
python scripts/standard/standardctl.py drift --runtime codex
python scripts/standard/standardctl.py drift --runtime claude
```

## 7. トラブル時の切り分け

- `doctor` 失敗: 必須ファイル不足 or runtime ミスマッチ。
- `apm compile --validate` 失敗: package 定義/参照整合性の問題。
- `apm audit --ci --policy org` 失敗: policy違反。
- 生成物差分が想定外: package直編集ではなく、元の `.apm/*` の意図を再確認。

## 8. 最短チェックリスト

- [ ] 変更は `packages/*` のソース側で実施したか
- [ ] `apm install` / `apm compile --validate` / `apm audit --ci --policy org` を実行したか
- [ ] `standardctl doctor/drift` で runtime 別に確認したか
- [ ] 既存repo適用時は `apply --section` で小さく導入したか
