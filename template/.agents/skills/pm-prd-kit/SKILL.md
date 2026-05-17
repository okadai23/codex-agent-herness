# PM PRD Kit Skill

## 目的
Product Manager が PRD（Product Requirements Document）を高速に作成・レビューするためのスキルです。

## 提供機能
- PRD の初稿生成（課題定義、ゴール、非ゴール、要件、計測）
- リスク・依存関係・未確定事項（Open Questions）抽出
- リリース計画（MVP / v1 / vNext）分割
- エンジニア向け実装チケットへの分解

## 入力
- `product_context`: プロダクト背景
- `problem_statement`: 解決したい課題
- `target_users`: 対象ユーザー
- `constraints`: 予算・納期・法務・技術制約
- `success_metrics`: 成功指標（任意）

## 出力
以下の構成で `docs/prd/<topic>.md` を生成または更新します。

1. 背景
2. 課題
3. ゴール / 非ゴール
4. ユーザーストーリー
5. 要件（機能 / 非機能）
6. 計測設計
7. リスクと軽減策
8. Open Questions
9. リリース計画

## 実行手順
1. 入力の不足項目を列挙（不明点は明示した上で合理的な仮定を置く）
2. `templates/prd-template.md` を基に初稿作成
3. `checklists/prd-quality-checklist.md` で自己レビュー
4. 実装チケット案を `docs/prd/tasks-<topic>.md` に出力

## Guardrails
- 曖昧な要求は「要確認」として明示
- 計測不能な要件は受け入れ基準にしない
- セキュリティ・プライバシー影響を必ず1項目以上確認
