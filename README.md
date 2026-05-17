# product-standard-template (seed)

このリポジトリは **Copier template管理repo** です。React/TypeScript/Python AI service 向けの標準テンプレートを管理します。

## リポジトリ方針
- `template/` 配下が Copier の生成元です。
- `copier.yml` で profile (`ts-fullstack` / `python-ai-service` / `hybrid-product`) を切り替えます。
- `.copier-answers.yml` と `apm.lock.yaml` は生成先で手編集しません。

## 初期ブランチ保護
v1 では最低限として以下を設定してください。
- main への直接 push 禁止
- PR 必須
- required checks: lint/test/docs verify

詳細は `docs/branch-protection.md` を参照。
