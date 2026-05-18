# Dual runtime policy

## 共通管理
- `standard.yml` の `agentRuntime`
- `scripts/standard/standardctl.py`

## ランタイム専用
- Codex専用: `.codex/**`
- Claude専用: `.claude.instructions.md`

## 同一PRレビュー観点
- 片側ランタイムのみ壊していないこと（doctor/driftを両方実行）。
- 生成物を直接ではなく、テンプレート/生成フローで変更していること。

## 失敗時の修復
1. `python scripts/standard/standardctl.py doctor --runtime codex` と `--runtime claude` を再実行。
2. 不足ファイルがあれば `copier update --defaults` で再生成。
3. `drift` 失敗時は `copier check-update` / `apm compile --validate` の失敗原因を先に解消。
