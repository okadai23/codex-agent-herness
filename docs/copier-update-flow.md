# Copier update 運用

## 手順
1. `copier check-update`
2. `copier update --defaults --conflict rej`
3. `git status` で差分確認
4. `.rej` と conflict marker を検出

## Conflict 検出スクリプト
- `scripts/check-copier-conflicts.sh` を実行

## 注意
- `.copier-answers.yml` は手編集しない。
