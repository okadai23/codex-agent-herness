# $github-mcp-read

## 目的
GitHub MCP を使って GitHub 上の Issue / Pull Request / リポジトリ情報を安全に取得する。

## 前提
- GitHub Personal Access Token (PAT) または同等の認証情報が発行済みである。
- MCP クライアントで GitHub MCP サーバーが設定済みである。
- 対象 Organization / Repository への参照権限がある。

## 手順
1. 取得対象（Issue、PR、Commit、Workflow など）を明確化する。
2. 絞り込み条件（repo、state、label、期間）を指定して最小範囲で取得する。
3. 取得結果にトークンや個人情報が含まれないか確認する。
4. 出典（repo URL、Issue/PR 番号）を記録する。

## 追加ルール
- 大量取得時はページネーションと条件指定を必ず行う。
- Private repo 情報は公開チャネルへ転載しない。
