# Security Assessment (2026-05-18)

## 対象
- `scripts/install-agent-tooling.sh`
- `scripts/standard/standardctl.py`
- `template/services/ai/src/api/main.py`
- `template/scripts/run_evals.py`

## 主要な懸念点

### 1) サプライチェーン攻撃リスク（高）
- `scripts/install-agent-tooling.sh` は `curl` で取得した内容をそのまま実行するインストール方式を含み、配布元改ざん時の影響が大きい。
- npm グローバル導入もバージョン固定がなく、想定外のメジャー更新が混入する可能性がある。

**修正方針**
1. 取得物のハッシュ検証（SHA256）を必須化。
2. npm パッケージをバージョン固定（または最小限の範囲指定）し、更新は明示PR運用にする。
3. `sudo` 実行前に確認プロンプトではなく、CI/ドキュメントで最小権限運用を明記する。

### 2) コマンド実行の信頼境界が曖昧（中）
- `scripts/standard/standardctl.py` は `copier`/`apm`/`pnpm` を環境に依存して実行する。PATHハイジャックや意図しないバイナリ実行の余地がある。

**修正方針**
1. 実行バイナリの絶対パス解決（`shutil.which`）と許可リスト化。
2. `--no-network` 相当の安全モードを追加し、`drift/update` での外部アクセスを制御可能にする。
3. `run_cmd` 実行時にタイムアウトを導入し、ハング/DoS耐性を上げる。

### 3) API入力バリデーション不足（中）
- `template/services/ai/src/api/main.py` の `/generate` は `dict[str, str]` を直接受け取り、入力サイズ・必須項目・形式が未検証。
- 巨大入力や不正ペイロードでリソース負荷が高まる可能性がある。

**修正方針**
1. Pydantic モデルでスキーマ定義（`input` 必須、最大長設定）。
2. レート制限/タイムアウト導入（テンプレート側の推奨設定として記載）。
3. 将来の実プロバイダ接続時を見据え、プロンプトインジェクション耐性チェックのフックを追加。

### 4) PII検知の網羅性不足（低〜中）
- `template/scripts/run_evals.py` の PII 検知は正規表現が限定的（SSN, email風文字列のみ）で、電話番号・カード番号・住所などは未対応。

**修正方針**
1. ルール拡張（電話・カード番号・API key 形式など）。
2. allowlist / denylist の仕組みを導入し、誤検知と検知漏れを運用で調整可能にする。
3. 失敗時に検知した行番号とルールIDを出力し、修正容易性を上げる。

## 優先度付き実行計画

### Phase A（今週）
- インストーラのバージョン固定とハッシュ検証実装。
- `standardctl` の `run_cmd` にタイムアウト・バイナリ検証追加。
- `/generate` の Pydantic 入力モデル化と最大入力長制限。

### Phase B（次週）
- eval PII スキャンルール拡張＋テスト追加。
- セキュリティ回帰テスト（悪性入力・長大入力・PATHハイジャック想定）を追加。

### Phase C（運用）
- CI に security job（依存監査 + script lint + SAST）を追加。
- 依存更新ポリシー（固定/更新頻度/承認フロー）を `docs/` に明文化。

## 受け入れ基準（完了定義）
- 高優先度（Phase A）の変更がすべて実装済み。
- 追加したセキュリティテストが CI で通過。
- ドキュメントに運用ルールとロールバック手順が記載されている。
