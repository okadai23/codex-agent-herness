# product-standard-template (seed)

このリポジトリは **Copier template管理repo** です。React/TypeScript/Python AI service 向けの標準テンプレートを管理します。

## リポジトリ方針
- `template/` 配下が Copier の生成元です。
- `copier.yml` で profile (`ts-fullstack` / `python-ai-service` / `hybrid-product`) を切り替えます。
- `.copier-answers.yml` と `apm.lock.yaml` は生成先で手編集しません。

## Claude Code 対応（実装済み最小セット）

- `copier.yml` に `agent_runtime`（`codex` / `claude` / `dual`）を追加。
- `template/standard.yml` に `agentRuntime` を出力。
- `scripts/standard/standardctl.py` に `doctor --runtime` / `drift --runtime` を追加。
- Claude向け最小ガイドとして `template/.claude.instructions.md` を追加。

例:

```bash
python scripts/standard/standardctl.py doctor --runtime claude
python scripts/standard/standardctl.py drift --runtime claude
```

## Ubuntu / macOS 向け Agent ツール導入

`apm` / `Claude Code` / 周辺ライブラリをまとめて導入するスクリプトを追加しています。

```bash
./scripts/install-agent-tooling.sh
```

オプション環境変数:

- `INSTALL_APM=0`: APM の導入をスキップ
- `INSTALL_CLAUDE_CODE=0`: Claude Code の導入をスキップ
- `INSTALL_NODE_LIBS=0`: `pnpm` / `typescript` / `tsx` の導入をスキップ

例:

```bash
INSTALL_CLAUDE_CODE=0 ./scripts/install-agent-tooling.sh
```

## 初期ブランチ保護
v1 では最低限として以下を設定してください。
- main への直接 push 禁止
- PR 必須
- required checks: lint/test/docs verify

詳細は `docs/branch-protection.md` を参照。


## Notion MCP Skill の追加と利用方法

`packages/core/.apm/skills/` に以下の Skill を追加しています。

- `notion-mcp-read`: Notion から情報を取得するための運用手順
- `notion-mcp-write`: Notion へ安全に書き込むための運用手順

### Notion MCP セットアップ

1. Notionで Integration を作成し、Internal Integration Token を発行する。
2. 参照/更新したい Notion ページまたはデータベースで「接続」を開き、作成した Integration を追加する。
3. MCPクライアント設定で Notion MCP サーバーを有効化する（例: `notionApiKey` を環境変数で渡す）。
4. ローカル環境変数にトークンを設定する（例: `export NOTION_API_KEY=...`）。

### 認証のポイント

- トークンは必ず環境変数やシークレットストア経由で設定し、リポジトリへコミットしない。
- Integration 側で必要最小限のアクセス権限を付与する。
- 認証エラー時は、(a) トークン有効性 (b) 対象ページへの Integration 接続 (c) MCP設定のキー名 を順に確認する。


## GitHub MCP Skill の追加と利用方法

`packages/core/.apm/skills/` に以下の Skill を追加しています。

- `github-mcp-read`: GitHub から情報を取得するための運用手順

### GitHub MCP セットアップ

1. GitHub で Personal Access Token (PAT) を作成する（最小権限推奨）。
2. 必要な権限を PAT に付与する（例: `repo`、`read:org`、必要に応じて `workflow`）。
3. MCPクライアント設定で GitHub MCP サーバーを有効化する（例: `githubToken` を環境変数で渡す）。
4. ローカル環境変数にトークンを設定する（例: `export GITHUB_TOKEN=...`）。

### GitHub MCP 認証のポイント

- トークンは環境変数またはシークレットマネージャで管理し、リポジトリに保存しない。
- 利用する Organization / Repository に対して PAT の権限が不足していないか確認する。
- 認証エラー時は、(a) トークン期限/失効 (b) 権限スコープ (c) MCP設定のキー名 を順に確認する。


## Packageメンテナンス/適用ガイド

各Packageの保守方法と実環境への適用フローは以下を参照してください。

- `docs/package-maintenance-and-apply-guide.md`

