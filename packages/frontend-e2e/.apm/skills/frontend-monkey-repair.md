# $frontend-monkey-repair

## 記録必須
- seed
- step count
- trace
- screenshot
- console error

## 実施方針
- BrowserUse / Playwright MCP は探索用途。CI合否の唯一根拠にしない。
- monkey失敗時は再現コマンド付きで repair request を作成する。
