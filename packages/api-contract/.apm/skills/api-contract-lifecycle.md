# $api-contract-lifecycle

## ルール
- 新規API要求は **OpenAPI更新を先行** する。
- generated client / mock は手編集しない（生成コマンドで更新）。
- mismatch発生時は provider-first で修正し、consumer 側に repair request を作る。

## 手順
1. OpenAPI変更。
2. `pnpm api:lint`。
3. Orval / mock再生成。
4. API test（happy path + error path）を更新。
