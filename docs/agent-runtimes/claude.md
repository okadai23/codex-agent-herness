# Claude runtime

## 対象
- `agent_runtime=claude` または `dual`。

## 必須ファイル
- `.claude.instructions.md`

## 検証
- `python scripts/standard/standardctl.py doctor --runtime claude`
- `python scripts/standard/standardctl.py drift --runtime claude`
