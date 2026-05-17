# $db-lifecycle-maintenance

## 高リスク変更
- `DROP TABLE`
- `DROP COLUMN`
- type narrowing

## seedルール
- 決定的・冪等・PIIなし。
- E2E seed scenario catalog と対応付ける。
