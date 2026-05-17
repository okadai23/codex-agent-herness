# db-migration-safety

この指示は `db` package 向けの標準ガードレールです。

- 生成ファイルやsecretの取り扱いを順守する。
- 変更前後でverifyコマンドを実行する。
